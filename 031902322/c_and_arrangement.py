'''string = "Special $#! characters $%#$/*+  spaces 888323"
print(''.join(e for e in string if e.isalnum()))'''
from PinYin_hh import Pinyin
from Tran_slate import Translate
import itertools
import numpy as np
from Pinyin2Hanzi import DefaultDagParams
from Pinyin2Hanzi import dag
pinyin = Pinyin()
translate = Translate()



read_dictionary = np.load('my_words.npy', allow_pickle=True).item()
class word_word:
    def changeandarra(self,str1):
        ALL=[]
        for i in str1:
            one_word=[]
            one_word.append(i)
            if '\u4e00' <= i <= '\u9fff':
                one_word.append(pinyin.GetPinyin(i))
                d=[]
                d.append(pinyin.GetPinyin(i).lower())
                dagParams = DefaultDagParams()
                # 10个候选值
                result = dag(dagParams, d, path_num=15, log=True)
                for item in result:
                    res = item.path  # 转换结果
                    if res[0] not in one_word:
                        one_word.append(res[0])
                one_word.append(pinyin.GetPinyin(i)[0])
                one_word.append(translate.ToTraditionalChinese(i))
                if i in read_dictionary:
                    one_word.append(read_dictionary[i])

            ALL.append(one_word)
        for i in range(0,len(ALL)-1):
            if i==0:
                g=[k for k in itertools.product(ALL[i],ALL[i+1])]
            else:
                g = [k for k in itertools.product(g, ALL[i + 1])]
        ALL.clear()
        for i in g:
            ALL.append(''.join(e for e in str(i) if e.isalnum()))
            ALL.sort()
        return ALL

