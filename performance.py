#!/usr/bin/env python
from __future__ import division
import sys



"""
    This is to be run on the test solution
"""

if len(sys.argv) != 3:
    print 'Usage: performance.py [path]input-filename [path]output-filename'
    sys.exit()

def calculateMicro(matrix):
   pDenominator=0
   rDenominator=0
   nominator=0
   for category in matrix:
      nominator+=matrix[category]['a']
      pDenominator+=(matrix[category]['a']+matrix[category]['b'])
      rDenominator+=(matrix[category]['a']+matrix[category]['c'])   
   pMicro=nominator/pDenominator
   rMicro=(nominator/rDenominator)
   return {'pMicro': pMicro, 'rMicro': rMicro}

def calculateMacro(matrix):
   pSum=0.0
   rSum=0.0
   numberOfCategories=len(matrix.keys())
   for category in matrix:
      if (matrix[category]['a']+matrix[category]['b']) != 0:
         pSum+=(matrix[category]['a'])/(matrix[category]['a']+matrix[category]['b'])
         rSum+=(matrix[category]['a'])/(matrix[category]['a']+matrix[category]['c'])
   pMacro=(numberOfCategories **(-1))*pSum
   rMacro=(numberOfCategories **(-1))*rSum
   return {'pMacro': pMacro, 'rMacro': rMacro}

resultFile = sys.argv[1]
expertFile='expert.txt'
perf=sys.argv[2]



exCat=[]
expert=open(expertFile,'r')
for cat in expert.readlines():
   exCat.append(cat.strip())
expert.close()

predCat =[]
predFile=open(resultFile,'r')
for cat in predFile.readlines():
   predCat.append(cat.strip())
predFile.close()

avialableCat=set(exCat)
performanceMatrix={}
for c in avialableCat:
   performanceMatrix[c]={'a': 0,'b': 0,'c': 0,'d': 0}


for i in range(len(exCat)):
   if exCat[i]==predCat[i]:
      performanceMatrix[exCat[i]]['a']+=1
      for c in avialableCat:
         if c != exCat[i]:
            performanceMatrix[c]['d']+=1
   else:
      performanceMatrix[exCat[i]]['c']+=1
      if predCat[i] in performanceMatrix:
         performanceMatrix[predCat[i]]['b']+=1



r= calculateMicro(performanceMatrix)
pMicro=r['pMicro']
rMicro=r['rMicro']

r= calculateMacro(performanceMatrix)
pMacro=r['pMacro']
rMacro=r['rMacro']


#print the results
fout1=open(perf,'w')
fout1.write("p-micro:: %f\n" % pMicro)
fout1.write("r-micro:: %f\n" % rMicro)
fout1.write("p-macro:: %f\n" % pMacro)
fout1.write("r-macro:: %f\n" % rMacro)         
for categ in performanceMatrix:

   if (performanceMatrix[categ]['a']+performanceMatrix[categ]['b']) != 0:
      fout1.write("category: %s\n" % categ)
      accuracy= (performanceMatrix[categ]['a']+performanceMatrix[categ]['d'])/(performanceMatrix[categ]['a']+performanceMatrix[categ]['b']+performanceMatrix[categ]['c']+performanceMatrix[categ]['d'])
      recall= (performanceMatrix[categ]['a']/(performanceMatrix[categ]['a']+performanceMatrix[categ]['c']))
      percision = performanceMatrix[categ]['a']/(performanceMatrix[categ]['a']+performanceMatrix[categ]['b'])
      fallout=(performanceMatrix[categ]['b']/(performanceMatrix[categ]['b']+performanceMatrix[categ]['d']))
      fout1.write("\taccuracy: %f\n" % accuracy)
      fout1.write("\trecall: %f\n" % recall)
      fout1.write("\tpercision: %f\n" % percision)
      fout1.write("\tfallout: %f\n" % fallout)

fout1.flush()


fout1.close()


   