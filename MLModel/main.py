import asyncio
import torch
import sys
from MLModel.preprocessing import Preprocess
from MLModel.aspect_mapping import map_reviews_to_synonyms
from MLModel.feature_sentiment_analysis import analyze_feature_sentiments
from MLModel.PyABSA.extract_aspects import extract_aspects_from_file


async def review_analysis(input_file_path):
    """
    Analyze the opinions toward the product based on a DataFrame of reviews.

    Args:
        input_file_path (str): Path to the input file containing reviews.
    """

    # Path to the output file for processed reviews
    output_file_path="./MLModel/data/review_sentences.txt"
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

    # TODO: Resolve the memory issue to work with output_file_path
    # Call the function from the aspect_extraction module
    #file_path = "./MLModel/data/sample_scraped_data_linebyline.txt"
    reviews = extract_aspects_from_file(output_file_path)

    # Clear GPU memory
    torch.cuda.empty_cache()

    # Call the function from the aspect_mapping module
    mapped_reviews = map_reviews_to_synonyms(reviews)

    # Now you can work with the mapped_reviews
    print(mapped_reviews)

    # Assuming you have already defined 'mapped_reviews' using the 'map_reviews_to_synonyms' function
    best_and_worst_features = analyze_feature_sentiments(mapped_reviews)

    print(best_and_worst_features)
    
    return best_and_worst_features


async def sentiment_analysis(input_file_path):
    return await review_analysis(input_file_path)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    input_file_path = './MLModel/data/scraped_data.txt'
    loop.run_until_complete(sentiment_analysis(input_file_path))
