import numpy as np
import Data_Preprocessing.MTG_preprocessing_pure_text as datapreprocessor
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB,ComplementNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import metrics
from sklearn.linear_model import SGDClassifier
import  copy
import pandas as pd
import Data_Preprocessing.Sentiment_Preprocessing as sentiment_preprocessor
from tqdm import  tqdm

def bootstrap(x,y):
    training_set = np.hstack((x,y))
    profitable_set = [training_set[i] for i in range(len(training_set)) if training_set[i][1]['profitable'] == 1]
    unprofitable_set = [training_set[i] for i in range(len(training_set)) if training_set[i][1]['profitable'] == 0]


    for _ in range(len(unprofitable_set) - len(profitable_set)):
        training_set = np.vstack((training_set,profitable_set[np.random.randint(0,len(profitable_set))]))

    bootstrapped_set = np.hsplit(training_set,2)

    return bootstrapped_set[0], bootstrapped_set[1]

def process_mtg(data,bootstrapping=False):
    #np.random.shuffle(data)
    X_train, Y_train = np.hsplit(np.array(data[:int(len(data) * 0.8)]), 2)

    if bootstrapping == True:
        X_train, Y_train = bootstrap(X_train, Y_train)
    X_test, Y_test = np.hsplit(np.array(data[int(len(data) * 0.8):]), 2)

    Y_train = [Y_train[i][0]['profitable'] for i in range(len(Y_train))]
    Y_test = [Y_test[i][0]['profitable'] for i in range(len(Y_test))]

    return X_train.flatten(), Y_train, X_test.flatten(),Y_test

def Classify(X_train, Y_train, X_test, Y_test, reps, classifier, tf_idf=False, stop_word=None):
    total_acc = 0
    conf_matrix = np.shape((2,2))
    for _ in tqdm(range(reps)):
        # Training
        count_vect = CountVectorizer(stop_words=stop_word)

        X_train_counts = count_vect.fit_transform(list(X_train))

        if tf_idf == True:

            tfidf_transformer = TfidfTransformer()
            X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

            clf = classifier.fit(X_train_tfidf, Y_train)

        else:
            clf = classifier.fit(X_train_counts, Y_train)

        # Testing
        X_test_counts = count_vect.transform(list(X_test))

        if tf_idf == True:
            X_test_tfidf = tfidf_transformer.transform(X_test_counts)
            predictions = clf.predict(X_test_tfidf)

        else:
            predictions = clf.predict(X_test_counts)

        accuracy = len([1 for i in range(len(predictions)) if predictions[i] == Y_test[i]])/len(predictions)
        total_acc += accuracy * 100

        conf_matrix += metrics.confusion_matrix(Y_test, predictions)

    # Error analysis
    print(f"Good Negative:{conf_matrix[0][0]/(conf_matrix[0][0] + conf_matrix[0][1])}")
    print(f"Good Positive:{conf_matrix[1][1]/(conf_matrix[1][1] + conf_matrix[1][0])}")
    print(f"Wrong Negative:{conf_matrix[0][1]/(conf_matrix[0][0] + conf_matrix[0][1])}")
    print(f"Wrong Positive:{conf_matrix[1][0]/(conf_matrix[1][1] + conf_matrix[1][0])}")
    print(f"Average Naive Bayes accuracy on {reps} pass: {total_acc/reps}%")


def run_mtg_naive_bayes(reps, alphas):
    for i in alphas:
        print(f"With alpha {i}")
        data = datapreprocessor.get_useful_fields_preprocessed_data()
        X_train, Y_train, X_test, Y_test = process_mtg(data,bootstrapping=True)
        Classify(X_train, Y_train, X_test, Y_test, reps, MultinomialNB(alpha=i), tf_idf=True)


def run_sentiment_analysis_naive_bayes(reps):
    X_train, Y_train, X_test, Y_test = sentiment_preprocessor.get_sentiment_analysis_dataset()
    Classify(X_train, Y_train, X_test, Y_test, reps, MultinomialNB(alpha=6), tf_idf=True, stop_word='english')


def run_mtg_svm(reps):
    data = datapreprocessor.get_useful_fields_preprocessed_data()
    X_train, Y_train, X_test, Y_test = process_mtg(data, bootstrapping=False)
    Classify(X_train, Y_train, X_test, Y_test, reps, SGDClassifier(loss='hinge', penalty='l2',
                                                                   alpha = 1e-3, random_state = 42,
                                                                   max_iter = 5, tol = None, class_weight='balanced'), tf_idf=False)

def run_sentiment_svm(reps):
    X_train, Y_train, X_test, Y_test = sentiment_preprocessor.get_sentiment_analysis_dataset()
    Classify(X_train, Y_train, X_test, Y_test, reps,SGDClassifier(loss='hinge', penalty='l2',
                                                                   alpha = 1e-3, random_state = 42,
                                                                   max_iter = 5, tol = None), tf_idf=False)


#run_sentiment_svm(2)
#run_mtg_svm(50)
run_mtg_naive_bayes(20,[19])
#run_sentiment_analysis_naive_bayes(1)


