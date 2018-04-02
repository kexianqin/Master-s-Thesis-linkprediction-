import jieba
import jieba.posseg as pseg
import sys
# pyexcel_xls 以 OrderedDict 结构处理数据
from collections import OrderedDict
from pyexcel_xls import get_data
from pyexcel_xls import save_data
import re

sys.path.append("../")
jieba.load_userdict('../Glossary/地震专业术语.txt')
jieba.load_userdict('../Glossary/四川地名.txt')
jieba.load_userdict('../Glossary/手动添加.txt')
jieba.add_word('应急办')

class ChPreprocess:
    def __init__(self):
        print('Chinese Preprocess...')

    # def FileRead(self, filePath):
    #     f = open(filePath, 'r')
    #     raw = f.read(
    #     return raw
    def delete_weibo_name(self,content): #去掉介于 @与: 之间的微博名
        return re.compile(r'@.*?:').sub('',content)

    def stopwordslist(self,filepath): # 创建停用词list
        stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
        return stopwords

    def JiebaTokener(self, raw):
        words = pseg.cut("".join(raw.split()).replace(u'\u200b',''))  # 进行分词
        stopwords = self.stopwordslist('../Glossary/stopword.txt')
        result = ''  # 记录最终结果的变量
        for w in words:
            #    result+= str(w.word)+"/"+str(w.flag) #加词性标注 甚至可以用词性过滤 if x.flag.startswith('n')
            if w.word not in stopwords:
                if w.word != '\t':
                    result += str(w.word) + "/"  # 去停用词
        return result

    def save_xls_file(self,xls_data,path):
        data = OrderedDict()
        # sheet表的数据
        sheet_1 = []
        for line in xls_data:
            sheet_1.append(line)
        data.update({u"这是XX表": sheet_1})

        # 保存成xls文件
        save_data(path, data)


if __name__ == "__main__":
    readpath=r"..\Data\8.8.21.xlsx"  #Excel格式有要求，只要三列，依次为id，内容，发布时间
    outputpath=r"..\Output\8.8.21.xls"

    chPreprocess=ChPreprocess()
    xls_data = get_data(readpath)
    print("Get data type:",type(xls_data))
    for sheet_n in xls_data.keys():  #sheet_n指的是一个Excel文件中表的个数，从左下角能看到，我们只设置一张表
        #print(sheet_n, ":", xls_data[sheet_n])
        for i,line_n in enumerate(xls_data[sheet_n]):
            if line_n[1] != '博文内容':
                a=chPreprocess.JiebaTokener(chPreprocess.delete_weibo_name(line_n[1]))
                line_n[1]=a
                print(i)
        print(sheet_n, ":", xls_data[sheet_n])
        chPreprocess.save_xls_file(xls_data[sheet_n],outputpath)


