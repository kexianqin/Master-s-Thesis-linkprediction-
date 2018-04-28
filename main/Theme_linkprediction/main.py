from class_similarity_easytest import*
from sampling_train_test_split import*
from metrics import *
from Lda.dolda import *

def read_nodepair (fr):
    nodepair_set = []
    line = fr.readline().strip('\n').split('\t')
    while line != ['']:
        # print(line)
        nodepair_set.append([int(line[0]), int(line[1])])
        line = fr.readline().strip('\n').split('\t')
    fr.close()
    return nodepair_set

'''
去除每个阶段中的重复链接
'''
def delete_duplicate(link_stage):
    for a in link_stage:           #先将二维list排序 [2,5]和[5,2]是相同的
        list.sort(a)

    reList = list(set([tuple(t) for t in link_stage])) #去除重复链接
    reLink = [list(v) for v in reList]
    return reLink

if __name__ == '__main__':

    stage1=456
    stage2=20217
    stage3=15297
    stage4=19948

    openpath = open(r'../Output/total/topic_link.txt', 'r', encoding='UTF-8')

    print('-------------得出实验集，测试集，用实验集构造共现矩阵--------------')

    topic_link = read_nodepair(openpath)

    link_stage1 = topic_link[:stage1]          # [[67, 27], [67, 14]...]
    link_stage2 = topic_link[stage1:stage1+stage2]
    link_stage3 = topic_link[stage1+stage2:stage1+stage2+stage3]
    link_stage4 = topic_link[stage1+stage2+stage3:stage1+stage2+stage3+stage4]

    nodepair_set_train = delete_duplicate(link_stage3)
    nodepair_set_test = delete_duplicate(link_stage4)

    vertex_dic = create_vertex(nodepair_set_train)  # 用是实验集数据选出关键词(作为共现矩阵的行)
    print('vertex_dic :', vertex_dic)
    matrix_train = create_adjmatrix(nodepair_set_train, vertex_dic)  # 实验矩阵
    matrix_test = create_adjmatrix(nodepair_set_test, vertex_dic)  # 测试矩阵
    print('matrix_train:', matrix_train)
    print('matrix_test:', matrix_test)

    pd = Predictor()
    score = pd.RA(matrix_train)  # 看使用哪一个指标，分数以矩阵形式
    print(score)

    print('--------------算法精确度指标------------')

    auc2 = auc_score2(score, matrix_test, matrix_train, n_compare='cc')
    print('auc:', auc2)

    precision2 = precision2(score, matrix_test, matrix_train, vertex_dic, 200)
    print('precision:', precision2[0], 'correct_pair:', precision2[1], 'wrong_pair:', precision2[2])

