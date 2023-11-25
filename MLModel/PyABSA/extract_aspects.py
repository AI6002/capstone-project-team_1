from pyabsa import ATEPCCheckpointManager


def extract_aspects_from_file(file_path):
    aspect_extractor = ATEPCCheckpointManager.get_aspect_extractor(
        checkpoint="100.electronics",
        auto_device=True,  # False means load model on CPU
        cal_perplexity=True,
    )

    scraped_data = []
    with open(file_path, 'r') as f:
        for line in f:
            scraped_data.append(line.strip())  # Assuming each line is a separate piece of text

    inference_source = examples = scraped_data
    aepc_result = aspect_extractor.extract_aspect(
        inference_source=inference_source,
        save_result=True,
        print_result=True,
        pred_sentiment=True,
    )

    reviews = []

    for example in aepc_result:
        reviews.append((example['aspect'], example['sentiment']))

    return reviews