"""
Description: Module for data preprocessing tasks in the aspect-based product review analysis project.

This module contains functions and utilities for loading and preprocessing data from customer reviews.
Preprocessing tasks include text cleaning, tokenization, stop word removal, and other data
transformations necessary to prepare the data for aspect identification and sentiment analysis.
"""

import pandas as pd
import re
import unicodedata
import demoji
import nltk
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string


class Preprocess():
    def __init__(self, data=None):
        self.data = data
        nltk.download('punkt')
        nltk.download('wordnet')
        self.lemmatizer = WordNetLemmatizer()

    def extract_sentences(self, input_file_path, output_file_path):
        """
        Extract sentences from an input file and write them to an output file.

        Args:
            input_file_path (str): Path to the input text file.
            output_file_path (str): Path to the output file.
        """
        # Download the punkt tokenizer data if it hasn't already
        nltk.download('punkt')

        max_line_length = 512

        # Open the input and output files
        with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w',
                                                                              encoding='utf-8') as output_file:
            # Read the content of the input file
            input_text = input_file.read()

            # Tokenize the input text into sentences
            sentences = sent_tokenize(input_text)

            # Initialize variables to keep track of the current line length
            current_line = ""
            current_line_length = 0

            # Iterate through sentences
            for sentence in sentences:
                # Check if adding the current sentence exceeds the maximum line length
                if len(current_line) + len(sentence) > max_line_length:
                    # Write the current line to the output file and start a new line
                    output_file.write(current_line + '\n')
                    current_line = sentence
                    current_line_length = len(sentence)
                else:
                    # Add the current sentence to the current line
                    current_line += sentence
                    current_line_length += len(sentence)

            # Write the remaining content to the output file
            if current_line:
                output_file.write(current_line + '\n')

        # Notify that the operation is complete
        print("Sentences have been extracted to", output_file_path)

    def demojize(self, text):
        try:
            emojis = demoji.findall(text)
        except Exception as e:
            print(f"Error while demojizing: {e}")
            emojis = {}

        for emoji in emojis:
            text = text.replace(emoji, " " + emojis[emoji].split(":")[0])

        return text

    def clean_text(self, text):
        try:
            # Normalize text to NFC (Normalization Form C)
            text = unicodedata.normalize('NFKD', text)
            # Convert text to lowercase
            text = text.lower()
            # Remove URLs using regular expression
            text = re.sub(r'http\S+|www\S+|https\S+', '', text)
            # Convert emojis to their English text equivalents
            text = self.demojize(text)
            # Remove punctuation
            text = ''.join([char for char in text if char not in string.punctuation])
            # Remove numbers
            text = ''.join([char for char in text if not char.isdigit()])
            # Remove extra white spaces
            text = ' '.join(text.split())
            return text
        except Exception as e:
            print(f"Error while cleaning text: {e}")
            return ""

    def tokenize_text(self, text):
        try:
            # Tokenize the text using NLTK's word_tokenize
            tokens = word_tokenize(text)
            return tokens
        except Exception as e:
            print(f"Error while tokenizing text: {e}")
            return []

    def lemmatization(self, stemmed_tokens):
        try:
            # Lemmatize tokens
            text = [self.lemmatizer.lemmatize(word) for word in stemmed_tokens]
            return text
        except Exception as e:
            print(f"Error while lemmatizing text: {e}")
            return []

    def preprocess_data(self):
        """
        Preprocesses the review data.

        Returns:
            A Pandas DataFrame containing the preprocessed reviews.
        """

        # Initialize an empty list to store preprocessed data
        preprocessed_data = []

        for review_text in self.data['Review']:
            try:
                # Apply cleaning, tokenization, and stop word removal to each review
                cleaned_text = self.clean_text(review_text)
                tokenized_text = self.tokenize_text(cleaned_text)
                lemmatized_text = self.lemmatization(tokenized_text)

                # Append the preprocessed text to the DataFrame
                preprocessed_data.append({
                    'Cleaned Text': cleaned_text,
                    'Tokenized Text': tokenized_text,
                    'Lemmatized Text': lemmatized_text
                })
            except Exception as e:
                print(f"Error while preprocessing a review: {e}")

        # Convert the list of dictionaries into a DataFrame
        preprocessed_df = pd.DataFrame(preprocessed_data)

        return preprocessed_df