import pyconll
import pandas as pd


def roleCounter(path_to_sample: str, path_to_result: str, targetUpos: list[str]) -> int:
    """
    Counts the number of A-, S- and O-roles, that are represented in each language of a sample,
    and creates a dataframe with this information.

    Arguments:
        path_to_sample: str
            The path to the list of .conllu files of languages that were included in a sample.
        path_to_result: str
            The path to the future .csv file with pivot table.
        targetUpos: list[str]
            The list of target upos-labels (e.g nouns, proper nouns or pronouns).

    Return:
        int: 0 in case of successful execution

    """
    roles = {}

    with open(path_to_sample, "r") as sample:
        sample = sample.readlines()

    for language in sample:
        language_name = language.split("/")[-2]
        roles[language_name] = {"S": 0, "A": 0, "O": 0}

        corpus = pyconll.iter_from_file(language.strip())
        for sentence in corpus:
            for token in sentence:
                head_id = token.head
                headUpos = (
                    None
                    if (head_id is None or head_id == "0")
                    else sentence[f"{token.head}"].upos
                )

                # exclude passive constructions
                is_passive = False
                if (
                    headUpos == "VERB"
                    and "Voice" in sentence[f"{token.head}"].feats
                    and "Pass" in sentence[f"{token.head}"].feats["Voice"]
                ):
                    is_passive = True

                # include only target upos-labels and exclude aux as heads and passive constructions
                if token.upos in targetUpos and headUpos == "VERB" and not is_passive:
                    # object detection
                    if token.deprel in ["obj", "iobj"]:
                        roles[language_name]["O"] += 1
                    # if subject has an O-sibling => it is A
                    # else S
                    if token.deprel == "nsubj":
                        has_sibling = False
                        for sibling in sentence:
                            if (
                                sibling.head == token.head
                                and sibling.upos in targetUpos
                                and sibling.deprel in ["obj", "iobj"]
                            ):
                                has_sibling = True
                        if has_sibling:
                            roles[language_name]["A"] += 1
                        else:
                            roles[language_name]["S"] += 1

    df = pd.DataFrame.from_dict(roles)

    df.to_csv(path_to_result)

    return 0
