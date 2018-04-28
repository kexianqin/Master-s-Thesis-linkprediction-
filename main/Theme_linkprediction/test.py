# -*- coding: UTF-8-*-
import numpy
import math
import string
import matplotlib.pyplot as plt
import re
from Theme_linkprediction.tool import *

def f_testset_word_count(testset):                                     #测试集的词数统计
    '''reture the sum of words in testset which is the denominator of the formula of Perplexity'''
    testset_clean=testset.split('/')
    return (len(testset_clean)-testset.count("\n"))

'''
wordlist应该是形如['地震',0.02,'四川',0.003,'祈福',0.006,'地震',0.07]
'''
def dictionary_found(wordlist):               #对模型训练出来的词转换成一个词为KEY,概率为值的字典。
    word_dictionary1={}
    for i in range(len(wordlist)):
        if i%2==0:
            if word_dictionary1.has_key(wordlist[i])==True:
                word_probability=word_dictionary1.get(wordlist[i])
                word_probability=float(word_probability)+float(wordlist[i+1])
                word_dictionary1.update({wordlist[i]:word_probability})
            else:
                word_dictionary1.update({wordlist[i]:wordlist[i+1]})
        else:
            pass
    return word_dictionary1

if __name__ == "__main__":
    f1 = open(r'C:\Users\Administrator\Desktop\test.txt', 'r')  # 测试集目录
    testset = f1.read()
    testset_word_count = f_testset_word_count(testset)  # call the function to count the sum-words in testset
    print(testset_word_count)

    threshold = 1
    readpath = r'C:\Users\Administrator\Desktop\test1.xlsx'

    vocab,matrix = preprocess(readpath, threshold)

    print(vocab)
    print(matrix)

    model = lda.LDA(n_topics=2, n_iter=300, random_state=1)
    model.fit(matrix)
    topic_word = model.topic_word_
    print(topic_word)

    doc_topic = model.doc_topic_
    print(doc_topic)
