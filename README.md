# Telugu Morphological Analyzer: Hybrid Approach with Statistical Fallback

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Flask](https://img.shields.io/badge/Python-Flask-brightgreen)](https://flask.palletsprojects.com/)
[![SentencePiece](https://img.shields.io/badge/SentencePiece-v0.1.99-blue)](https://github.com/google/sentencepiece)
[![Morfessor](https://img.shields.io/badge/Morfessor-2.0-orange)](https://github.com/aalto-speech/morfessor)

## Overview

This repository contains a Telugu morphological analyzer built using a hybrid approach. It combines rule-based techniques (sandhi rules, prefix/suffix extraction) with statistical methods (Morfessor, Byte-Pair Encoding) to segment and analyze Telugu words. The analyzer is implemented as a Flask web application, allowing users to input Telugu words or sentences and receive a morphological analysis showing the root word and any affixes.

This analyzer is designed to:

*   **Segment Telugu words into their constituent morphemes.**
*   **Identify prefixes and suffixes.**
*   **Handle sandhi (phonetic combination) rules.**
*   **Provide a fallback mechanism using statistical models for unknown words.**
*   **Offer a user-friendly web interface for analysis.**

## Features

*   **Hybrid Approach:** Combines rule-based and statistical techniques for improved accuracy.
*   **Sandhi Rule Application:** Handles common Telugu sandhi phenomena.
*   **Prefix/Suffix Extraction:** Identifies and labels prefixes and suffixes.
*   **Morfessor Integration:** Uses Morfessor for unsupervised morphological segmentation.
*   **Byte-Pair Encoding (BPE):** Leverages SentencePiece BPE for subword segmentation.
*   **Flask Web Application:** Easy-to-use web interface for analysis.
*   **JSON Data Files:** Uses JSON files for prefixes, suffixes, sandhi rules, and known roots, making it easy to extend and customize the rule set.

## Architecture

The application follows a modular architecture:

1.  **Data Loading:**  Loads prefixes, suffixes, sandhi rules, and known roots from JSON files. Also loads the Morfessor and SentencePiece models.
2.  **Preprocessing:** Handles sentence splitting and whitespace trimming.
3.  **Rule-Based Analysis:** Applies sandhi rules, extracts prefixes and suffixes, and checks for known roots.
4.  **Statistical Fallback:** Uses Morfessor and BPE models to segment unknown words.
5.  **Output:**  Returns a JSON response with the input word and its morphological analysis.
6.  **Web Interface:** Implemented with Flask, providing a simple user interface.

## Technologies Used

*   **Python:** The primary programming language.
*   **Flask:** A micro web framework for building the web application.
*   **Morfessor:** An unsupervised morphological segmentation tool.
*   **SentencePiece:** A subword tokenizer, including Byte-Pair Encoding (BPE).
*   **JSON:** Used for storing morphological rules and data.
*   **HTML/CSS/JavaScript:** For the web interface.

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/<your_github_username>/telugu-morphological-analyzer.git
    cd telugu-morphological-analyzer
    ```

2.  **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Obtain the necessary data files (see below).**  Place the following files in the root directory:

    *   `morfessor_telugu.model`
    *   `bpe_telugu.model`
    *   `prefixes.json`
    *   `suffixes.json`
    *   `sandhi_rules.json`
    *   `known_roots.json`
    *   `telugu_corpus.txt` (See note below about obtaining this file.)

4.  **Run the Flask application:**

    ```bash
    python app.py
    ```

5.  **Access the application in your browser:**  Open your web browser and go to `http://127.0.0.1:5000/`.

## Obtaining the Data Files

The core data files (`prefixes.json`, `suffixes.json`, `sandhi_rules.json`, and `known_roots.json`, `morfessor_telugu.model`, `bpe_telugu.model`) are included in this repository.

**Important: The `telugu_corpus.txt` file is not included directly in this repository due to its large size.** You can download it from the following Google Drive link: [Telugu Corpus (Google Drive)](https://drive.google.com/file/d/1i5G1FluRSFVpu0CcXojKL068801Q72u8/view?usp=drive_link)

**Please be aware:** The corpus may be updated periodically, and the version available via the link may change. By downloading it, you acknowledge that you are solely responsible for all use, storage, and transfer of the contents of the file. Be advised that the original file creators may own licensing. It is recommended that the corpus is used for academic purposes only.

## Usage

1.  **Enter a Telugu word or sentence** in the text box on the web interface.
2.  **Click the "Analyze" button.**
3.  The analysis will be displayed below the input box, showing the segmented morphemes and their roles (Prefix, Root, Suffix).

## Example

**Input:**  `భారతదేశం`

**Output:** `భారతదేశం_Root`

**Input:** `ప్రాతినిధ్యం వహిస్తుంది`

**Output:** `ప్రాతినిధ్యం_Root + వహి_Root + స్తుంది_Suffix`

## Contributing

Contributions are welcome!  If you have improvements to the code, data files (prefixes, suffixes, sandhi rules, known roots), or documentation, please submit a pull request.  Specifically, contributions to the following would be very helpful:

*   Expanding the prefix and suffix lists.
*   Adding more sandhi rules.
*   Improving the accuracy of the statistical models by providing training the Morphossor and SentencePiece models with more data

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

*   This project utilizes the [Morfessor](https://github.com/aalto-speech/morfessor) toolkit for unsupervised morphological segmentation.
*   This project utilizes the [SentencePiece](https://github.com/google/sentencepiece) library for subword tokenization.
