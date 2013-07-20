#!/usr/bin/env python
import sys
import xml.dom.minidom
import re
import pickle
import nltk
from nltk.corpus import stopwords


"""
    This is pre processing the doc
"""

doctlist = []
fileOUT1='output.txt'
fileOUT2='tabulate.txt'
pattern=re.compile("[^\w']|_")
stopwords = stopwords.words('english')
bagOfWords= set()

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



if len(sys.argv) != 2:
    print 'Usage: p1.py [path]filename'
    sys.exit()

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
   
   #get category
   categoryElement=dom.getElementsByTagName("maincat")
   category = handleTok(categoryElement)

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
         filtered_words.append(w)
         #bagOfWords.add(w)
         fdist1.inc(w)

   doctlist.append({'text': str(filtered_words), 'category': str(category)})
   if lineNumber % 1000 == 0:
      print "processed 1000 lines"

fout1=open(fileOUT1,'w')
for item in doctlist:
  fout1.write("%s\n" % item)
fout1.close()

fout2=open(fileOUT2,'w')
pickle.dump(fdist1, fout2)
fout2.close()
