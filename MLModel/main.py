from preprocessing import Preprocess
from aspect_extraction import AspectExtractor
from sentiment_analysis import SentimentAnalyzer
import pandas as pd


def review_analysis(df):
    """
    Analyses the opinions toward the product.

    Args:
        df: A Pandas DataFrame containing the reviews.

    Returns:
        A Pandas DataFrame containing the preprocessed reviews.
    """

    review = Preprocess(df)
    preprocessed_data = review.preprocess_data()

    # TODO: Aspect extraction

    # TODO: Sentiment Analysis

    return preprocessed_data


if __name__ == "__main__":

    reviews = []  # Initialize with an empty list

    # Read data from the text file (each line is treated as a separate entry)
    try:
        with open('./MLModel/data/ScrapedData.txt', 'r', encoding='utf-8') as file:
            reviews = file.readlines()
    except FileNotFoundError:
        print("The input file does not exist.")
    except IOError as e:
        print(f"An error occurred while reading the input file: {str(e)}")

    if reviews:
        # Create a DataFrame from the reviews
        df = pd.DataFrame({'Review': reviews})

        # Analyse the opinions toward the product
        print(review_analysis(df))
    else:
        print("No reviews were loaded. Exiting the program.")
