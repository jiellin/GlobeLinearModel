# -*- coding: utf-8 -*-
'''
Created on Dec 27, 2015

@author: jielin

@description:This module contains score computing and feature vector weighting
'''
import cPickle as pickle
from collections import defaultdict

class FeatureVectorWeight(object):
    def __init__(self, featrue_template_list, label_list, model_params = None):
        self.params = defaultdict(lambda: 0)
        self.feature = featrue_template_list
        self.label_list = label_list
        if model_params:
            #with open(model_params) as f:
            #    self.params = pickle.load(f)
            with open(model_params) as f:
                for tags in f:
                    tags = tags.split()
                    self.params[tags[0]] = float(tags[1])

    def __getitem__(self, key):
        return sum([self.params[f(*key)] for f in self.feature])

    def _gradientDecent(self, key, value):
        for f in self.feature:
            nums = f(*key)
            if nums:
                self.params[nums] += value

    def _init_matrix(self, seq_len, label_num):
        matrix = list()
        for i in xrange(seq_len):
            tmp_list = [0 for j in xrange(label_num)]
            matrix.append(tmp_list)
        return matrix

    ###################################################
    #@func:               update feature vector weight
    #@param word_seq:     oberserved data sequence
    #@param ideal_label:  precise pos-tag sequence
    #@param predict_label:predict pos-tag sequence
    ###################################################
    def update(self, word_seq, ideal_label, predict_label):
        sample_num = len(word_seq)
        ideal_label = ['*'] + ideal_label
        predict_label = ['*'] + predict_label
        for i in xrange(1, sample_num + 1):
            if ideal_label[i-1] != predict_label[i-1] or ideal_label[i] != predict_label[i]:
                self._gradientDecent([[ideal_label[i-1], ideal_label[i]], word_seq, i-1], 1)
                self._gradientDecent([[predict_label[i-1], predict_label[i]], word_seq, i-1], -1)

    ###################################################
    #@func:  veterbi algorithm return predict pos-tag sequence
    ###################################################
    def viterbi(self, word_seq):
        getMax = lambda pair: max(pair, key = lambda x: x[1])
        seq_len = len(word_seq)
        label_num = len(self.label_list)
        #init the matrix
        matrix = self._init_matrix(seq_len, label_num)
        path = self._init_matrix(seq_len, label_num)
        matrix[0] = [self[[['*', self.label_list[each]], word_seq, 0]] for each in xrange(label_num)]
        # dp
        for i in xrange(1, seq_len):
            for j in xrange(label_num):
                pre_possible_values = list()
                for k in xrange(label_num):
                    tmp = (k, matrix[i-1][k] + self[[[self.label_list[k], self.label_list[j]], word_seq, i]])
                    pre_possible_values.append(tmp)
                path[i][j], matrix[i][j] = getMax(pre_possible_values)

        # path stores the pos-tag labels
        predict_label = [getMax([(j, matrix[seq_len-1][j]) for j in xrange(label_num)])[0]]
        for i in xrange(seq_len - 1):
            predict_label.append(path[seq_len - i - 1][predict_label[-1]])
        predict_label.reverse()
        return [self.label_list[index] for index in predict_label]
