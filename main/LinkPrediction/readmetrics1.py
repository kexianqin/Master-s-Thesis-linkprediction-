# -*- coding: utf-8 -*-
import numpy as np

## 将含有-----------------的排注释掉，并将49,55行的int()去掉就能还原之前的含有中文的矩阵版本。

#(k) ['+' '地震' '九寨沟' '四川'] -->{0: '+', 1: '地震', 2: '九寨沟', 3: '四川'}
def translateDic(list):                        #---------------------
    dic = {}
    pos = 0
    for i in list:
        dic[pos] = str(i)
        pos = pos + 1
    return dic

#(k) 由字典的值来找键,即把中文翻译为汉字
def get_value_key(dic, *valuelist):            #---------------------
    keylist = []
    contrarydic = {v: k for k, v in dic.items()}
    for value in valuelist:
        key = contrarydic[value]
        keylist.append(key)
    if len(valuelist) == 1:
        return keylist[0]
    else:
        return keylist

def readFile(path):
    # 打开文件（注意路径）
    f = open(path,'r',encoding='UTF-8')
    # 逐行进行处理

    dic={}                                       #----------------------
    #做一个翻译（'地震' '九寨沟' '四川'-->1 2 3）

    first_ele = True
    for data in f.readlines():
        ## 去掉每行的换行符，"\n"
        data = data.strip('\n')
        ## 按照 空格进行分割。
        nums = data.split("\t")
        ## 添加到 matrix 中。
        if first_ele:
            #中文翻译为数字
            dic=translateDic(nums)              #---------------------
            nums=get_value_key(dic,*nums)       #---------------------
            ### 将字符串转化为整型数据
            nums = [int(x) for x in nums ]
            ### 加入到 matrix 中 。
            matrix = np.array(nums)
            first_ele = False
        else:
            nums[0]=get_value_key(dic,nums[0])  #---------------------
            nums = [int(x) for x in nums]

            matrix = np.c_[matrix,nums]
    dealMatrix(matrix)
    f.close()

def dealMatrix(matrix):

    print(matrix)
    ## 一些基本的处理。
    # print("transpose the matrix")
    # matrix = matrix.transpose()
    # print(matrix)
    #
    # print("matrix trace ")
    # print(np.trace(matrix))

# test.
if __name__ == '__main__':
    readFile(r"C:\Users\Administrator\Desktop\haha.txt")