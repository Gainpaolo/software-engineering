"""string = "Special $#! characters $%#$/*+  spaces 888323"
print(''.join(e for e in string if e.isalnum()))"""
from PinYin_hh import Pinyin
from Tran_slate import Translate
import itertools
import numpy as np
from Pinyin2Hanzi import DefaultDagParams
from Pinyin2Hanzi import dag
pinyin = Pinyin()
translate = Translate()
read_dictionary = np.load('../031902322/my_words.npy', allow_pickle=True).item()


class WORDword:
    @staticmethod
    def changeandarra(str1):
        all1 = []
        for i in str1:
            one_word = [i]
            if '\u4e00' <= i <= '\u9fff':
                one_word.append(pinyin.GetPinyin(i))
                d = [pinyin.GetPinyin(i).lower()]
                dagparams = DefaultDagParams()
                # 10个候选值
                result = dag(dagparams, d, path_num=5, log=True)
                for item in result:
                    res = item.path  # 转换结果
                    if res[0] not in one_word:
                        one_word.append(res[0])
                one_word.append(pinyin.GetPinyin(i)[0])
                one_word.append(translate.ToTraditionalChinese(i))
                if i in read_dictionary:
                    one_word.append(read_dictionary[i])

            all1.append(one_word)

        """获得所有的可能的组合"""
        g = []
        for i in range(0, len(all1) - 1):
            if i == 0:
                g = [k for k in itertools.product(all1[i], all1[i + 1])]  # 笛卡尔乘积,第一次笛卡尔用ALL队列的第一个元素和第二个进行
            else:
                g = [k for k in itertools.product(g, all1[i + 1])]  # 后面的都是用g与ALL进行笛卡尔积
        all1.clear()
        for i in g:
            all1.append(''.join(e for e in str(i) if e.isalnum()))  # 除去特殊字符
            all1.sort()
        return all1
