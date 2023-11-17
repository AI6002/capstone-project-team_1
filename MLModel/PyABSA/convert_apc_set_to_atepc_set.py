# -*- coding: utf-8 -*-
# file: convert_apc_set_to_atepc_set.py
# time: 2021/5/27 0027
# author: yangheng <hy345@exeter.ac.uk>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.

from pyabsa.utils.file_utils import convert_apc_set_to_atepc_set
from pyabsa.functional import ABSADatasetList

convert_apc_set_to_atepc_set(
    "MLModel/PyABSA/integrated_datasets/apc_datasets/600.electronics600",
)  # for custom datasets, absolute path recommended for this function
