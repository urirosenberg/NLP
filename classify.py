#!/usr/bin/env python
import sys
import xml.dom.minidom
import re
import pickle
import nltk
import copy
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer


"""
    This is to be run on the test data
"""

testdDoctlist = []
fileOUT1='test_solution.out'
pattern=re.compile("[^\w']|_")
stopwords = stopwords.words('english')
K=10

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

def normalizeD(document):
    sum2=0.0
    for word in document:
       sum2=sum2+(document[word]**2)
    sqr2=(sum2**0.5)
    return sqr2

def calculateSim(doc,fdist1):
    sum=0.0
    doc1 = copy.deepcopy(doc)
    del doc1['observed category']
    for keyWord in fdist1:
       if keyWord in doc1:
          sum=sum+(fdist1.freq(keyWord)*doc1[keyWord])
    xNorm = normalizeX(fdist1)
    dNorm = normalizeD(doc1)
    sim=0.0
    sim=(sum/(xNorm* dNorm))
    return sim

if len(sys.argv) != 2:
    print 'Usage: classify.py [path]filename'
    sys.exit()

st = LancasterStemmer()
fileIN = sys.argv[1]
f=open(fileIN,'r')
documentNumber=0
fdist1 = nltk.FreqDist()

similarityList=[]
fout1=open(fileOUT1,'w')
for rawDoc in f.readlines():
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
   allText= allText.lower()
   filtered_words = []
   for w in str(allText).split():
      if w not in stopwords:
         w=st.stem(w)
         filtered_words.append(w)
         fdist1.inc(w)

   #doc is a row in the matrix  
   for doc in matrix:
      docCategory=doc['observed category'].strip()
      sim=calculateSim(doc, fdist1)
      similarityList.append({'similarity': sim, 'category': docCategory})

   similarityList.sort(reverse=True)
   categoryDist = nltk.FreqDist()
   for i in xrange(K):
      categoryDist.inc(similarityList[i]['category'])
   theCategory=categoryDist.max()
   fout1.write("%s\n" % theCategory)
   
   #if documentNumber % 1000 == 0:
   #   ten3+=1
   print "processed %d (thousands) docs"%(documentNumber)

fout1.close()
