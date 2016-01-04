# -*- coding: utf-8 -*-
'''
Created on Dec 27, 2015

@author: jielin

@description:This module contains CONSTANTS and utilized functions
'''

#data path
PARAM_PATH = '../data/param.model'
TRAIN_DATA_PATH = '../data/train_ch.dat'
TEST_DATA_PATH = '../data/test_ch.dat'
OUTPUT_PATH = '../data/test.out'

#train param
ITER_NUM = 3
BATCH_NUM = 2000

#all possible tags
LABEL_SET = set()

####################################
#@func: yield one sentence a time to save memory
####################################
def read_data(filename):
    sentence = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            #line is empty
            if not line:
                yield sentence
                sentence = []
                continue
            #line is not empty
            parts = line.split('\t')
            if len(parts) > 1:
                LABEL_SET.add(parts[1])
                sentence.append((parts[0], parts[1]))
            else:
                sentence.append((parts[0]))
