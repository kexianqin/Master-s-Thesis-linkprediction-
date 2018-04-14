import networkx as nx
from class_similarity_easytest import*
from sampling_train_test_split import*
from metrics import *
from Lda.dolda import *

if __name__ == '__main__':
    train="起始"
    train_threshold=3
    test="爆发"
    test_threshold=20

    file_train=r'../Output/'+train+'阶段/'+train+'顶点对(阈值为'+str(train_threshold)+').txt'
    readpath = r'../Output/'+train+'阶段.xls'  # 与Buildmatrix中设置的参数一致
    threshold = train_threshold                # 与Buildmatrix中设置的参数一致
    file_test=r'../Output/'+test+'阶段/'+test+'顶点对(阈值为'+str(test_threshold)+').txt'

    topics = 5
    top_n_words = 20


    fr_train = open(file_train, 'r', encoding='UTF-8')
    fr_test = open(file_test, 'r', encoding='UTF-8')
    print('-------------得出实验集，测试集，用实验集构造共现矩阵--------------')

    nodepair_set_train = just_read_nodepair(fr_train)
    nodepair_set_test = just_read_nodepair(fr_test)

    vertex_dic = create_vertex(nodepair_set_train)  # 用是实验集数据选出关键词(作为共现矩阵的行)
    print('vertex_dic :', vertex_dic)
    matrix_train = create_adjmatrix(nodepair_set_train, vertex_dic)  # 实验矩阵
    matrix_test = create_adjmatrix(nodepair_set_test, vertex_dic)  # 测试矩阵
    print('matrix_train:', matrix_train)
    print('matrix_test:', matrix_test)

    pd = Predictor()
    score = pd.CN(matrix_train)  # 看使用哪一个指标，分数以矩阵形式
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

    auc2 = auc_score2(score, matrix_test, matrix_train, n_compare='cc')
    print('auc:', auc2)

    precision2 = precision2(score, matrix_test, matrix_train, vertex_dic, 200)
    print('precision:', precision2[0], 'correct_pair:', precision2[1], 'wrong_pair:', precision2[2])

    print('---------------隶属主题矩阵------------------------')


    x, vocab = preprocess(readpath, threshold)
    topic_word = dolda(x, vocab, topics)
    topN(topic_word,top_n_words,vocab)
    print(link_belong(topic_word, precision2[1], vocab))

