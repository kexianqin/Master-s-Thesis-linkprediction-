from sampling_train_test_split import *
import numpy.matlib
import networkx as nx
import matplotlib.pyplot as plt
import math

class Predictor(object):
    """docstring for  similarity"""

    def fit(self, train_adj):
        "矩阵维度大于1"
        train = np.matrix(train_adj)
        if train.ndim < 2:
            raise Exception("Invalid ndim!", train.ndim)
        if train.size < 2:
            raise Exception("Invalid size!", train.size)
        if train.shape[0] != train.shape[1]:
            raise Exception("Invalid shape!", train.shape)

    """
            CommonNeighbors 求交集
    """
    def CN(self, train_adj):
        Predictor.fit(self, train_adj)
        train_adj = np.matrix(train_adj)

        return train_adj * train_adj

    """
            Jaccard 两顶点邻居的交集与并集之比
    """
    def JC(self, train_adj):
        Predictor.fit(self, train_adj)
        train_adj = np.matrix(train_adj)
        numerator = train_adj * train_adj
        deg0 = np.matlib.repmat(train_adj.sum(0), len(train_adj), 1)
        deg1 = np.matlib.repmat(train_adj.sum(1), 1, len(train_adj))
        denominator = deg0 + deg1 - numerator
        sim = numerator / denominator
        sim[np.isnan(sim)] = 0
        sim[np.isinf(sim)] = 0
        return sim

    """
            Adamic/Adar (Frequency-Weighted Common Neighbors)
    """
    def AA(self,train):
        Predictor.fit(self, train)
        dim = train.shape[0]
        neig = [set() for i in range(dim)]
        for i in range(dim):
            for j in range(i + 1, dim):
                if train[i][j]:
                    neig[i].add(j)
                    neig[j].add(i)

        sim = np.zeros((dim, dim), dtype=np.float)
        for i in range(dim):
            for j in range(i + 1, dim):
                for z in neig[i] & neig[j]:
                    sim[i][j] += (1.0 / math.log(len(neig[z])))
                sim[j][i] = sim[i][j]
        return sim

    """      
            Katz (Exponentially Damped Path Counts)
    """
    def KZ(self,train, beta):
        Predictor.fit(self, train)
        dim = train.shape[0]
        sim = np.linalg.inv(np.eye(dim, dtype=np.float) - beta * train) - np.eye(dim, dtype=np.float)
        return sim

    """
            Preferential Attachment
    """
    def PA(self,train):
        Predictor.fit(self, train)
        dim = train.shape[0]
        neig = [set() for i in range(dim)]
        for i in range(dim):
            for j in range(i + 1, dim):
                if train[i][j]:
                    neig[i].add(j)
                    neig[j].add(i)

        sim = np.zeros((dim, dim), dtype=np.int)
        for i in range(dim):
            for j in range(i + 1, dim):
                sim[i][j] = sim[j][i] = len(neig[i]) * len(neig[j])
        return sim

    """
            Resource Allocation
    """
    def RA(self,train):
        Predictor.fit(self, train)
        dim = train.shape[0]
        neig = [set() for i in range(dim)]
        for i in range(dim):
            for j in range(i + 1, dim):
                if train[i][j]:
                    neig[i].add(j)
                    neig[j].add(i)

        sim = np.zeros((dim, dim), dtype=np.float)
        for i in range(dim):
            for j in range(i + 1, dim):
                for z in neig[i] & neig[j]:
                    sim[i][j] += (1.0 / len(neig[z]))
                sim[j][i] = sim[i][j]
        return sim




if __name__ == '__main__':

    nodepair_set = [[0, 1], [0, 2], [1, 2], [1, 5], [1, 3], [3, 4], [3, 5], [3, 4], [2, 5], [2, 0]]

    pd = Predictor()
    vertex_dic = create_vertex(nodepair_set)

    matrix_train = create_adjmatrix(nodepair_set, vertex_dic)

    print(vertex_dic)
    print(matrix_train)

    print(pd.RA(matrix_train))

    print('--------------------------')

    # graph = nx.from_numpy_matrix(matrix_train)
    # nx.draw_networkx(graph)
    # plt.show()

    # preds = nx.jaccard_coefficient(graph)
    # print(type(preds))
    # for u, v, p in preds:
    #     print('(%d, %d) -> %.8f' % (u, v, p))

    print('--------------------------')

    #
    # preds = nx.jaccard_coefficient(graph)
    # a=list(preds)
    # b=np.array(a)
    # print(b)
    # c=b[np.lexsort(-b.T)]
    # print(c)
    # l=5
    # d=c[0:l]
    # print(d)
    #
    # for i in range(l):
    #   print(int(d[i][0]),int(d[i][1]))