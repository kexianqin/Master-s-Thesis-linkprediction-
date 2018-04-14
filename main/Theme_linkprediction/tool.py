import time
import xlrd
from Comatrix.Buildmatrix import *
import numpy as np
from Lda.dolda import *

def preprocess(readpath,threshold):
    data = readxls(readpath)  # data形如['四川/九寨沟/', '乐观/四川人/小震/',...]'''
    dic = countfrequency(data)
    wf = {k: v for k, v in dic.items() if v >= threshold}
    wf_order = sorted(wf.items(), key=lambda item: item[1],reverse=True)  # 形如[('地震', 8942), ('九寨沟', 8104), ('四川', 6338)]
    a = []
    for d in wf_order:
        a.append(d[0])  # 临时放词
    vocab = tuple(a)

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
        print(n)

    return vocab,matrix



if __name__ == "__main__":
    stage = '爆发'
    threshold = 20

    readpath = r"../Output/" + stage + "阶段.xls"

    vocab=preprocess(readpath,threshold)[0]
    matrix=preprocess(readpath,threshold)[1]

    print(vocab)
    print(matrix)

    topic_word = dolda(matrix, vocab, 20)
    print(topic_word[:, :3])  # 前三个词在每个主题的比重

