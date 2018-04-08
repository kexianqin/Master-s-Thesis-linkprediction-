import numpy as np
from pprint import pprint as p
import re, collections
from functools import reduce
import random
import networkx as nx
from class_similarity_easytest import*
from sampling_train_test_split import*
from metrics import *
if __name__ == '__main__':
    # a=[[1,2,3],[2,9,4],[5,6,7]]
    # b=np.array(a)
    # print(b.shape[0])
    # print('---')
    # print(b[:,1].argsort()[-1:])

    matrix = [['' for j in range(3)] for i in range(3)]
    print(matrix)
