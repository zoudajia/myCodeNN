import os
import re


def read_lines(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
    return lines


def write_file(file, data):
    with open(file, 'a+', encoding='utf-8') as f:
        f.writelines(data) 


def filter_chinese(codes, comments):
    # 匹配中文字符
    pattern = re.compile(u'[\u4e00-\u9fff]+')
    codes_new = []
    comments_new = []
    for i in range(len(comments)):
        match = re.search(pattern, comments[i])
        if match == None:
            comments_new.append(comments[i]+"\n")
            codes_new.append(codes[i]+"\n")
    return codes_new, comments_new


def filter_param(codes, comments):
    codes_new = []
    comments_new = []
    for i in range(len(comments)):
        if re.match(r'^[\w]+', comments[i]):
            codes_new.append(codes[i]+"\n")
            comments_new.append(comments[i]+"\n")
    return codes_new, comments_new


path = '/Users/dajia/Documents/work/'
code_file = 'code_method.txt'
comment_file = 'comment_method.txt'
code_file_new = 'code_method_filter.txt'
comment_file_new = 'comment_method_filter.txt'

# 读入代码和注释
codes = read_lines(code_file)
comments = read_lines(comment_file)

# 过滤comment中文字符
code, comm = filter_chinese(codes, comments)

# 去除换行符
code_ = [cd.strip() for cd in code]
comm_ = [cm.strip() for cm in comm]

# 过滤不是以英文字符开始的comment
codes_new, comments_new = filter_param(code_, comm_)

# 写入代码和注释
write_file(code_file_new, codes_new)
write_file(comment_file_new, comments_new)







