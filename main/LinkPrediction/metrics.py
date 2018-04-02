import numpy as np
import random


def precision(preds, matrix_test, l):
    '''
    :param preds:使用networkx中方法返回的一个generator
    :l:选前l个预测概率最大的边
    '''
    a = np.array(list(preds))
    b = a[np.lexsort(-a.T)][0:l]
    # b 形如，前两位是顶点，最后一位是分数：
    # [[0.          3.          0.66666667]
    #  [2.          4.          0.5]]
    linked_num = 0
    for i in range(l):
        if matrix_test[int(b[i][0])][int(b[i][1])] == 1:
            linked_num += 1
    precision = linked_num / l
    return precision


def precision2(matrix_score, matrix_test, matrix_train,vertex_dic, l):
    '''
    :param l: 选前l个预测概率最大的边
    :return: 一个list，list[0]是精准度，list[1]是这前l条边中预测正确的词对，list[2]是预测错误的
    '''
    linked_num = 0
    correct_pair=[]  #用来存放预测正确的边
    wrong_pair=[]    #用来存放预测错误的边
    new_dict = {v: k for k, v in vertex_dic.items()}  #将边还原为关键词

    test_pair = []
    p = 1
    for i in range(0, len(matrix_test)):
        for j in range(0, p):
            if i != j and matrix_train[i][j] != 1:  # 去掉训练集中已经存在的边
                test_pair.append([i, j, matrix_score[i, j]])
        p += 1

    a = np.array(test_pair)
    b = a[np.lexsort(-a.T)][0:l]
    for i in range(l):
        if matrix_test[int(b[i][0])][int(b[i][1])] == 1:
            correct_pair.append([new_dict[int(b[i][0])], new_dict[int(b[i][1])],b[i][2]])
            linked_num += 1
        else:
            wrong_pair.append([new_dict[int(b[i][0])], new_dict[int(b[i][1])],b[i][2]])
    precision = linked_num / l
    return [precision,correct_pair,wrong_pair]

def auc_score(preds,matrix_test, matrix_train, n_compare=10):
    if type(n_compare) == int:
        if len(matrix_test[0]) < 2:
            raise Exception("Invalid ndim!", matrix_train.ndim)
        elif len(matrix_test[0]) < 10:
            n_compare = len(matrix_test[0])
    else:
        if n_compare != 'cc':
            raise Exception("Invalid n_compare!", n_compare)

    list_score = np.array(list(preds))
    unlinked_pair = []
    linked_pair = []
    # print(matrix_score[0][0])
    l = 1
    for i in range(0,len(list_score)):
        if matrix_test[int(list_score[i][0])][int(list_score[i][1])] ==1:
            linked_pair.append(list_score[i][2])
        elif matrix_test[int(list_score[i][0])][int(list_score[i][1])] ==0:
            unlinked_pair.append(list_score[i][2])
        else:
            raise Exception("Invalid connection!", matrix_test[int(list_score[i][0])][int(list_score[i][1])])

    auc = 0.0
    if n_compare == 'cc':
        frequency = min(len(unlinked_pair), len(linked_pair))
    else:
        frequency = n_compare
    for fre in range(0, frequency):
        unlinked_score = float(unlinked_pair[random.randint(0, frequency - 1)])  # 为什么是(0, frequency - 1)
        linked_score = float(linked_pair[random.randint(0, frequency - 1)])
        if linked_score > unlinked_score:
            auc += 1.0
        elif linked_score == unlinked_score:
            auc += 0.5
    auc = auc / frequency
    return auc

def auc_score2(matrix_score, matrix_test, matrix_train, n_compare=10):

    '''
            根据测试顶点的邻接矩阵，分出发生链接与没有发生链接的集合
            n_compare: int,'cc' ，计算auc比较次数，当该参数输入为int型时为比较次数，
            当输入为cc时以为Complete comparison，完全比较，默认参数为10
    '''
    if type(n_compare) == int:
        if len(matrix_test[0]) < 2:
            raise Exception("Invalid ndim!", matrix_train.ndim)
        elif len(matrix_test[0]) < 10:
            n_compare = len(matrix_test[0])
    else:
        if n_compare != 'cc':
            raise Exception("Invalid n_compare!", n_compare)
    unlinked_pair = []
    linked_pair = []
    # print(matrix_score[0][0])
    l = 1
    for i in range(0, len(matrix_test)):
        for j in range(0, l):
            if i != j and matrix_train[i][j] != 1:  # 去掉训练集中已经存在的边
                if matrix_test[i][j] == 1:
                    linked_pair.append(matrix_score[i, j])
                elif matrix_test[i][j] == 0:
                    unlinked_pair.append(matrix_score[i, j])
                else:
                    raise Exception("Invalid connection!", matrix_test[i][j])
        l += 1
    auc = 0.0
    if n_compare == 'cc':
        frequency = min(len(unlinked_pair), len(linked_pair))
    else:
        frequency = n_compare
    for fre in range(0, frequency):
        unlinked_score = float(unlinked_pair[random.randint(0, frequency - 1)])  #为什么是(0, frequency - 1)
        linked_score = float(linked_pair[random.randint(0, frequency - 1)])
        if linked_score > unlinked_score:
            auc += 1.0
        elif linked_score == unlinked_score:
            auc += 0.5
    auc = auc / frequency
    return auc

def manytimes(x,f,*args, **kwargs): #x为运行次数.f为评价函数
    # 例如 avg=manytimes(20,auc_score,preds, matrix_test, matrix_train, n_compare='cc')
    avg=0
    for i in range(x):
        avg += f(*args, **kwargs)
    return avg/x