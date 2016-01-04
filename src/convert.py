# -*- coding: utf-8 -*-
'''
Created on Dec 27, 2015

@author: myue
'''

import cPickle as pickle
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def get_id(path):
    id_list = list()
    with open(path) as f:
        for line in f:
            terms = line.split(' ')
            id_list.append(terms[0].strip())
    #print id_list
    return id_list

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
            sentence.append(parts[0]+'/'+parts[1])

def convert(path,output_path, id_list):
    ofs = open(output_path, 'w')
    cnt = 0
    for sentence in read_data(path):
        tmp = ' '.join(sentence)
        ofs.write(id_list[cnt] + ' ' + tmp + '\n')
        cnt += 1
    ofs.close()

if __name__ == '__main__':
    id_list = get_id('../data/POS_test.txt')
    convert('result_esemble.txt','submit_ensemble.txt',id_list)
