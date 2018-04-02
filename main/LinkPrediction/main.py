import networkx as nx
from class_similarity_easytest import*
from sampling_train_test_split import*
from metrics import *


if __name__ == '__main__':
    readpath=r'C:\Users\Administrator\Desktop\顶点对(阈值为5).txt' #文件地址

    fr = open(readpath, 'r', encoding='UTF-8')

    print('-------------得出实验集，测试集，用实验集构造共现矩阵--------------')
    nodepair_sets = train_test_split(fr, 3)   #随机划分实验集以及测试集，3是分三段
    nodepair_set_train = nodepair_sets[0]+nodepair_sets[1]
    nodepair_set_test = nodepair_sets[2]
    print('nodepair_set_train :', nodepair_set_train)
    print('nodepair_set_test :', nodepair_set_test)

    vertex_dic = create_vertex(nodepair_set_train)  #用是实验集数据选出关键词(作为共现矩阵的行)
    print('vertex_dic :',vertex_dic)
    matrix_train = create_adjmatrix(nodepair_set_train, vertex_dic) #实验矩阵
    matrix_test = create_adjmatrix(nodepair_set_test, vertex_dic)   #测试矩阵
    print('matrix_train:',matrix_train)
    print('matrix_test:',matrix_test)

    pd=Predictor()
    score=pd.CN(matrix_train)      #看使用哪一个指标，分数以矩阵形式
    print(score)

    print('-------------networkx.algorithms.link_prediction--------------')
    # graph = nx.from_numpy_matrix(matrix_train)
    # nx.draw_networkx(graph)
    # plt.show()
    # preds = nx.jaccard_coefficient(graph) #看使用哪一个指标，分数以generator形式
    # print(type(preds))
    # preds=list(preds)
    # for u, v, p in preds:
    #     print('(%d, %d) -> %.8f' % (u, v, p))  #形如 (6, 10) -> 0.57142857

    print('--------------算法精确度指标------------')

    auc2=auc_score2(score, matrix_test, matrix_train, n_compare='cc')
    print('auc:', auc2)

    precision2=precision2(score, matrix_test, matrix_train,vertex_dic,200)
    print('precision:',precision2[0],'correct_pair:',precision2[1],'wrong_pair:',precision2[2])