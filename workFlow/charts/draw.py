# -*- coding: utf-8 -*-
import mplcyberpunk
import numpy as np
import json
import math
import pandas as pd
import matplotlib.pyplot as plt


def load_data(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        return json.load(file)


def draw_bar(labels, quants):
    width = 0.4
    ind = np.linspace(1, len(labels), len(labels))
    # make a square figure
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    # Bar Plot
    ax.bar(ind - width / 2, quants, width, color=['r', 'g', 'b', 'c', 'm', 'y', 'k', 'w'])
    # Set the ticks on x-axis
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
    # labels
    ax.set_xlabel('Every Tow-Week', color='w')
    ax.set_ylabel('News Number', color='w')
    # title
    ax.set_title('All 14 Two-Week', bbox={'facecolor': '0.8', 'pad': 5}, color='k')
    plt.grid(True)
    x = [int(i) for i in labels]
    for a, b in zip(x, quants):
        plt.text(a - 0.1, b + 0.05, '%.0f' % b, ha='center', va='bottom')
    plt.show()
    plt.close()


def draw_Radar_chart():
    plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
    plt.rcParams['axes.unicode_minus'] = False
    plt.style.use('cyberpunk')
    file1 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\First\analysisResult.txt"
    file2 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Second\analysisResult.txt"
    file3 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Third\analysisResult.txt"
    file4 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Forth\analysisResult.txt"
    with open(file1, mode='r', encoding='utf-8') as f1:
        vector1 = json.load(f1)
    with open(file2, mode='r', encoding='utf-8') as f2:
        vector2 = json.load(f2)
    with open(file3, mode='r', encoding='utf-8') as f3:
        vector3 = json.load(f3)
    with open(file4, mode='r', encoding='utf-8') as f4:
        vector4 = json.load(f4)

    # 构造数据
    N = len(vector1)
    # 设置雷达图的角度，用于平分切开一个圆面
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
    # 为了使雷达图一圈封闭起来，需要下面的步骤
    vector1 = np.concatenate((vector1, [vector1[0]]))
    vector2 = np.concatenate((vector2, [vector2[0]]))
    vector3 = np.concatenate((vector3, [vector3[0]]))
    vector4 = np.concatenate((vector4, [vector4[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    # 绘图
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, vector1, 'o-', linewidth=1, label='first')
    ax.fill(angles, vector1, alpha=0.25)
    ax.plot(angles, vector2, 'o-', linewidth=1, label='second')
    ax.fill(angles, vector2, alpha=0.25)
    ax.plot(angles, vector3, 'o-', linewidth=1, label='third')
    ax.fill(angles, vector3, alpha=0.25)
    ax.plot(angles, vector4, 'o-', linewidth=1, label='forth')
    ax.fill(angles, vector4, alpha=0.25)
    feature = ['Positive, grateful', 'Worry, fear, doubt', 'Embattled']
    # 填充颜色
    ax.fill(angles, vector4, alpha=0.25)
    # 添加每个特征的标签
    ax.set_thetagrids(angles * 180 / np.pi, feature)
    # 设置雷达图的范围
    ax.set_ylim(-100*math.pow(10, -14), 150*math.pow(10, -14))
    # 添加标题
    plt.title('Four stages of public mentality')
    # 添加网格线
    ax.grid(True)
    # 设置图例
    plt.legend(loc='best')
    # 显示图形
    plt.show()


def Visualize5D(vector_path):
    # Visualizing 5-D mix data using bubble charts
    # leveraging the concepts of hue, size and depth
    # v->积极,w->担忧,x->质疑,y->感激,z->严阵以待
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False
    with open(vector_path, mode='r', encoding='utf-8') as file:
        data = json.load(file)
        emotion_dict = {"积极": [], "担忧": [], "质疑": [], "感激": [], "严阵以待": [], "数量": []}
        for emotion in data:
            emotion_dict["积极"].append(emotion[0])
            emotion_dict["担忧"].append(emotion[1])
            emotion_dict["质疑"].append(emotion[2])
            emotion_dict["感激"].append(emotion[3])
            emotion_dict["严阵以待"].append(emotion[4])
        emotion_dict["数量"] = list(range(0, len(emotion_dict["积极"])))
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        fig.suptitle('心态散点图', fontsize=14)
        xs = emotion_dict["数量"]
        ys = emotion_dict["积极"]
        zs = emotion_dict["担忧"]
        # data_points = [(x, y, z) for x, y, z in zip(xs, ys, zs)]
        ss = emotion_dict["质疑"]
        ss = [50 * i for i in ss]
        colors = ['lime' if i != 0 else 'deeppink' for i in emotion_dict["感激"]]
        ax.scatter(xs, ys, zs, alpha=0.5, color=colors, s=ss, marker='o')
        ax.set_xlabel('数量')
        ax.set_ylabel('积极')
        ax.set_zlabel('担忧')
        plt.show()


def Visualize3D(dimension_path):
    # Visualizing 3-D numeric data with a bubble chart
    # length, breadth and size
    with open(dimension_path, mode='r', encoding='utf-8') as file:
        data = json.load(file)
        pos = pd.DataFrame()
        pos['X'] = data[:, 0]
        pos['Y'] = data[:, 1]
        pos['Z'] = data[:, 2]
        plt.scatter(pos['X'], pos['Y'], pos['Z'], alpha=0.4, edgecolors='y')
        plt.xlabel('Fixed Acidity')
        plt.ylabel('Alcohol')
        plt.title('Wine Alcohol Content - Fixed Acidity - Residual Sugar', y=1.05)
        plt.show()


if __name__ == "__main__":
    # plt.style.use('cyberpunk')
    plt.style.use("ggplot")
    # num_path = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\charts\num.txt"
    # data = load_data(num_path)
    # labels = data.keys()
    # quants = data.values()
    # print(labels)
    # print(quants)
    # draw_bar(labels, quants)
    # draw_Radar_chart()

    vector1 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\First\vector.txt"
    vector2 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Second\vector.txt"
    vector3 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Third\vector.txt"
    vector4 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Forth\vector.txt"
    Visualize5D(vector4)

    dimension1 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\First\3dimension.txt"
    # dimension2 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Second\3dimension.txt"
    # dimension3 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Third\3dimension.txt"
    # dimension4 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Forth\3dimension.txt"
    # Visualize3D(dimension1)
