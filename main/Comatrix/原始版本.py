import os
import xlrd
import re
import time


def readxls(path):
    xl = xlrd.open_workbook(path)
    sheet = xl.sheets()[0]
    data = []
    for i in range(0, sheet.ncols):
        data.append(list(sheet.col_values(i)))
    return (data[1][1:])


def buildmatrix(x, y):
    return [[0 for j in range(y)] for i in range(x)]


def dic(xlspath):
    keygroup = readxls(xlspath)
    keytxt = ''.join(keygroup) #因为每句话形如‘西瓜/视频/’，故可以直接用‘’来链接而不是‘/’
    keyfir = keytxt.split('/')
    keylist = list(set([key for key in keyfir if key != ''])) #set作用去掉重复值
    keydic = {}
    pos = 0
    for i in keylist:
        pos = pos+1
        keydic[pos] = str(i)
    return keydic

def countwordsfrequency(dic,keylis): #统计每个词的频数，同一段文字中出现多次算一次。
    wordsfrequency={}
    for d in dic:
        count = 0
        for k in keylis:
            ech=str(k).split('/')
            if str(dic[d]) in ech:
                count +=1
            else:
                continue
        wordsfrequency[str(dic[d])]=count
    return wordsfrequency

def order(wordsfrequency,x):   #调整字典顺序，按照关键词频数从大到小进行排序;并选取频次大于x的关键词
    newdic = {}
    wf={k: v for k, v in wordsfrequency.items() if v > x}   #这句话作用就是选取频次大于x的关键词
    pos = 0
    for a in sorted(wf.items(),key=lambda item:item[1],reverse=True):
        pos = pos + 1
        newdic[pos] = str(a[0])
    return newdic

def inimatrix(matrix, dic, length):
    matrix[0][0] = '+'

    for i in range(1, length):
        matrix[0][i] = dic[i]
    for i in range(1, length):
        matrix[i][0] = dic[i]
    # pt(matrix)
    return matrix

def countmatirx(matrix, dic, mlength, keylis):
    for i in range(1, mlength):
        for j in range(1, mlength):
            count = 0
            if str(matrix[0][i]) == str(matrix[j][0]):
                matrix[i][j]=str(wordsfrequency[matrix[0][i]])
            else:
                for k in keylis:
                    ech = str(k).split('/')
                    # print(ech)
                    if str(matrix[0][i]) in ech and str(matrix[j][0]) in ech :
                        count = count+1
                    else:
                        continue
                matrix[i][j] = str(count)
    return matrix

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

def wryer(path, text):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(text)
    return path+' is ok!'

if __name__ == "__main__":
    readpath=r"../Output/8.8.21.xls"
    outputpath=r'C:\Users\Administrator\Desktop\haha2.txt'
    x=1   #选取频次大于x的值来做共现矩阵

    keylis = readxls(readpath)  #读取Excel数据
    keydic= dic(readpath)       #建立词典，去掉重复值
    print('keylis ：',keylis)
    print('keydic : ',keydic)

    wordsfrequency=countwordsfrequency(keydic,keylis)  #统计每个词的频次
    print('wordsfrequency : ',wordsfrequency)

    # newdic=order(wordsfrequency,x)
    # print('newdic :',newdic)
    #
    # length = len(newdic) + 1  # 矩阵长宽
    # print(length)
    #
    # matrix=buildmatrix(length, length)
    # print(matrix)
    # print('Matrix had been built successfully!')
    #
    # matrix = inimatrix(matrix, newdic, length)
    # print(matrix)
    # print('Col and row had been writen!')
    #
    # matrix = countmatirx(matrix, newdic, length, keylis)
    # print(matrix)
    # print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),'Matrix had been counted successfully!')
    #
    # matrixtxt = showmatrix(matrix)
    # # pt(matrix)
    # print(wryer(outputpath, matrixtxt))