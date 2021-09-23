# -*- coding:utf-8 -*-
"""DFA算法思想是将敏感词组通过建立嵌套字典的方式去构建敏感词链表(以一个特定字符’\x00’作为结束),
然后遍历新词的每个字是否出现在敏感词链表中,如果出现,即为敏感词,"""
import time
import re
import sys
from c_and_arrangement import WORDword


# DFA算法

class DFAFilter:

    def __init__(self):
        self.keyword_chains = {}
        self.delimit = '\x00'

    def add(self, keyword, ww):
        keyword = keyword.lower()  # 关键词英文变为小写
        chars = keyword.strip()  # 关键字去除首尾空格和换行
        if not chars:  # 如果关键词为空直接返回
            return
        level = self.keyword_chains
        # 遍历关键字的每个字
        i = 0
        for i in range(len(chars)):
            if chars[i] in level:
                # 如果这个字已经存在字符链的key中就进入其子字典
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                last_level = {}
                last_char = ""
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: ww}  # 对同一类别的敏感词进行标记
                break
        if i == len(chars) - 1:  # 最后一个字
            level[self.delimit] = ww  # 对同一类别的敏感词进行标记

    def parse(self, path):  # 创建敏感词树
        tt = 1
        with open(path, encoding='utf-8') as f:
            for keyword in f:
                keyword = keyword.strip()
                all_kind = WORDword.changeandarra(keyword)
                for i in all_kind:
                    self.add(str(i).strip(), tt)
                tt = tt + 1

    def filter(self, path1, path2, path3):
        messages = open(path1, encoding="utf-8")
        i = 1
        total = 0
        allword = []
        rang = []
        old_word = []
        baocun_oldword = []
        mark = 0
        temp = {}
        string = "~!@#！…￥$%^&*( )·|_+-*/<>,—.[]=?;\"{}，。《》？\\:：“/1234\'56789【】；‘、；"
        with open(path3, encoding="utf-8") as pps:
            for pp in pps:
                pp = pp.strip()
                old_word.append(pp)
        for message in messages:
            start = 0
            find_1 = ''
            while start < len(message):
                level = self.keyword_chains
                step_ins = 0
                for char in message[start:]:
                    char1 = char.lower()
                    if (re.search(r"\W", char1) or char1 in string) and step_ins != 0:
                        find_1 = find_1 + char1
                        step_ins += 1
                        continue
                    if char1 in level:
                        step_ins += 1
                        find_1 = find_1 + char
                        if self.delimit not in level[char1]:
                            level = level[char1]
                        else:
                            number = re.findall("\\d+", str(level[char1].values()))
                            if len(level[char1]) == 1 and mark == 0:
                                # number = re.findall("\\d+", str(level[char1].values()))  # 这里用正则找到之前标记的敏感词种类
                                baocun_oldword.append(old_word[int(number[0]) - 1])
                                allword.append(find_1)
                                rang.append(i)
                                find_1 = ''
                                start += step_ins - 1
                                total += 1
                                level = level[char1]
                                break
                            else:
                                mark += 1
                                level = level[char1]
                                temp[1] = old_word[int(number[0]) - 1]
                                temp[2] = find_1
                                temp[3] = i
                    else:
                        if len(temp) != 0:
                            baocun_oldword.append(temp[1])
                            allword.append(temp[2])
                            rang.append(temp[3])
                            total += 1
                            temp.clear()
                        mark = 0
                        find_1 = ''
                        break
                start += 1
            i = i + 1
        f = open(path2, 'a', encoding='utf-8')
        f.write('Total: {}\n'.format(total))
        for i in range(len(allword)):
            f.write('Line{}'.format(rang[i]) + ': <' + baocun_oldword[i] + '> ' + allword[i] + '\n')


def main(argv):
    path1 = argv[1]
    path2 = argv[2]
    path3 = argv[3]
    gfw = DFAFilter()
    # path1 = "E:/hh/words.txt"
    # path2 = 'E:/hh/org.txt'
    # path3 = 'E:/hh/tst.txt'
    gfw.parse(path1)
    gfw.filter(path2, path3, path1)
    time2 = time.time()
    print('总共耗时：' + str(time2 - time1) + 's')


if __name__ == "__main__":
    time1 = time.time()
    if len(sys.argv) != 4:
        print('usage: python  getuser.py inputfile1 inputfile2 outfile')
    else:
        main(sys.argv)

