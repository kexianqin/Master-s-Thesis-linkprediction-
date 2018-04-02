#! /usr/bin/env python  
# coding=utf-8

# pyexcel_xls 以 OrderedDict 结构处理数据  
from collections import OrderedDict
from pyexcel_xls import get_data
from pyexcel_xls import save_data


def read_xls_file():
    xls_data = get_data(r"..\Data\地震实验.xlsx")
    print("Get data type:", type(xls_data))
    for sheet_n in xls_data.keys():
        print(sheet_n, ":", xls_data[sheet_n])
        for line_n in xls_data[sheet_n]:
            if line_n[1] != '博文内容':

                a=line_n[1].replace(" ", "").strip('').replace(u'\u200b','') #这个u表示将后面跟的字符串以unicode格式存储
                print(a)   #关于replace(u'\u200b','')，见http://www.newsmth.net/nForum/#!article/Python/124657
                print(len(a))
                print('-'*40)

if __name__ == '__main__':
    read_xls_file() 