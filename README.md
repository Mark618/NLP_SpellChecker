# Medical Spelling Checker and Corrector

This project focuses on detecting spelling errors and providing correct word suggestions based on a medical dataset. It leverages NLTK language models with bigram and edit distance calculations to identify and correct spelling mistakes. The user interface is built using Dash Plotly, allowing interactive exploration and correction of detected errors.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Methodology](#methodology)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)

## Features
- **Spelling Error Detection**: Detects spelling errors using NLTK language models trained on a medical dataset.
- **Correct Word Suggestions**: Provides suggestions for corrections based on bigrams and edit distance calculations.
- **Interactive User Interface**: Built with Dash Plotly, enabling users to interactively correct detected spelling mistakes.
- **Real-Time Updates**: Displays corrections in real-time and updates suggestions as new words are entered.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Mark618/NLP_SpellChecker.git
    ```
2. Navigate to the project directory:
    ```bash
    cd NLP_SpellChecker
    ```
3. Create a virtual environment and activate it:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```
4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the Dash application:
    ```bash
    python app.py
    ```
2. Open your web browser and go to `http://127.0.0.1:{port number}/` to access the interface.

3. Enter text directly into the interface to check for spelling errors and view suggestions.

## Methodology

1. **Data Preprocessing**: Text data is tokenized and cleaned using the `spaCy` library to remove stop words and punctuation.
2. **Language Model**: An NLTK language model is built using bigrams from the medical dataset to predict probable words based on context.
3. **Error Detection**: For each word in the input, the model checks its presence in the vocabulary. If not found, it suggests corrections based on edit distance and bigram probability.
4. **Correction Suggestions**: Suggestions are generated using a combination of Levenshtein distance and bigram-based cont

## Project Structure
```bash
NLP_SpellChecker/  
├── app.py  # Main Dash application file  
├── data/  
│   └── processed_text.pkl  
├── models/  
│   └── model.pkl  # Trained language models
├── assets/  
│   └── css
├── requirements.txt # Python dependencies
└── README.md # Project README file   
```
## Dependencies  
To install all dependencies, use the following command:

```bash
pip install -r requirements.txt
