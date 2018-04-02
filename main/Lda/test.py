from __future__ import division, print_function
import xlrd
import numpy as np
import lda
import lda.datasets
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
'''
这个小例子测试的是 用所有词做特征文本提取（方法一）与sklearn.feature_extraction.text（方法二）的区别
 第二种方法中回删去一些不重要的词，但是方法一在设置阈值之后，效果差不多。（其方法2将英文全部变为小写）
'''
if __name__ == '__main__':
    path=r"../Output/8.8.21.xls"
    xl = xlrd.open_workbook(path)
    sheet = xl.sheets()[0]
    corpus = []
    data = []
    for i in range(0, sheet.ncols):
        data.append(list(sheet.col_values(i)))
    data = data[1][1:]  # 形如 ['人民日报/四川/','手机/加油/']
    data = "".join(data)  # 形如 人民日报/四川/九寨沟/地震/
    w1=(set(data.split('/')))


    corpus = data.replace('/', '\t')  # 形如 人民日报	四川	九寨沟	地震 type:string
    corpus= [corpus]                    # 形如[人民日报	四川	九寨沟	地震] 由于只有一篇文档，所以list只有一个元素
    vectorizer = CountVectorizer()  #将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
    X = vectorizer.fit_transform(corpus) #fit_transform是将文本转为词频矩阵
    print(type(X))
    w2 = vectorizer.get_feature_names() #获取词袋模型中的所有词语
    print(w1, '\n', 'type:', type(w1), 'length:', len(w1))
    print(w2, '\n', 'type:', type(w2), 'length:', len(w2))

    def diff_list(l1,l2):
        return set(l1)-set(l2)
    print(diff_list(w1,w2))
    print('Everthingwillbeok'in w1)

    '''
    如果老师说需要用到方法2，就用此方法读取excel文件
    '''
    def readxls(path):
        '''读取Excle中的语料，一行预料为一个文档（仅有一篇文档）'''
        xl = xlrd.open_workbook(path)
        sheet = xl.sheets()[0]
        corpus = []
        data = []
        for i in range(0, sheet.ncols):
            data.append(list(sheet.col_values(i)))
        data = data[1][1:]  # 形如 ['人民日报/四川/','手机/加油/']
        data = "".join(data)  # 形如 人民日报/四川/九寨沟/地震/
        # print(len(set(data.split('/'))))
        corpus = data.replace('/', '\t')  # 形如 人民日报	四川	九寨沟	地震 type:string
        return [corpus]