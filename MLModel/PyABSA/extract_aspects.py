from pyabsa import ATEPCCheckpointManager


def extract_aspects_from_file(file_path):
    aspect_extractor = ATEPCCheckpointManager.get_aspect_extractor(
        #checkpoint="MLModel/PyABSA/finetuned_models/best_model",
        checkpoint="MLModel/PyABSA/finetuned_models/fast_lcf_atepc_600.electronics600_cdw_apcacc_82.63_apcf1_78.08_atef1_78.55",
        #checkpoint="100.electronics",
        auto_device=True,  # False means load model on CPU
        cal_perplexity=True,
    )

    scraped_data = []
    with open(file_path, 'r', encoding='utf-8') as f:
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