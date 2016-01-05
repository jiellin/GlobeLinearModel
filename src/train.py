# -*- coding: utf-8 -*-
'''
Created on Dec 27, 2015

@author: myue
'''

import sys
from GlobalLinearModel.PerceptronOnlineLearning import Perceptron
from utils.common import read_data, TRAIN_DATA_PATH, PARAM_PATH, ITER_NUM, BATCH_NUM
from GlobalLinearModel.gen_features import features

if __name__ == '__main__':
    params = PARAM_PATH
    train_data_path = TRAIN_DATA_PATH
    iter_num = ITER_NUM
    # load all label
    sample_num = 0
    for l in read_data(train_data_path):
        sample_num += 1
    TrainModel = Perceptron(train_data_path, features, params)
    TrainModel.train(iter_num)
    TrainModel.save_params_to_file()
    #TrainModel.save_params_to_pickle()
