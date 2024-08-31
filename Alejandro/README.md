# HAAG | NLP | Fall 2024

This repo contains scripts written as the NLP group works toward solutions for the "sentencias" project in Dominican Republic

Initial experiment is to extract/identify the following:  
    - Names of the parties (individuals, companies)  
    - Amounts of money  
    - Dates (and ideally the event that happened on that date)

Resources: [Spanish/English Legal Terms Glossary](https://www.saccourt.ca.gov/general/legal-glossaries/docs/spanish-legal-glossary.pdf)

## Environment Setup

Prerequisites:

- Ensure you have installed [miniconda](https://docs.anaconda.com/miniconda/)
- Install [spaCy](https://spacy.io/usage)

### Test your Installation

```bash
conda list
```

### Create the Conda Environment

```bash
conda env create --name nlp_env --file=environment.yml
```

### (Optional) If an update to the dependencies is needed

```bash
conda env update --name nlp_env --file environment.yml --prune
```

or

```bash
conda install -n nlp_env <name_of_new_package> --update-deps --force-reinstall
```

### Activate the Conda Environment

```bash
conda activate nlp_env
```

### Download the Pre-Trained Language Model

```bash
python -m spacy download es_core_news_sm
```

Now reload VSCode (or other IDE) and select your new environment as the Jupyter Notebook kernel.
