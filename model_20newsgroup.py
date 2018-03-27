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
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier


def read_data(fname, labl="none", flag='Train'):
    """
    Reads and outputs in as text, label value.
    """
    stopword_list = stopwords.words('english')
    words = []
    labels = []
    fin = open(fname, 'r', encoding="ISO-8859-1")

    if flag == 'Train':

        for w in fin.read().lower().strip().split():
            if w not in stopword_list and w != "":
                words.append(w.lower())
                labels.append(str(labl))
        fin.close()
        return words, labels
    else:
        for w in fin.read().lower().strip().split():
            if w not in stopword_list and w != "":
                words.append(w.lower().strip(string.punctuation))
        fin.close()
        return words


def vectorize_train_data(data_list, train_test_flag, mindf=0.01, maxdf=0.7):
    """
    This method reads the list of reviews then converts it to a csr_matrix using sklearns built-in function
    we also remove the stopwords from every review using nltk's list of stopwords

    :param data_list: list of reviews
    :return: csr_matrix containing tf-idf values of the reviews
    """
    stopword_list = stopwords.words('english')
    vectorizer = TfidfVectorizer(max_df=maxdf, sublinear_tf=True,
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


def fit_model(train_vector, train_labels, strategy='linear'):
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
    classifier_linear = RidgeClassifier(tol=1e-2, solver="lsqr")
    classifier_linear.fit(train_vector, train_labels)

    return classifier_linear


def classify(test_vector, classifier_linear):
    prediction_svm_linear = classifier_linear.predict(test_vector)
    return prediction_svm_linear


def main():
    labelIndPair = {}
    train_data_cumm_list = []
    train_label_cumm_list = []

    news_groups = ['comp', 'sport', 'politics', 'rec']

    for idx, i in enumerate(news_groups):
        labelIndPair[idx] = i
        train_data, train_label = read_data(os.path.join("data/training/", i, "{}.txt".format(i)),
                                            labl=idx)

        for word in train_data:
            train_data_cumm_list.append(word)

        for label in train_label:
            train_label_cumm_list.append(label)

    train_vector, vectorizer = vectorize_train_data(data_list=train_data_cumm_list, train_test_flag="train")

    print("\nTraining...")
    svm_model = fit_model(train_vector=train_vector, train_labels=train_label_cumm_list, strategy="linear")
    print("Finished training\n")

    predicted_group_label = []
    actual_group_label = []

    print("Predicting for test data\n")
    for idx, i in enumerate(news_groups):

        ith_test_data_dir = os.path.join("data/testing/", i)

        for root, dirs, files in os.walk(ith_test_data_dir):
            if len(files) > 0:
                for test_file in files:

                    test_file_path = os.path.join(root, test_file)
                    print("Predicting for {}".format(test_file))
                    test_data = read_data(test_file_path, flag='test')
                    if len(test_data) == 0:
                        print("Empty file. So skipping")
                        continue
                    test_vector = vectorize_test_data(test_data_list=test_data, vectorizer=vectorizer)
                    predicted_labels = classify(test_vector=test_vector, classifier_linear=svm_model)
                    current_test_data_label_count = {}
                    for predicted_label in predicted_labels:
                        if predicted_label in current_test_data_label_count:
                            current_test_data_label_count[predicted_label] += 1
                        else:
                            current_test_data_label_count[predicted_label] = 1
                    predicted_group = max(current_test_data_label_count, key=current_test_data_label_count.get)
                    predicted_group_label.append(int(predicted_group))
                    # print(current_test_data_label_count)
                    # print("Predicted label: {}".format(labelIndPair[int(predicted_group)]))
                    # print("Actual label: {}".format(labelIndPair[idx]))
                    actual_group_label.append(idx)

    print("\n Testing accuracy: {}".format(100.0*sum(1.0 for x, y in zip(predicted_group_label, actual_group_label) if x == y) / float(
        len(predicted_group_label))))
