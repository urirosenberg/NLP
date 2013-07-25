#!/usr/bin/env python
from __future__ import division
import sys
import re
import nltk
import ast
import cPickle as pickle
import math


#N= number of documents
N=20000
fileOUT1='matrix.txt'


if len(sys.argv) != 2:
    print 'Usage: p2.py [path]filename'
    sys.exit()

tabulateFile=open('tabulate.txt','r')
#collectionFreqDist=nltk.FreqDist()
#collectionFreqDist =pickle.load(tabulateFile)
numOfDocsContainWord =pickle.load(tabulateFile)
tabulateFile.close()

#M=the number of distinct words in the collection
#M=len(collectionFreqDist)



def calculateSquareSum(docFreqDist) :
   sum=0.0
   for key in docFreqDist:
      sum=sum + (docFreqDist.freq(key)**2)
   return (sum**0.5)    



def calculateWight(word,docFreqDist,squarSum) :
    wight=0.0
    ni=numOfDocsContainWord[word]
    logNByni=math.log(N/ni)
    fij= docFreqDist.freq(word)
    wight=(fij/squarSum)* logNByni
    return wight


def normalizeDoc(document):
    sum2=0.0
    sqr2=0.0
    for word in document:
       if word != 'observed category':
          sum2+=(document[word]**2)
    sqr2=(sum2**0.5)
    return sqr2

fileIN = sys.argv[1]
f=open(fileIN,'r')
lineNumber=0

docNumber=0

matrix=[]
ten3=0

for doc in f.readlines():
   docNumber+=1
   docFreqDist = nltk.FreqDist()
   rec=ast.literal_eval(doc)
   wordList=ast.literal_eval(rec['text'])
   documentCat=rec['category']
    
   if len(wordList)!=0:
      for word in wordList:
         docFreqDist.inc(word)
   
      squarSum=calculateSquareSum(docFreqDist)
      matrixRow={}
      matrixRow['observed category']= documentCat
   

      for word in wordList:
         wordWightInDocument=calculateWight(word,docFreqDist,squarSum)
         matrixRow[word]= wordWightInDocument
   
      norm= normalizeDoc(matrixRow)
      matrixRow['normalized form']= norm
      matrix.append(matrixRow)
   if docNumber % 1000 == 0:
      ten3+=1
      print "processed %d (thousands) docs"%(ten3)
f.close()

print "dumping matrix"
fout1=open(fileOUT1,'w')
pickle.dump(matrix, fout1,protocol=2) 
fout1.close()
print "done!"