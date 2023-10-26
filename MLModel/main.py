from utils import extract_sentences
from aspect_extraction import AspectExtractor
from sentiment_analysis import SentimentAnalyzer
import pandas as pd


def review_analysis(df):
    """
    Analyze the opinions toward the product based on a DataFrame of reviews.

    Args:
        df (pandas.DataFrame): A DataFrame containing the reviews in a 'Review' column.

    Returns:
        pandas.DataFrame: A DataFrame containing the preprocessed reviews.
    """

    # review = Preprocess(df)
    # preprocessed_data = review.preprocess_data()

    # TODO: Aspect extraction

    # TODO: Sentiment Analysis

    pass


if __name__ == "__main__":

    reviews = []  # Initialize with an empty list
    input_file_path = './MLModel/data/scraped_data.txt'
    output_file_path = './MLModel/data/review_sentences.txt'
    # Read data from the text file (each line is treated as a separate entry)
    try:
        extract_sentences(input_file_path, output_file_path)
    except FileNotFoundError:
        print("The input file does not exist.")
    except IOError as e:
        print(f"An error occurred while reading the input file: {str(e)}")

    with open(output_file_path, 'r', encoding='utf-8') as file:
        reviews = file.readlines()

    if reviews:
        # Create a DataFrame from the reviews
        df = pd.DataFrame({'Review': reviews})

        # Analyse the opinions toward the product
        print(review_analysis(df))
    else:
        print("No reviews were loaded. Exiting the program.")
