#!/usr/bin/env python
import sys
import re
import math
charRegex = re.compile('[a-zA-Z]')
totalChars=0
if len(sys.argv) != 2:
    print 'Usage: Ex1_question4.py [path]filename'
    sys.exit()

fileIN = sys.argv[1]
f=open(fileIN,'r')
chars={}

for line in f.readlines():
   for i in line:   
      if i in chars:
         totalChars+=1
         chars[i]+=1
      else:
         if charRegex.match(i):
            totalChars+=1
            chars[i]=1
dist={}
entropy=0.0
for k in chars.keys():
   dist[k]=chars[k]/(totalChars * 1.0)
   entropy=entropy+(dist[k]*math.log(dist[k],2))
   print (k,chars[k],dist[k])
entropy = -entropy
print "The entropy is: " + repr(entropy)
