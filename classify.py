#!/usr/bin/env python
import sys
import xml.dom.minidom
import re
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer


"""
    This is to be run on the test data
"""

testdDoctlist = []
#fileOUT1='output.txt'
#fileOUT2='tabulate.txt'
pattern=re.compile("[^\w']|_")
stopwords = stopwords.words('english')
#bagOfWords= set()

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


def calculateSim(doc,fdist1):
    sum=0.0
    for keyWord in fdist1:
       if keyWord in doc:
          sum=sum+(fdist1.freq()
       



if len(sys.argv) != 2:
    print 'Usage: classify.py [path]filename'
    sys.exit()

st = LancasterStemmer()
fileIN = sys.argv[1]
f=open(fileIN,'r')
lineNumber=0
fdist1 = nltk.FreqDist()


for rawDoc in f.readlines():
   lineNumber+=1
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

     
   for doc in matrix:
      sim=calculateSim(doc, fdist1)
   

'''
fout1=open(fileOUT1,'w')
for item in doctlist:
  fout1.write("%s\n" % item)
fout1.close()
'''
