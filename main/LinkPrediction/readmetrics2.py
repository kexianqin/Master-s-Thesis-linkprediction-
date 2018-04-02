# -*- coding: utf-8 -*-
import numpy as np

def readFile(path):
    # 打开文件（注意路径）
    f = open(path,'r',encoding='UTF-8')
    # 逐行进行处理
    first_row = True
    for data in f.readlines():
        ## 去掉每行的换行符，"\n"
        data = data.strip('\n')
        ## 按照 空格进行分割。
        nums = data.split("\t")
        ## 添加到 matrix 中。
        if first_row:
            ### 将字符串转化为整型数据
            nums = [x for x in nums ]
            ### 加入到 matrix 中 。
            matrix = np.array(nums)
            first_row = False
        else:
            L=[]
            first_ele=True
            for x in nums:
                if first_ele:
                    L.append(x)
                    first_ele=False
                else:
                    L.append(int(x))
            nums=L
            matrix = np.c_[matrix,nums]  #----到这一步还是变成了字符串类型
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
    readFile(r"C:\Users\Administrator\Desktop\haha2.txt")