

import re
from bs4 import BeautifulSoup
import pickle
from operator import itemgetter
import numpy as np
import ast
from scipy import spatial


def decontracted(phrase):
    # specific
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase


def tokenization(sentance) :
    sentance = re.sub(r"http\S+", "", sentance)
    sentance = BeautifulSoup(sentance, 'lxml').get_text()
    sentance = decontracted(sentance)
    sentance = ' '.join(e.lower() for e in sentance.split() )
    sentance.strip()
    return sentance

def word_embeddings(vector,keys ,sent) :
    
    sent_vec = np.zeros(100) 
    cnt_words =0 
    for word in sent: 
        if word in keys:
            vec = word
            sent_vec += vector[vec]
            cnt_words += 1
    if cnt_words != 0:
        sent_vec /= cnt_words
    return sent_vec
