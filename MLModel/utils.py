"""
Description: Contains utility functions for text preprocessing and file operations.
"""

import nltk
from nltk import sent_tokenize


def extract_sentences(input_file_path, output_file_path):
    """
    Extract sentences from an input file and write them to an output file.

    Args:
        input_file_path (str): Path to the input text file.
        output_file_path (str): Path to the output file.
    """
    # Download the punkt tokenizer data if it hasn't already
    nltk.download('punkt')

    # Open the input and output files
    with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
        # Read the content of the input file
        input_text = input_file.read()

        # Tokenize the input text into sentences
        sentences = sent_tokenize(input_text)

        # Write each sentence to the output file on a new line
        for sentence in sentences:
            output_file.write(sentence + '\n')

    # Notify that the operation is complete
    print("Sentences have been extracted to", output_file_path)
