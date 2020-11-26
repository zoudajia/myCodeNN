import re
import os


path = '/Users/dajia/Documents/work/'
files = os.listdir(path)
code_file = '/Users/dajia/Documents/work/code.txt'
comment_file = '/Users/dajia/Documents/work/comment.txt'

file = 'AzureBlobStoreRepositoryTests.java'

comment = re.compile(r'/\*((?:.|\n)*?)\*/\\n', re.S)

with open(path + file, 'r', encoding='utf-8') as f:
    lines = [line.strip(" ") for line in f.readlines()]
comments = comment.findall(str(lines))
print(comments)
