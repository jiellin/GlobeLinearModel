# -*- coding: utf-8 -*-
'''
Created on Dec 27, 2015

@author: jielin
'''

import sys
from GlobalLinearModel.PerceptronOnlineLearning import Perceptron
from GlobalLinearModel.PosTagger import PosTagger
from utils.common import read_data, PARAM_PATH, TEST_DATA_PATH, OUTPUT_PATH
from GlobalLinearModel.gen_features import features

if __name__ == '__main__':
    params = PARAM_PATH
    test_data_path = TEST_DATA_PATH
    output_path = OUTPUT_PATH
    #count all tags
    for x in read_data(test_data_path):
        pass
    TaggerTool = PosTagger(test_data_path, features, params, output_path)
    TaggerTool.tag()
