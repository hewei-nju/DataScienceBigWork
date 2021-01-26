# -*- coding: utf-8 -*-
import json

from snownlp import SnowNLP
import codecs
import os
import matplotlib.pyplot as plt
import numpy as np

path = r'C:\Users\ThinkPad\PycharmProjects\dataScience\nocut'

for i in os.listdir(path):
    data = ""
    repath = path + '\\' + str(i)
    for j in os.listdir(repath):
        datapath = repath + '\\' + str(j)
        source = open(datapath, encoding='utf-8').read()
        for line in source.split('\n'):
            sentimentslist = []
            for k in line:
                s = SnowNLP(k)
                # print(s.sentiments)
                sentimentslist.append(s.sentiments)
plt.hist(sentimentslist, bins=np.arange(0, 1, 0.01), facecolor='g')
plt.xlabel('Sentiments Probability')
plt.ylabel('Quantity')
plt.title('Analysis of Sentiments')
plt.show()
