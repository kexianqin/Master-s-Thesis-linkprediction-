import numpy as np
import re,collections
import time
import xlrd
from pprint import pprint as p
from functools import reduce

# def log(func):
#     def wrapper(*args, **kwargs):
#         now_time = str(time.strftime('%Y-%m-%d %X', time.localtime()))
#         print('------------------------------------------------')
#         print('%s %s called' % (now_time, func.__name__))
#         print('Document:%s' % func.__doc__)
#         print('%s returns:' % func.__name__)
#         re = func(*args, **kwargs)
#         p(re)
#         return re
#     return wrapper

# @log
def readxls(path):
    '''读取Excle中的数据，返回的data形如['四川/九寨沟/', '乐观/四川人/小震/',...]'''
    xl = xlrd.open_workbook(path)
    sheet = xl.sheets()[0]
    data = []
    for i in range(0, sheet.ncols):
        data.append(list(sheet.col_values(i)))
    data=data[1][1:]
    return data

# @log
def countfrequency(data):
    '''统计词频(其中data为readxls步的返回值),返回一个字典,如{'街区': 114,'天灾': 113,...}'''
    keylist = []
    for txt in data:
        keyfir = txt.split('/')
        keylist.extend(list(set([key for key in keyfir if key != ''])))
    c = collections.Counter(keylist)  #统计词频
    # result=c.most_common(1000)  取频数最大的1000个词
    dic=dict(c)
    return dic

# @log
def get_set_key(dic,threshold):
    '''选取频数大于等于Threshold的关键词构建一个集合，用于作为共现矩阵的首行和首列'''
    wf = {k: v for k, v in dic.items() if v >= threshold}
    set_key_list=[]
    for a in sorted(wf.items(), key=lambda item: item[1], reverse=True): #对字典按频数进行排序
        set_key_list.append(a[0])
    return set_key_list

# @log
def build_matirx(set_key_list):
    '''建立矩阵，矩阵的高度和宽度为关键词集合的长度+1'''
    edge = len(set_key_list)+1
    # matrix = np.zeros((edge, edge), dtype=str)              #<class 'numpy.ndarray'>，适合英文
    matrix = [['' for j in range(edge)] for i in range(edge)] #<class 'list'>
    return matrix

# @log
def init_matrix(set_key_list, matrix):
    '''初始化矩阵，将关键词集合赋值给第一列和第二列'''
    matrix[0][1:] = np.array(set_key_list)
    matrix = list(map(list, zip(*matrix)))
    matrix[0][1:] = np.array(set_key_list)
    return matrix

# @log
def format_data(data,set_key_list):
    '''格式化需要计算的数据，将原始数据格式转换成二维数组'''
    formated_data = []
    for ech in data:
        ech_line = ech.split('/')

        temp=[]                 # 筛选出format_data中属于关键词集合的词。
        for e in ech_line:
            if e in set_key_list:
                temp.append(e)
        ech_line = temp

        ech_line = list(set(filter(lambda x: x != '', ech_line))) #set去掉重复数据
        formated_data.append(ech_line)
    return formated_data

# @log
def count_matrix(matrix, formated_data):
    '''计算各个关键词共现次数'''
    keywordlist=matrix[0][1:]  #列出所有关键词
    appeardict={}  #每个关键词与 [出现在的行(formated_data)的list] 组成的dictionary
    for w in keywordlist:
        appearlist=[]
        i=0
        for each_line in format_data:
            if w in each_line:
                appearlist.append(i)
            i +=1
        appeardict[w]=appearlist

    for row in range(1, len(matrix)):
        # 遍历矩阵第一行，跳过下标为0的元素
        for col in range(1, len(matrix)):
                # 遍历矩阵第一列，跳过下标为0的元素
                # 实际上就是为了跳过matrix中下标为[0][0]的元素，因为[0][0]为空，不为关键词
            if col >= row:
                #仅计算上半个矩阵
                if matrix[0][row] == matrix[col][0]:
                    # 如果取出的行关键词和取出的列关键词相同，则其对应的共现次数为0，即矩阵对角线为0
                    matrix[col][row] = str(0)
                else:
                    counter = len(set(appeardict[matrix[0][row]])&set(appeardict[matrix[col][0]]))

                    matrix[col][row] = str(counter)
            else:
                matrix[col][row]=matrix[row][col]
    return matrix

# @log
def showmatrix(matrix):
    '''以矩阵的方式'''
    matrixtxt = ''
    count = 0
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix)):
            matrixtxt = matrixtxt+str(matrix[i][j])+'\t'
        matrixtxt = matrixtxt[:-1]+'\n'
        count = count+1
        print('No.'+str(count)+' had been done!')
    return matrixtxt

# @log
def showmatrix2(matrix):
    '''以顶点对的方式'''
    matrixtxt = ''
    for i in range(1, len(matrix)):
        for j in range(1, len(matrix)):
            if i < j:
                if int(matrix[i][j]) != 0:
                    matrixtxt = matrixtxt + matrix[i][0]+'\t'+matrix[0][j]+'\t'+matrix[i][j]+'\n'

    return matrixtxt

# @log
def showvocab(dic,set_key_list):
    '''输出关键词及频数'''
    vocabtxt = ''
    for w in set_key_list:
        vocabtxt += w + '\t'+str(dic[w])+'\n'
    return vocabtxt

# @log
def wryer(path, text):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(text)
    return path+' is ok!'




if __name__ == "__main__":
    stage='起始'
    threshold = 3

    readpath = r"../Output/"+stage+"阶段.xls"
    outputpath1 = r'../Output/'+stage+r'阶段/%s'%''+stage+'顶点对(阈值为'+str(threshold)+').txt'
    outputpath2 = r'../Output/'+stage+r'阶段/%s'%''+stage+'词频(阈值为'+str(threshold)+').txt'

    data=readxls(readpath)

    dic=countfrequency(data)

    set_key_list=get_set_key(dic,threshold)
    print('关键词个数：',len(set_key_list))
    print(str(dic['地震']))
    wryer(outputpath2, showvocab(dic,set_key_list))
    # 输出到文件的形式来查看 共现矩阵 由哪些关键词构成

    matrix=build_matirx(set_key_list)
    print(type(matrix))

    matrix=init_matrix(set_key_list, matrix)

    format_data=format_data(data,set_key_list)

    start_time = time.time()
    result_matrix=count_matrix(matrix, format_data)
    end_time = time.time()
    print(end_time - start_time)

    print(result_matrix[0],'\n',[row[0] for row in result_matrix])

    show_matrix=showmatrix2(result_matrix)
    wryer(outputpath1, show_matrix)