import numpy as np
import pandas as pd
import os

def get_sentiment_analysis_dataset():
    # We will need to merge all files in a big file for naives bayes.
    X_train = []
    Y_train = []
    X_test = []
    Y_test = []

    for files in os.listdir("../Data/Sentiment Analysis/train/pos"):
        text = open("../Data/Sentiment Analysis/train/pos/" + files,'r',encoding="utf8").read()
        X_train.append(text)
        Y_train.append(1)

    for files in os.listdir("../Data/Sentiment Analysis/train/neg"):
        text = open("../Data/Sentiment Analysis/train/neg/" + files,'r',encoding="utf8").read()
        X_train.append(text)
        Y_train.append(0)

    for files in os.listdir("../Data/Sentiment Analysis/test/pos"):
        text = open("../Data/Sentiment Analysis/test/pos/" + files,'r',encoding="utf8").read()
        X_test.append(text)
        Y_test.append(1)

    for files in os.listdir("../Data/Sentiment Analysis/test/neg"):
        text = open("../Data/Sentiment Analysis/test/neg/" + files,'r',encoding="utf8").read()
        X_test.append(text)
        Y_test.append(0)

    return X_train, Y_train, X_test, Y_test

