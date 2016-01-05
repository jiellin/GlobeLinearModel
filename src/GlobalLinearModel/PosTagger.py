# -*- coding: utf-8 -*-
'''
Created on Dec 27, 2015

@author: myue

@description:This module implements Sentence tagging by trained params
'''

import sys
from FeatureVectorWeightModel import FeatureVectorWeight
from utils.common import read_data, LABEL_SET

class PosTagger(object):
    def __init__(self, test_data_path, feature_template_list, feature_weight_vector, output_path):
        self.test_data_path = test_data_path
        self.featureModel = FeatureVectorWeight(feature_template_list, list(LABEL_SET), feature_weight_vector)
        self.output_path = output_path

    ######################################################
    #@func: calculate precison when test our model
    ######################################################
    def _cal_precision(self, sentence, predict_label):
        correct = 0
        total = 0
        if len(sentence) > 0 and len(sentence[0]) > 1:
            ideal_lable = [term[1] for term in sentence]
            for i in xrange(len(ideal_lable)):
                if ideal_lable[i] == predict_label[i]:
                    correct += 1
                total += 1
        return correct*1.0/total

    #####################################################
    #@func: tag a sequence using trained model
    #####################################################
    def tag(self):
        output = open(self.output_path, 'w')
        for sentence in read_data(self.test_data_path):
            word_seq = [part[0] for part in sentence]
            predict_label = self.featureModel.viterbi(word_seq)
            for (word, predict_tag) in zip(word_seq, predict_label):
                output.write(word + '\t' + predict_tag + '\n')
            output.write('\n')
