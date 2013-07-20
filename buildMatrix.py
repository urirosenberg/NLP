#!/usr/bin/env python
import sys
import re
import nltk
import ast
from __future__ import division

#N= number of documents
N=20000

if len(sys.argv) != 2:
    print 'Usage: p2.py [path]filename'
    sys.exit()

tabulateFile=open('tabulate.txt','r')
collectionFreqDist=nltk.FreqDist()
collectionFreqDist =pickle.load(tabulateFile)
tabulateFile.close()

#M=the number of distinct words in the collection
M=len(collectionFreqDist)



def calculateSquareSum(docFreqDist) :
   sum=0.0
   for key in docFreqDist:
      sum=sum + (docFreqDist.freq(key)**2)
   return (sum**0.5)    



def calculateWight(word,docFreqDist,squarSum) :
    wight=0.0
    ni=collectionFreqDist.freq(word)
    logNByni=log(N/ni)
    fij= docFreqDist[word]
    wight=(fij/squarSum)* logNByni
    return wight


fileIN = sys.argv[1]
f=open(fileIN,'r')
lineNumber=0

docNumber=0


for doc in f.readlines():
   docNumber+=1
   docFreqDist = nltk.FreqDist()
   rec=ast.literal_eval(doc)
   wordList=ast.literal_eval(rec['text'])

   for word in wordList:
      docFreqDist.inc(word)
   

   squarSum=calculateSquareSum(docFreqDist)
   for word in wordList:
      wordWightInDocument=calculateWight(word,docFreqDist,squarSum)

f.close()