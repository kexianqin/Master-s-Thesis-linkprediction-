import time
import xlrd
from Comatrix.Buildmatrix import *
import numpy as np
import lda

def log(func):
    def wrapper(*args, **kwargs):
        now_time = str(time.strftime('%Y-%m-%d %X', time.localtime()))
        print('------------------------------------------------')
        print('%s %s called' % (now_time, func.__name__))
        print('Document:%s' % func.__doc__)
        print('%s returns:' % func.__name__)
        re = func(*args, **kwargs)
        p(re)
        return re
    return wrapper

'''
输入分词后的xls文件、词阈值，返回截选的词集（vocab）和每条微博数据（data）
'''
def preprocess(readpath,threshold):
    data = readxls(readpath)  # data形如['四川/九寨沟/', '乐观/四川人/小震/',...]'''
    dic = countfrequency(data)
    wf = {k: v for k, v in dic.items() if v >= threshold}
    wf_order = sorted(wf.items(), key=lambda item: item[1],reverse=True)  # 形如[('地震', 8942), ('九寨沟', 8104), ('四川', 6338)]
    a = []
    for d in wf_order:
        a.append(d[0])  # 临时放词
    vocab = tuple(a)    # 形如 ("地震","九寨沟","四川"....)
    return vocab,data

@log
def get_doc_word_matrix(vocab,data):
    row = len(data)
    column=len(vocab)
    # matrix = [['' for j in range(column)] for i in range(row)] #建立矩阵
    matrix=np.zeros([row,column],int)

    n=0
    for txt in data:
        keyfir = txt.split('/')
        for w in keyfir:
            if w in vocab:
                index=vocab.index(w)
                matrix[n,index]+=1
        n+=1
        # print(n)
    return matrix

def dolda(matrix,vocab,topics):
    model = lda.LDA(n_topics=topics, n_iter=200, random_state=1)
    model.fit(matrix)

    topic_word = model.topic_word_  #主题——词 分布
    print("type(topic_word): {}".format(type(topic_word)))
    print("shape: {}".format(topic_word.shape))

    doc_topic = model.doc_topic_    #文档——主题 分布
    print("type(doc_topic): {}".format(type(doc_topic)))
    print("shape: {}".format(doc_topic.shape))

    return topic_word,doc_topic

@log
def showVocab(vocab):
    '''输出关键词及频数'''
    vocabtxt = ''
    for w in vocab:
        vocabtxt += w +'\n'
    return vocabtxt

@log
def showTopicLink(topic_link):
    linktxt = ''
    for a in topic_link:
        linktxt += str(a[0]) + '\t' + str(a[1]) + '\n'
    return linktxt


if __name__ == "__main__":
    topics = 80   #设定的主题数
    top_n_words = 20    #计算各个主题top_n个单词
    outputpath=r"../Output/total/"  #文件输出地址

    vocab1, data1 = preprocess(r"../Output/起始阶段.xls",3)
    vocab2, data2 = preprocess(r"../Output/爆发阶段.xls", 20)
    vocab3, data3 = preprocess(r"../Output/衰退阶段.xls", 20)
    vocab4, data4 = preprocess(r"../Output/平息阶段.xls", 40)

    vocab=(tuple(set(vocab1)|set(vocab2)|set(vocab3)|set(vocab4))) #所有微博的词集
    data= data1+data2+data3+data4                                  #所有微博的数据集
    print("vocab:{} data:{}".format(len(vocab),len(data)))

    vocabtxt=showVocab(vocab)                                      #输出所有微博的词集
    wryer(outputpath+'vocab.txt',vocabtxt)

    matrix=get_doc_word_matrix(vocab,data)                         #微博(data)-词(vocab) 矩阵

    topic_word,doc_topic = dolda(matrix, vocab, topics)            #lda,生成两个矩阵

    topic_link = []                                                #主题共现情况 [[2,3],[2,4]...]
    for n in range(len(doc_topic)):
        topic_most_pr = doc_topic[n].argmax()
        b=doc_topic[n]
        # 选最大的两个主题
        topic_second_pr = np.where(b==b[topic_most_pr],0,b).argmax()
        print("doc: {} topic1: {} topic2: {}".format(n, topic_most_pr,topic_second_pr))
        topic_link.append([topic_most_pr,topic_second_pr])

    linktxt=showTopicLink(topic_link)                              # 输出共现主题对
    wryer(outputpath + 'topic_link.txt', linktxt)

    n = top_n_words                                                # 每个主题中比重最大的前N个词
    topicwordtxt=''
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n + 1):-1]
        print('*Topic {}\n- {}'.format(i, ' '.join(topic_words)))
        topicwordtxt += '*Topic {}\n- {}'.format(i, ' '.join(topic_words)) +'\n'
    wryer(outputpath + 'topic_word.txt', topicwordtxt)


