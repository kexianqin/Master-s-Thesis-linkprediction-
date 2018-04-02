import numpy as np
import re,collections
import time
import xlrd
from pprint import pprint as p

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

@log
def readxls(path):
    '''读取Excle中的数据，返回的data形如['四川/九寨沟/', '乐观/四川人/小震/',...]'''
    xl = xlrd.open_workbook(path)
    sheet = xl.sheets()[0]
    data = []
    for i in range(0, sheet.ncols):
        data.append(list(sheet.col_values(i)))
    data=data[1][1:]
    return data

@log
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

@log
def get_set_key(dic,threshold):
    '''选取频数大于等于Threshold的关键词构建一个集合，用于作为共现矩阵的首行和首列'''
    wf = {k: v for k, v in dic.items() if v >= threshold}
    set_key_list=[]
    for a in sorted(wf.items(), key=lambda item: item[1], reverse=True):
        set_key_list.append(a[0])
    return set_key_list

@log
def build_matirx(set_key_list):
    '''建立矩阵，矩阵的高度和宽度为关键词集合的长度+1'''
    edge = len(set_key_list)+1
    # matrix = np.zeros((edge, edge), dtype=str)                  #<class 'numpy.ndarray'>
    matrix = [['' for j in range(edge)] for i in range(edge)] #<class 'list'>
    return matrix

@log
def init_matrix(set_key_list, matrix):
    '''初始化矩阵，将关键词集合赋值给第一列和第二列'''
    matrix[0][1:] = np.array(set_key_list)
    matrix = list(map(list, zip(*matrix)))
    matrix[0][1:] = np.array(set_key_list)
    return matrix

@log
def format_data(data):
    '''格式化需要计算的数据，将原始数据格式转换成二维数组'''
    formated_data = []
    for ech in data:
        ech_line = ech.split('/')
        ech_line = list(filter(lambda x: x != '', ech_line))
        formated_data.append(ech_line)
    return formated_data

@log
def count_matrix(matrix, formated_data):
    '''计算各个关键词共现次数'''
    for row in range(1, len(matrix)):
        # 遍历矩阵第一行，跳过下标为0的元素
        for col in range(1, len(matrix)):
                # 遍历矩阵第一列，跳过下标为0的元素
                # 实际上就是为了跳过matrix中下标为[0][0]的元素，因为[0][0]为空，不为关键词
            if matrix[0][row] == matrix[col][0]:
                # 如果取出的行关键词和取出的列关键词相同，则其对应的共现次数为0，即矩阵对角线为0
                matrix[col][row] = str(0)
            else:
                counter = 0
                # 初始化计数器
                for ech in formated_data:
                        # 遍历格式化后的原始数据，让取出的行关键词和取出的列关键词进行组合，
                        # 再放到每条原始数据中查询
                    if matrix[0][row] in ech and matrix[col][0] in ech:
                        counter += 1
                    else:
                        continue
                matrix[col][row] = str(counter)
    return matrix

@log
def showmatrix(matrix):
    matrixtxt = ''
    count = 0
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix)):
            matrixtxt = matrixtxt+str(matrix[i][j])+'\t'
        matrixtxt = matrixtxt[:-1]+'\n'
        count = count+1
        print('No.'+str(count)+' had been done!')
    return matrixtxt

@log
def wryer(path, text):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(text)
    return path+' is ok!'




if __name__ == "__main__":
    readpath = r"../Output/地震实验.xls"
    outputpath = r'C:\Users\Administrator\Desktop\haha3.txt'
    threshold=15

    data=readxls(readpath)

    dic=countfrequency(readxls(readpath))

    set_key_list=get_set_key(dic,threshold)

    matrix=build_matirx(set_key_list)
    print(type(matrix))

    matrix=init_matrix(set_key_list, matrix)
    format_data=format_data(data)

    # result_matrix=count_matrix(matrix, format_data)
    #
    # show_matrix=showmatrix(result_matrix)
    # wryer(outputpath, show_matrix)

