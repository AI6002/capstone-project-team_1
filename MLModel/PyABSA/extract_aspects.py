# -*- coding: utf-8 -*-
# file: extract_aspects.py
# time: 2021/5/27 0027
# author: yangheng <hy345@exeter.ac.uk>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
from pyabsa import ABSADatasetList, available_checkpoints
from pyabsa import ATEPCCheckpointManager

# checkpoint_map = available_checkpoints(from_local=False)


aspect_extractor = ATEPCCheckpointManager.get_aspect_extractor(
    checkpoint="english",
    auto_device=True,  # False means load model on CPU
    cal_perplexity=True,
)

# load data from a text file line by line in a list
scraped_data = []
#with open("mlmodel/data/Train_70_LinebyLine.txt", 'r') as f:
with open("mlmodel/data/sample_scraped_data_linebyline.txt", 'r') as f:
    for line in f:
        scraped_data.append(line)
inference_source = examples = scraped_data
print(inference_source)
atepc_result = aspect_extractor.extract_aspect(
    inference_source=inference_source,  #
    save_result=True,
    print_result=True,  # print the result
    pred_sentiment=True,  # Predict the sentiment of extracted aspect terms
)

for example in atepc_result:
    print(example['aspect'], example['sentiment'])

#print(atepc_result)
