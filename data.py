import os
import pyconll


def dataPreprocces(
    path_to_sample: str,
    path_to_result: str,
    targetUpos: list[str],
    MAX_ROLE_NUMBER: int,
) -> int:
    """
    Creates a balanced dataset of sentences for the each language that was included in a sample.

    Arguments:
        path_to_sample: str
            The path to the .txt, where a list of .conllu of languages that were included in a sample is written.
        path_to_result: str
            The path to the directory, where the future balanced .conllu files of a sample will be stored.
        targetUpos: list[str]
            A macroparameter, the list of upos, included in the consideration of the research.
        MAX_ROLE_NUMBER: int
            A macroparameter that is needed to balance the dataset of each language.

    Return:
        int: 0 in case of successful execution
    """

    with open(path_to_sample, "r") as sample:
        sample = sample.readlines()

    balanced_dir = f"{path_to_result}/Balanced-Datasets"
    if not os.path.isdir(balanced_dir):
        os.makedirs(balanced_dir)

    for language in sample:
        language_name = language.split("/")[-2]

        balanced_language_path = (
            f"{language.split("/")[-1].split(".")[0]}-balanced.conllu"
        )

        with open(f"{balanced_dir}/{balanced_language_path}", "a") as balanced_corpus:

            corpus = pyconll.iter_from_file(language.strip())
            roles = {"S": 0, "A": 0, "O": 0}
            sentences_all, sentences_balanced = 0, 0
            sentences = []

            for sentence in corpus:
                sentences_all += 1
                role_S, role_A, role_O = 0, 0, 0
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

                    # exclude pronouns, aux as heads and passive constructions
                    if (
                        token.upos in targetUpos
                        and headUpos == "VERB"
                        and not is_passive
                    ):
                        # object detection
                        if token.deprel in ["obj", "iobj"]:
                            role_O += 1
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
                                role_A += 1
                            else:
                                role_S += 1

                if role_A + role_S + role_O != 0:
                    sentences.append((sentence.id, sentence, role_A, role_S, role_O))
            sentences = sorted(
                sentences, key=lambda x: (x[2], x[3], x[4]), reverse=True
            )

            for sentence_id, sentence, a, s, o in sentences:
                flag = False
                if (
                    roles["A"] <= MAX_ROLE_NUMBER
                    and roles["S"] <= MAX_ROLE_NUMBER
                    and roles["O"] <= MAX_ROLE_NUMBER
                ):
                    roles["A"] += a
                    roles["S"] += s
                    roles["O"] += o
                    flag = True
                elif roles["A"] > MAX_ROLE_NUMBER and not a:
                    if roles["S"] <= MAX_ROLE_NUMBER and roles["O"] <= MAX_ROLE_NUMBER:
                        roles["S"] += s
                        roles["O"] += o
                        flag = True
                    elif (
                        roles["S"] <= MAX_ROLE_NUMBER
                        and roles["O"] > MAX_ROLE_NUMBER
                        and not o
                    ):
                        roles["S"] += s
                        flag = True
                    elif (
                        roles["S"] > MAX_ROLE_NUMBER
                        and roles["O"] <= MAX_ROLE_NUMBER
                        and not s
                    ):
                        roles["O"] += o
                        flag = True
                elif roles["S"] > MAX_ROLE_NUMBER and not s:
                    if roles["A"] <= MAX_ROLE_NUMBER and roles["O"] <= MAX_ROLE_NUMBER:
                        roles["A"] += a
                        roles["O"] += o
                        flag = True
                    elif (
                        roles["A"] <= MAX_ROLE_NUMBER
                        and roles["O"] > MAX_ROLE_NUMBER
                        and not o
                    ):
                        roles["A"] += a
                        flag = True
                    elif (
                        roles["A"] > MAX_ROLE_NUMBER
                        and roles["O"] <= MAX_ROLE_NUMBER
                        and not a
                    ):
                        roles["O"] += o
                        flag = True
                elif roles["O"] > MAX_ROLE_NUMBER and not o:
                    if roles["A"] <= MAX_ROLE_NUMBER and roles["S"] <= MAX_ROLE_NUMBER:
                        roles["A"] += a
                        roles["S"] += s
                        flag = True
                    elif (
                        roles["A"] > MAX_ROLE_NUMBER
                        and roles["S"] <= MAX_ROLE_NUMBER
                        and not a
                    ):
                        roles["S"] += s
                        flag = True
                    elif (
                        roles["A"] <= MAX_ROLE_NUMBER
                        and roles["S"] > MAX_ROLE_NUMBER
                        and not s
                    ):
                        roles["A"] += a
                        flag = True

                if flag:
                    balanced_corpus.write(sentence.conll())
                    balanced_corpus.write("\n\n")
    return 0


def tokensExtraction():
    """
    Extracts sentences and their tokens from .conllu files with target roles.
    """
    pass
