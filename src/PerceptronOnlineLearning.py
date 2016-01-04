# -*- coding: utf-8 -*-
'''
Created on Dec 27, 2015

@author: myue

@description:This module implements Perceptron Onling Training Algorithm
'''

import cPickle as pickle
import sys
import time
import random
from FeatureVectorWeightModel import FeatureVectorWeight
from common import read_data, LABEL_SET

class Perceptron(object):
    def __init__(self, train_data_path, feature_template_list, model_params_path):
        self.train_data_path = train_data_path
        self.featureModel = FeatureVectorWeight(feature_template_list, list(LABEL_SET))
        self.model_params_path = model_params_path

    ######################################################
    #@func: train process
    #@param iteration:  iter_num, hyperparam in algorithm
    ######################################################
    def train(self, iteration):
        for i in xrange(iteration):
            print 'iteration: ', i + 1
            for sentence in read_data(self.train_data_path):
                observe_data = [pair[0] for pair in sentence]
                ideal_label = [pair[1] for pair in sentence]
                predict_label = self.featureModel.viterbi(observe_data)
                #update feature vector
                self.featureModel.update(observe_data, ideal_label, predict_label)

    #save feature vector weight
    def save_params_to_file(self):
        alist = list()
        for hashstr in self.featureModel.params:
            weight = self.featureModel.params[hashstr]
            if weight != 0:
                alist.append(hashstr + '\t' + str(weight))
        with open(self.model_params_path,'w') as f:
            tmp_str = '\n'.join(alist)
            f.write(tmp_str)

    def save_params_to_pickle(self):
        final = dict()
        for hashstr in self.featureModel.params:
            weight = self.featureModel.params[hashstr]
            if weight != 0:
                final[hashstr] = weight
        with open(self.model_params_path,'w') as f:
            pickle.dump(final,f)
