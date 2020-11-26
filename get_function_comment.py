import os
import re
import sys


def write_string(file, string):
    with open(file, 'a+', encoding='utf-8') as f:
        string = string + "\n"
        f.writelines(string)


def read(file):
    line = []
    if os.path.isfile(file) and file.split('.')[-1] == 'java':
        # try-except：过滤非二进制编码的JAVA文件
        try:
            with open(file, 'r', encoding='utf-8') as f:
                # 去除Java文件中的单行注释
                for lin in f.readlines():
                    lin = lin.strip()
                    if lin.find('//') != -1:
                        lin = lin[:lin.find('//')]
                    line.append(lin)
        except UnicodeDecodeError:
            write_string(except_file, file)
    return line


path = './java_files/'
if not os.path.exists(path):
    print("No such path!")
    sys.exit()
files = os.listdir(path)
code_file = './code.txt'
comment_file = './comment.txt'
except_file = './except.txt'

for file in files:

    lines = read(path+file)
    if not lines:
        continue

    for i in range(len(lines)):
        comment = ""
        code = ""
        if lines[i].startswith('/*') and lines[i].endswith('*/'):
            comment = comment + lines[i].strip().strip('/').strip('*')
        elif lines[i].startswith('/*'):
            while i < len(lines) and not lines[i].endswith('*/'):
                comment = comment + " " + lines[i].strip('*').strip('/').strip()
                i = i + 1
        i = i + 1
        while i < len(lines) and lines[i].startswith('@'):
            i = i + 1
        if i < len(lines) and lines[i].startswith('public') and comment != "":
            if lines[i].find('{') == -1 and lines[i+1].find('{') != -1:
                code = code + " " + lines[i]
                i = i + 1
            elif lines[i].find('{') == -1 and lines[i+1].find('{') == -1:
                code = ""
                continue
            code = code + " " + lines[i]
            if lines[i].find('}') != -1:
                end = 0
            else:
                i = i + 1
                end = 1
            while end > 0 and i < len(lines):
                code = code + " " + lines[i]
                end = end + lines[i].count("{") - lines[i].count("}")
                i = i + 1
        else:
            i = i - 1
        if code != "" and comment != "":
            write_string(code_file, code)
            write_string(comment_file, comment)
        code = ""
        comment = ""
print("Over!")