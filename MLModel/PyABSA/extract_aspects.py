# -*- coding: utf-8 -*-
# file: extract_aspects.py
# time: 2021/5/27 0027
# author: yangheng <hy345@exeter.ac.uk>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
from pyabsa import ATEPCCheckpointManager

async def extract_aspects_and_sentiments(path_to_data: str, checkpoint: str):

    # load data from a text file line by line in a list
    data_to_analyze = []
    with open(path_to_data, 'r', encoding='utf-8') as f:
        for line in f:
            data_to_analyze.append(line)

    inference_source = data_to_analyze

    # Load the model
    aspect_extractor = ATEPCCheckpointManager.get_aspect_extractor(
    checkpoint=checkpoint,
    auto_device=True,  # False means load model on CPU
    cal_perplexity=True,
    )
    
    # Predict
    atepc_result = aspect_extractor.extract_aspect(
    inference_source=inference_source, 
    save_result=True,
    print_result=True,  # print the result
    pred_sentiment=True,  # Predict the sentiment of extracted aspect terms
    )

    result=[]
    for example in atepc_result:
        aspect_sentiment_pairs = {
        'aspects': example['aspect'],
        'sentiments': example['sentiment']
        }
        result.append(aspect_sentiment_pairs)

    return result

if __name__ == '__main__':
    import asyncio
    print(asyncio.run(extract_aspects_and_sentiments("mlmodel/data/scraped_data.txt","MLModel/PyABSA/checkpoints/finetuned_model")))