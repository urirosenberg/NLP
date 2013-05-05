#!/usr/bin/env python
import nltk
from nltk import bigrams
from nltk import trigrams
from nltk.probability import LidstoneProbDist  
from nltk.model import NgramModel    

with open('./austen/persuasion.txt', 'r') as training_file:
    raw = training_file.read() 
tokens = nltk.word_tokenize(raw)

with open('./austen/sense_and_sensibility.txt', 'r') as test_file:
    test = test_file.read()
test_list = nltk.word_tokenize(test)

estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
model = NgramModel(3, tokens,True,False,estimator)  
tri=model.entropy(test_list)
print "tri-gram: " + str(tri)

model = NgramModel(2, tokens,True,False,estimator)  
bi=model.entropy(test_list)
print "bi-gram: " + str(bi)

