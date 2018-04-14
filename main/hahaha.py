from __future__ import division, print_function

import numpy as np
import lda
import lda.datasets
if __name__ == '__main__':
    tuple=('123','234','345')
    print(tuple.index('234'))

    # X = lda.datasets.load_reuters()
    # print("type(X): {}".format(type(X)))
    # print("shape: {}\n".format(X.shape))
    # print(X[:5, :5])
    #
    # vocab = lda.datasets.load_reuters_vocab()
    # print("type(vocab): {}".format(type(vocab)))
    # print("len(vocab): {}\n".format(len(vocab)))
    # print(vocab[:6])
    #
    # # titles for each story
    # titles = lda.datasets.load_reuters_titles()
    # print("type(titles): {}".format(type(titles)))
    # print("len(titles): {}\n".format(len(titles)))
    # print(titles[:2])  # 前两篇文章的标题
    #
    # model = lda.LDA(n_topics=20, n_iter=500, random_state=1)
    # model.fit(X)
    # topic_word = model.topic_word_
    # print("type(topic_word): {}".format(type(topic_word)))
    # print("shape: {}".format(topic_word.shape))
    #
    # doc_topic = model.doc_topic_
    # print("type(doc_topic): {}".format(type(doc_topic)))
    # print("shape: {}".format(doc_topic.shape))
    #
    # for n in range(10):
    #     topic_most_pr = doc_topic[n].argmax()
    #     b=doc_topic[n]
    #     # 选最大的两个主题
    #     topic_second_pr = np.where(b==b[topic_most_pr],0,b).argmax()
    #     print("doc: {} topic1: {} topic: {}".format(n, topic_most_pr,topic_second_pr))

