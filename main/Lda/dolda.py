# coding=utf-8
import xlrd
import re,collections
import numpy as np
import matplotlib
import scipy
import matplotlib.pyplot as plt
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
import lda
import lda.datasets
from Comatrix.Buildmatrix import *


if __name__ == "__main__":
    readpath = r"../Output/8.8.21.xls"  #与Buildmatrix中设置的参数一致
    threshold = 5                       #与Buildmatrix中设置的参数一致
    topics=10
    top_n_words=10   #获得每个主题的前几个单词
    outputpath = r'C:\Users\Administrator\Desktop\顶点对(阈值为5).txt'

    print('------------首先是数据处理--------------------------------')
    data = readxls(readpath)
    dic = countfrequency(data)
    wf = {k: v for k, v in dic.items() if v >= threshold}
    wf_order=sorted(wf.items(), key=lambda item: item[1], reverse=True) #形如[('地震', 8942), ('九寨沟', 8104), ('四川', 6338)]
    a=[]
    b=[]
    c=[]
    for d in wf_order:
        a.append(d[0])  #临时放词
        b.append(d[1])  #临时放频率
    c.append(b)         #一维list变为二维list
    x=np.array(c)    #<class 'numpy.ndarray'> [[8942 8104 6338 ......]]
    vocab=tuple(a)             #<class 'list'> ['地震', '九寨沟', '四川', ......]
    print(wf_order)
    print('type(x):',type(x),'\n x.shape:',x.shape,'\n x:',x)
    print('type(vocab):',type(vocab),'\n vocab:',vocab)

    print('-----------------------------下面是LDA---------------------------------')
    model = lda.LDA(n_topics=topics, n_iter=500, random_state=1)
    model.fit(x)

    topic_word = model.topic_word_
    print("type(topic_word): {}".format(type(topic_word)))
    print("shape: {}".format(topic_word.shape))

    print(topic_word[:,:3])  #前三个词在每个主题的比重

    n=top_n_words            #每个主题中比重最大的前N个词
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n + 1):-1]
        print('*Topic {}\n- {}'.format(i+1, ' '.join(topic_words)))

    f, ax = plt.subplots(5, 1, figsize=(8, 6), sharex=True)  #作图
    for i, k in enumerate([0, 2, 5, 7, 9]):
        ax[i].stem(topic_word[k, :], linefmt='b-',
                   markerfmt='bo', basefmt='w-')
        ax[i].set_xlim(-50, 3000)
        ax[i].set_ylim(0, 0.08)
        ax[i].set_ylabel("Prob")
        ax[i].set_title("topic {}".format(k))
    ax[4].set_xlabel("word")
    plt.tight_layout()
    plt.show()
