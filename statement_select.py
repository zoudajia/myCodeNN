import os
import sys
import re
import math


def divide_token(token):
    # 如defaultValue, QueryOptions, assertEndBoundjngQ 
    pattern = re.compile(r'[A-Z]*[a-z]+[A-Z]')
    m = re.match(pattern, token)
    str = []
    str2 = token
    while m != None:
        str1 = str2[m.start():m.end()-1]
        str2 = str2[m.end()-1:]
        str.append(str1.lower())
        m = re.match(pattern, str2)
    str.append(str2.lower())
    return str
    

def two_sentences_similarity(sents_1, sents_2):
    sents_1_tokens = re.split(r'[^A-Za-z0-9]+', sents_1)
    sents_2_tokens = re.split(r'[^A-Za-z0-9]+', sents_2)
    sents_1_token = [token for token in sents_1_tokens if token != '']
    sents_2_token = [token for token in sents_2_tokens if token != '']
    sen = []
    for sent in sents_1_token:
        sen.append(divide_token(sent))
    sent_1 = [i for arr in sen for i in arr]
    sen = list(set(sent_1))
    if len(sen) == 0 or len(sents_2_token) == 0:
        return 0
    
    counter = 0
    for sent in sen:
        if sent in sents_2_token:
            counter = counter + 1
    if len(sen) == 1 and len(sents_2_token) == 1:
        sents_similarity = counter / 2
    else:
        sents_similarity = counter / (math.log(len(sen)) + math.log(len(sents_2_token)))
    return sents_similarity


def read_lines(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return lines


def normalization(datas):
    max_data = max(datas)
    min_data = min(datas)
    norm_data = []
    for data in datas:
        if max_data > min_data:
            norm_data.append((data - min_data) / (max_data - min_data))
        else:
            norm_data.append(1)
    return norm_data


def write_file(file, data):
    with open(file, 'a+', encoding='utf-8') as f:
        f.writelines(data) 


def select_statements(code_methods, comment_methods):
    codes = []
    for i in range(len(code_methods)):
        # 划分语句
        code_s = re.split(r'\{|\}|;', code_methods[i])
        code_statements = [j for j in code_s if j != '']
        # 计算每个语句的相似度
        scores = []
        for code_statement in code_statements:
            score = two_sentences_similarity(code_statement, comment_methods[i])
            scores.append(score)
        # 归一化
        scores = normalization(scores)
        # 选择相似度阈值大于0.5的代码语句
        code_select_statements = code_statements[0].strip() + " "
        for j in range(1, len(scores)):
            if scores[j] >= 0.5:
                code_select_statements = code_select_statements + code_statements[j].strip() + " "
        code_select_statements = code_select_statements + '\n'
        codes.append(code_select_statements)
    return codes
    

code_file = './code_method_filter.txt'
comment_file = './comment_method_filter.txt'
codes_select_file = './code_select_statement.txt'

codes = read_lines(code_file)
comments = read_lines(comment_file)
codes_selected = select_statements(codes, comments)
write_file(codes_select_file, codes_selected)