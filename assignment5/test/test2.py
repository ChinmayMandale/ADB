import pandas as pd
import numpy as np
import collections
import math
from numpy import linalg as LA
import re

doc1 = 'Game of Thrones is an amazing tv series!'
doc2 = 'Game of Thrones is the best tv series!'
doc3 = 'Game of Thrones is so great'

l_doc1 = re.sub(r"[^a-zA-Z0-9]", " ", doc1.lower()).split()
l_doc2 = re.sub(r"[^a-zA-Z0-9]", " ", doc2.lower()).split()
l_doc3 = re.sub(r"[^a-zA-Z0-9]", " ", doc3.lower()).split()

wordset12 = np.union1d(l_doc1,l_doc2)
wordset =  np.union1d(wordset12,l_doc3)
print(wordset)

def calculateTF(wordset,bow):
  termfreq_diz = dict.fromkeys(wordset,0)
  counter1 =  dict(collections.Counter(bow))
  for w in bow:
    termfreq_diz[w]=counter1[w]/len(bow)
  return termfreq_diz

termfreq1_diz = calculateTF(wordset,l_doc1)
print(termfreq1_diz)
termfreq2_diz = calculateTF(wordset,l_doc2)
print(termfreq2_diz)
termfreq3_diz = calculateTF(wordset,l_doc3)
print(termfreq3_diz)
df = pd.DataFrame([termfreq1_diz,termfreq2_diz,termfreq3_diz])
df.head()