# Balanced Language Sampling for Multilingual Models

This repository contains the results and the visualization of these results that I used in the term paper 'Balanced Language Sampling for Multilingual Models'.

## Replication of the experiment

The code for replicating the experiment was borrowed from the article [Deep Subjecthood: Higher Order Grammatical Features in Multilingual BERT](https://aclanthology.org/2021.eacl-main.215/).

In order to reproduce the experiment from the original article with your own data, you need to install all dependencids from our `requirements.txt` by executing this code:

```
pip install -r /path/to/requirements.txt
```

For further steps you should read the README.md from the [original repository](https://github.com/toizzy/deep-subjecthood).

## Samples

The directory [samples](samples) contains three subdirectories: original sample, balanced sample and extra sample. There are two `.txt` files in each of these subdirectories. There, the information about train- and test-languages, that were included in the samples, is stored. For further information, see the text of the paper.

## Results

The directory [results](results) contains the files that I got from the replication of the experiment on the original, balanced and extra samples. Further they are used in the visualization part.

## Visualization

The `.R` file contains the code for creating a map with languages marked on it. The map was created with the use of R package ['lingtypology'](<https://CRAN.R-project.org/package=lingtypology>).

The `.ipynb` notebook contains the code for creating graphs that I used in the term paper.
