"""
A simple script that demonstrates how we classify textual data with sklearn.

"""

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.metrics import accuracy_score

import csv
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn import svm
import string
import os
from io import open

def read_data(fname, labl = "none", flag = 'Train'):
    """
    Reads and outputs in as text, label value.
    """
    stopword_list = stopwords.words('english')
    words = []
    labels = []
    fin = open(fname, 'r', encoding="ISO-8859-1")

    if flag == 'Train':

        for w in fin.read().lower().split():
            if w not in stopword_list:
                words.append(w.lower())    
                labels.append(str(labl))
        fin.close()
        return words,labels
    else:

        for w in fin.read().lower().split():
            words.append(w.lower().strip(string.punctuation))  
        fin.close()
        return words


for idx, i in enumerate(['politics']):
#     labelIndPair[count] = i
    train_data, train_label = read_data(os.path.join("data/training/", i, "{}.txt".format(i)),
                                        labl=idx)


from collections import Counter
counts = Counter(train_data)
# print(counts)

dict_words = {}


for i in ['computer','mac','program','software','file','image','windows','drive','disk']:
    dict_words[i] = 'comp'
    
for i in ['hockey','games','players','play','file','team','game','games','teams','cup']:
    dict_words[i] = 'sport'

for i in ['government','turkish','law','political','war','public','states','israel','guns','rights']:
    dict_words[i] = 'politics'    


for idx, i in enumerate(['comp', 'sport', 'politics', 'rec']):

    ith_test_data_dir = os.path.join("data/testing/", i)

    for root, dirs, files in os.walk(ith_test_data_dir):
        if len(files) > 0:
            for test_file in files:
                test_file_path = os.path.join(root, test_file)


test_data = read_data(test_file_path, flag='test')
test_counts = Counter(test_data)
res = "none"
for i in test_counts:
    try:
        res = dict_words[i]
        break
    except:
        pass
if res == "none":
    print("rec")
print(res)
