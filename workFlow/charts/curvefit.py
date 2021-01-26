# -*- coding:utf-8 -*-
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


def loadData(num_path):
    with open(num_path, mode='r', encoding='utf-8') as file:
        dic = json.load(file)
        x = []
        for i in range(1, len(dic.keys())):
            x.append(int(dic[str(i)]))
        return x


def draw(x):
    # print(x)
    # x = np.arange(70, 1000, 50)
    u = np.mean(x)
    sigma = np.std(x)
    num_bins = len(x)  # 直方图柱子的数量
    n, bins, patches = plt.hist(x, num_bins, density=True, alpha=1.0)
    # 直方图函数，x为x轴的值，normed=1表示为概率密度，即和为一，绿色方块，色深参数0.5.返回n个概率，直方块左边线的x值，及各个方块对象
    y = norm.pdf(bins, u, sigma)  # 拟合一条最佳正态分布曲线y
    print(y)

    plt.grid(True)
    plt.plot(bins, y, 'r--')  # 绘制y的曲线
    plt.xlabel('values')  # 绘制x轴
    plt.ylabel('Probability')  # 绘制y轴
    plt.title('Histogram : $\mu$=' + str(round(u, 2)) + ' $\sigma=$' + str(round(sigma, 2)))  # 中文标题 u'xxx'
    # plt.subplots_adjust(left=0.15)#左边距
    plt.show()


if __name__ == "__main__":
    num_path = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\charts\num.txt"
    x = loadData(num_path)
    draw(x)
