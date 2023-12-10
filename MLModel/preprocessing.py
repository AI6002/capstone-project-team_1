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

        max_line_length = 128

        # Open the input and output files
        with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w',
                                                                              encoding='utf-8') as output_file:
            # Read the content of the input file
            input_text = input_file.read()
            
            # Extract the first line as the category
            first_line_break = input_text.find('\n')  # Find the first newline character
            category = input_text[:first_line_break].strip()  # Extract the first line
            remaining_text = input_text[first_line_break:].lstrip('\n')  # Remove the first line from the remaining content
      
            # Tokenize the input text into sentences
            sentences = sent_tokenize(remaining_text)

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
        
        return category

    def concat_rows_by_length(self, input_csv_path, max_length=512):
        """
        Concatenate rows in a CSV file based on the length of the review sentences.

        Args:
            input_csv_path (str): Path to the input CSV file.
            max_length (int): Maximum length for concatenation.

        Returns:
            pd.DataFrame: Concatenated data as a Pandas DataFrame.
        """
        # Read the input CSV file
        data = pd.read_csv(input_csv_path)

        # Initialize variables for concatenated rows
        concatenated_reviews = []
        concatenated_positives = []
        concatenated_negatives = []

        current_review = ""
        current_positive = []
        current_negative = []

        # Iterate through each row in the data
        for index, row in data.iterrows():
            review = row['Review']
            positive_aspects = row['Best_Features']
            negative_aspects = row['Worst_Features']

            # Check if adding the current review exceeds the maximum length
            if len(current_review) + len(review) > max_length:
                # Append the current concatenated row
                concatenated_reviews.append(current_review)
                concatenated_positives.append(current_positive)
                concatenated_negatives.append(current_negative)

                # Reset current variables
                current_review = review
                current_positive = []
                current_negative = []
            else:
                # Add the current review to the current concatenated row
                current_review += review

            # Check for NaN values and replace with an empty list
            current_positive += [] if pd.isna(positive_aspects) else [aspect.strip() for aspect in positive_aspects.split(',')]
            current_negative += [] if pd.isna(negative_aspects) else [aspect.strip() for aspect in negative_aspects.split(',')]

        # Append the last concatenated row
        concatenated_reviews.append(current_review)
        concatenated_positives.append(current_positive)
        concatenated_negatives.append(current_negative)

        # Create a new DataFrame with the concatenated data
        concatenated_data = pd.DataFrame({
            'Review': concatenated_reviews,
            'Positive_Aspects': concatenated_positives,
            'Negative_Aspects': concatenated_negatives
        })

        return concatenated_data

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