#!/usr/bin/env python
import sys
import xml.dom.minidom
import re
import pickle
import nltk
import copy
import time
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer



"""
    This is to be run on the test data
"""

testdDoctlist = []
#fileOUT1='test_solution.out'
pattern=re.compile("[^\w']|_")
punctuation = re.compile(r'[-.?!,":;()|0-9]')
stopwords = stopwords.words('english')
K=20
lmtzr = WordNetLemmatizer()

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def handleTok(tokenlist):
    texts = ""
    for token in tokenlist:
        texts += " "+ getText(token.childNodes)
    return texts


#get the matrix
matrixFile=open('matrix.txt','r')
matrix =pickle.load(matrixFile)
matrixFile.close()


def normalizeX(fdist):
    sum1=0.0
    for word in fdist:
       sum1=sum1+(fdist.freq(word)**2)
    sqr=(sum1**0.5)
    return sqr

def calculateSim(doc,fdist1, xNorm):
    sum=0.0
    doc1 = copy.deepcopy(doc)
    del doc1['observed category']
    dNorm= doc1['normalized form']
    del doc1['normalized form']
    for keyWord in fdist1:
       if keyWord in doc1:
          sum=sum+(fdist1.freq(keyWord)*doc1[keyWord])
    sim=0.0
    if (xNorm* dNorm) != 0:
       sim=(sum/(xNorm* dNorm))
    else:
       print "*****zero for doc %s"%doc1
    return sim

if len(sys.argv) != 3:
    print 'Usage: classify.py [path]input-filename output-filename'
    sys.exit()

st = LancasterStemmer()
fileIN = sys.argv[1]
fileOUT1 =sys.argv[2]
f=open(fileIN,'r')
documentNumber=0


fout1=open(fileOUT1,'wb')
for rawDoc in f.readlines():
   start = time.time()
   fdist1 = nltk.FreqDist()
   documentNumber+=1
   rawDoc = '<root>' + rawDoc + '</root>'
   dom = xml.dom.minidom.parseString(rawDoc)
   
   #get the subject
   subjectElement = dom.getElementsByTagName("subject")
   subject = handleTok(subjectElement)


   #get content
   contentElement=dom.getElementsByTagName("content")
   content = handleTok(contentElement)
   
   allText=subject+ ' ' + content
   allText=pattern.sub(' ', allText)
   allText=' '.join(allText.split())
   allText =punctuation.sub("", allText)
   allText= allText.lower()
   filtered_words = []
   for w in str(allText).split():
      if w not in stopwords:
         w=st.stem(w)
         w= lmtzr.lemmatize(w)
         filtered_words.append(w)
         fdist1.inc(w)

   #doc is a row in the matrix
   xNorm = normalizeX(fdist1)
   similarityList=[]
   matrow=0
   ten3=0
   for doc in matrix:
      matrow+=1
      docCategory=doc['observed category']
      sim=calculateSim(doc, fdist1, xNorm)
      similarityList.append({'similarity': sim, 'category': docCategory})
   
   SortedsimilarityList=[]   
   SortedsimilarityList=sorted(similarityList, key=lambda k: k['similarity'],reverse=True)
   categoryDist = nltk.FreqDist()
   for i in xrange(K):
      checkCategory=SortedsimilarityList[i]['category']
      categoryDist.inc(checkCategory)
   
   argmaxList = []
   for category in categoryDist:
      probOfCatDependDoc = (categoryDist[category]/K)
      argmaxList.append({'probability': probOfCatDependDoc, 'category': category})
   

   #theCategory=categoryDist.max()
   theCategory=max(argmaxList, key=lambda k: k['probability'])['category'].strip()
   fout1.write("%s\n" % theCategory)
   fout1.flush()

   #if documentNumber % 1000 == 0:
   #   ten3+=1
   end = time.time()
   docProcessingTime= end - start
   print "processed %d docs. Processing time: %d (seconds)"%(documentNumber,docProcessingTime)

fout1.close()
