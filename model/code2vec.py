#!/usr/bin/env python

import _pickle as pickle
import tensorflow as tf
from util.pretty_print import log,success,error

def init(train_path):
    # train_path: path to training data

    # Load dict
    with open('{}.dict.c2s'.format(train_path),'rb') as file:
        subtoken_to_count = pickle.load(file)
        node_to_count = pickle.load(file)
        target_to_count = pickle.load(file)
        max_contexts = pickle.load(file)
        num_training_examples = pickle.load(file)

        success('Dictionaries loaded.')



if __name__ == '__main__':
    init()
    train()
