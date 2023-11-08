# -*- coding: utf-8 -*-
# file: train_atepc_english.py
# time: 2021/6/8 0008
# author: yangheng <hy345@exeter.ac.uk>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.

########################################################################################################################
#                                               ATEPC training script                                                  #
########################################################################################################################

from pyabsa.functional import ATEPCModelList
from pyabsa.functional import Trainer, ATEPCTrainer
from pyabsa.functional import ABSADatasetList
from pyabsa.functional import ATEPCConfigManager
from pyabsa import available_checkpoints
from pyabsa import ATEPCCheckpointManager

checkpoint_map = available_checkpoints('atepc')

config = ATEPCConfigManager.get_atepc_config_english()
config.model = ATEPCModelList.FAST_LCF_ATEPC
config.evaluate_begin = 4 #0
config.log_step = -1
config.batch_size = 16
config.num_epoch = 2
config.max_seq_len = 128
config.cache_dataset = False
config.use_bert_spc = True
config.l2reg = 1e-5
config.learning_rate = 1e-5
multilingual = ABSADatasetList.English
config.pretrained_bert = "yangheng/deberta-v3-base-absa-v1.1"
Dataset = '100.electronics'

checkpoint_path = ATEPCCheckpointManager.get_checkpoint(checkpoint='english')
aspect_extractor = ATEPCTrainer(
    config=config,
    dataset=Dataset,
    from_checkpoint=checkpoint_path,
    checkpoint_save_mode=2,
    auto_device=True,
    load_aug=False,
).load_trained_model()

# aspect_extractor.extract_aspect(
#     [
#        "My road to the Sennheiser HD 600's has been a little long and filled with some interesting twists and turns that have, or so I hope, led me to a better understanding of what are a great set of headphones.",
# "Naturally it is very typical to wish to compare these to other headphones."
#     ]
# )
