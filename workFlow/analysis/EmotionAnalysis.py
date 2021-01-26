import csv
import functools
from collections import Counter
import datetime
import jieba
import json
import os
import pandas as pd
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams
import matplotlib as plt
from emotionDirectory import directory
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
rcParams['font.family'] = 'sans-serif '
rcParams['font.sans-serif'] = ['Tahoma']

path = r'C:\Users\ThinkPad\PycharmProjects\dataScience\nocut'
targetpath = r'C:\Users\ThinkPad\PycharmProjects\dataScience\dailyFrequency'


def comparetime(a, b):
    a = str(a).split('.')[0]
    b = str(b).split('.')[0]
    a = [int(i) for i in str(a).split('-')]
    b = [int(i) for i in str(b).split('-')]
    timea = datetime.date(a[0], a[1], a[2])
    timeb = datetime.date(b[0], b[1], b[2])
    if (timea.__ge__(timeb)):
        return 1
    return -1


def getDailyFrequecy():
    for i in os.listdir(path):
        data = ""
        repath = path + '\\' + str(i)
        for j in os.listdir(repath):
            datapath = repath + '\\' + str(j)
            data += json.loads(open(datapath, encoding='utf-8').read())['sina']
        cut_words = ""
        all_words = ""

        data = open(datapath, encoding='utf-8').read()
        data = json.loads(data)['sina']
        newdata = ""
        for line in data.split('\n'):
            # line.strip('\n')
            seg_list = jieba.cut(line, cut_all=False)
            # print(" ".join(seg_list))
            cut_words = (" ".join(seg_list))
            newdata += cut_words + '\n'
            all_words += cut_words

        all_words = all_words.split()

        c = Counter()
        for x in all_words:
            if len(x) > 1 and x != '\r\n':
                c[x] += 1

        name = targetpath + '\\' + str(i)
        cv = open(name, 'w', encoding='utf-8')
        w = csv.writer(cv)
        w.writerow(["词语", "频率"])
        j = 0
        for (k, v) in c.most_common(len(c)):
            w.writerow([str(k), str(v)])
            j += 1
            if j > 10000:
                break
        cv.close()


def mainAnalys():
    m = directory()
    d = dict()
    count = 0
    p = os.listdir(targetpath)
    prei = ''
    wordnum = 0
    p = sorted(p, key=functools.cmp_to_key(comparetime()))
    for i in p:
        name = targetpath + '\\' + str(i)
        c = pd.read_csv(name)
        if (count == 0):
            d[i[0:10]] = [0, 0, 0, 0]
            prei = i
        for pair in c.values:
            wordnum += int(pair[1])
            for j in range(0, 4):
                for word in directory.getdirectory(self=directory)[j]:
                    word = str(word)
                    emotionword = str(pair[0])
                    if (emotionword == word or emotionword.__contains__(word) or word.__contains__(emotionword)):
                        d[prei[0:10]][j] += pair[1]
                        continue
        count += 1
        if (count == 14 or i == '2020-06-20'):
            d[prei[0:10]] = [int(x) / wordnum for x in d[prei[0:10]]]
            wordnum = 0
            count = 0
    f = open(r'C:\Users\ThinkPad\PycharmProjects\dataScience\output.csv', 'w')
    c = csv.writer(f)
    c.writerow(["日期", "积极,有信心,充满希望", "担忧,紧张,质疑", "不松懈，对已取得的成功不放松警惕", "感激，祝福，加油，支持"])
    for i in d:
        l = d[i]
        c.writerow([i[0:10], l[0], l[1], l[2], l[3]])


def showpaint():
    data = pd.read_csv(r'C:\Users\ThinkPad\PycharmProjects\dataScience\output.csv', encoding='GBK')
    dic = dict()
    for i in data.values:
        dic[i[0][6:]] = i[1:5]
    list = [0, 0, 0, 0]
    for i in dic:
        for j in range(0, 4):
            list[j] += float(dic[i][j])
    print(list)
    averagestrength = sum(list) / (4 * len(dic))
    lst = [averagestrength / (i / len(dic)) for i in list]
    x = dic.keys()
    font = FontProperties(fname=r'C:\Windows\Fonts\simsun.ttc')
    y1 = [dic[i][0] for i in x]
    y2 = [dic[i][1] for i in x]
    y3 = [dic[i][2] for i in x]
    y4 = [dic[i][3] for i in x]
    x = [i for i in x]
    ax = plt.subplot(111)
    ax.plot(x, y1, label='积极,有信心,充满希望', )
    ax.plot(x, y2, label='担忧,紧张,质疑')
    ax.plot(x, y3, label='不松懈，对已取得的成功不放松警惕')
    ax.plot(x, y4, label='感激，祝福，加油，支持')
    ax.legend(prop=font)
    plt.title('疫情下的大众心态变化', fontproperties=font)
    plt.xlabel('时间', fontproperties=font)
    plt.ylabel('强度', fontproperties=font)
    plt.show()


showpaint()
