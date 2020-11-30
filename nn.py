import torch
import torch.autograd as autograd # torch中自动计算梯度模块
import torch.nn as nn # 神经网络模块
import torch.nn.functional as F # 神经网络模块中常用的功能
import torch.optim as optim # 模型优化器

torch.manual_seed(1)

# lstm 单元输入和输出纬度都是3
lstm = nn.LSTM(3, 3)
# 生成一个长度为5，每一个元素为1*3的序列作为输入，这里的数字3对应于上句中第一个3
inputs = [autograd.Variable(torch.randn(1,3)) for _ in range(5)]

# 设置隐藏层纬度，初始化隐藏层的数据,hidden是一个元组
hidden = (autograd.Variable(torch.randn(1, 1, 3)), autograd.Variable(torch.randn(1, 1, 3)))

def way_1(inputs, hidden):
    for i in inputs:
        # Step through the sequence one element at a time.
        # after each step, hidden contains the hidden state.
        out, hidden = lstm(i.view(1, 1, -1), hidden)
        print(out)
        print(hidden)

def way_2(inputs, hidden):
    inputs = torch.cat(inputs).view(len(inputs), 1, -1)
    out, hidden = lstm(inputs, hidden)
    print(out)
    print(hidden)


training_data = [
    ("The dog ate the apple".split(), ["DET", "NN", "V", "DET", "NN"]),
    ("Everybody read that book".split(), ["NN", "V", "DET", "NN"])
]

word_to_ix = {} # 单词的索引字典
for sent, tags in training_data:
    for word in sent:
        if word not in word_to_ix:
            word_to_ix[word] = len(word_to_ix)
print(word_to_ix)
tag_to_ix = {"DET": 0, "NN": 1, "V": 2} # 手工设定词性标签数据字典

