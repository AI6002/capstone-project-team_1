import sys
from preprocessing import Preprocess
from aspect_mapping import map_reviews_to_synonyms
from feature_sentiment_analysis import analyze_feature_sentiments


def review_analysis(input_file_path, output_file_path):
    """
    Analyze the opinions toward the product based on a DataFrame of reviews.

    Args:
        input_file_path (str): Path to the input file containing reviews.
        output_file_path (str): Path to the output file for processed reviews.
    """

    prep = Preprocess()
    try:
        prep.extract_sentences(input_file_path, output_file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}. The input file does not exist.")
        sys.exit(1)
    except IOError as e:
        print(f"Error: {e}. An error occurred while reading the input file.")
        sys.exit(1)

    with open(output_file_path, 'r', encoding='utf-8') as file:
        reviews = file.readlines()

    # Check if reviews were loaded
    if not reviews:
        print("No reviews were loaded. Exiting the program.")
        sys.exit(0)

    # TODO: add training and fine tuning

    reviews = [
        (['camera', 'performance', 'battery life'], ['Positive', 'Positive', 'Negative']),
        (['photos', 'Android experience', 'battery'], ['Positive', 'Positive', 'Negative']),
        (['price', 'performance', 'OxygenOS', 'camera quality', 'features'],
         ['Positive', 'Positive', 'Positive', 'Negative', 'Negative']),
        (['camera system', 'Google services'], ['Positive', 'Negative']),
        (['design', 'processing power'], ['Positive', 'Negative']),
        (['performance', 'portability'], ['Positive', 'Positive']),
        (['display', 'media consumption', 'productivity', 'price'], ['Positive', 'Positive', 'Positive', 'Neutral']),
        (['use', 'performance', 'applications'], ['Positive', 'Negative', 'Neutral']),
        (['display', 'keyboard', 'stylus'], ['Positive', 'Negative', 'Negative']),
        (['processing power'], ['Negative'])
    ]

    # Call the function from the aspect_mapping module
    mapped_reviews = map_reviews_to_synonyms(reviews)

    # Now you can work with the mapped_reviews
    print(mapped_reviews)

    # Assuming you have already defined 'mapped_reviews' using the 'map_reviews_to_synonyms' function
    best_features, worst_features = analyze_feature_sentiments(mapped_reviews)

    print("Best Features:")
    print(best_features)

    print("\nWorst Features:")
    print(worst_features)


if __name__ == "__main__":
    input_file_path = './MLModel/data/scraped_data.txt'
    output_file_path = './MLModel/data/review_sentences.txt'
    review_analysis(input_file_path, output_file_path)
