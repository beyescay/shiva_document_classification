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


def vectorize_train_data(data_list, train_test_flag, mindf=4, maxdf=0.8):
    """
    This method reads the list of reviews then converts it to a csr_matrix using sklearns built-in function
    we also remove the stopwords from every review using nltk's list of stopwords

    :param data_list: list of reviews
    :return: csr_matrix containing tf-idf values of the reviews
    """
    stopword_list = stopwords.words('english')
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=mindf, max_df=maxdf, sublinear_tf=True, use_idf=True,
                                 stop_words=stopword_list)

    data_vector = vectorizer.fit_transform(data_list)

    return data_vector, vectorizer


def vectorize_test_data(test_data_list, vectorizer):
    """

    :param test_data_list:
    :param vectorizer:
    :return:
    """
    data_vector = vectorizer.transform(test_data_list)

    return data_vector


def classify(test_vector, train_vector, train_labels, strategy='linear'):
    """
    This method takes in the train and test vectors containing tf-idf scores , train_labels and performs classification
    using SVM(Support Vector Machine, and uses a linear kernel for the strategy) and returns a list of predicted labels
    for the test data.

    :param      test_vector : csr matrix containing tf-idf scores for the test_data
    :param      train_vector: csr matrix containing tf-idf scores for the train_data
    :param      train_labels: list of corresponding labels for the train_data_vector
    :param      strategy    : The type of Kernel to use for a Support Vector Machine

    :return:  A list of predicted labels for the test data
    """
    classifier_linear = svm.SVC(kernel=strategy, C=0.8)
    classifier_linear.fit(train_vector, train_labels)
    prediction_svm_linear = classifier_linear.predict(test_vector)
    return prediction_svm_linear


labelIndPair = {}
count = 0
train_data_cumm_list = []
train_label_cumm_list = []

test_data_cumm_list = []
test_label_cumm_list = []


for idx, i in enumerate(['comp', 'sport', 'politics', 'rec']):
    labelIndPair[count] = i
    train_data, train_label = read_data(os.path.join("data/training/", i, "{}.txt".format(i)),
                                        labl=idx)

    for word in train_data:
        train_data_cumm_list.append(word)

    for label in train_label:
        train_label_cumm_list.append(label)

train_vector, vectorizer = vectorize_train_data(data_list=train_data_cumm_list, train_test_flag="train")

predicted_group_label = []
actual_group_label = []

for idx, i in enumerate(['comp', 'sport', 'politics', 'rec']):

    ith_test_data_dir = os.path.join("data/testing/", i)

    for root, dirs, files in os.walk(ith_test_data_dir):
        if len(files) > 0:
            for test_file in files:
                test_file_path = os.path.join(root, test_file)
                test_data = read_data(test_file_path, flag='test')
                test_vector = vectorize_test_data(test_data_list=test_data, vectorizer=vectorizer)
                predicted_labels = classify(test_vector=test_vector, train_vector=train_vector, train_labels=train_label, strategy="linear")
                predicted_group = max(predicted_labels)
                predicted_group_label.append(predicted_group)
                actual_group_label.append(idx)


print("Accuracy: {}".format(sum(predicted_group_label == actual_group_label)/len(predicted_group_label)))
