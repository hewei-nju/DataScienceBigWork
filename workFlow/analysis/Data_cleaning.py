# -*- coding:utf-8 -*-
from scripts.get_sina_PaperText import getDateList
import json
import os


def formatFile(folder_path, start, end, filename):
    date_list = getDateList(start, end)
    with open(filename, mode='w', encoding='utf-8') as file_obj:
        data = []
        if os.path.exists(folder_path):
            for date in date_list:
                folder = folder_path + "\\" + date
                if os.path.exists(folder):
                    fileList = os.listdir(folder)
                    for file in fileList:
                        file = folder + "\\" + file
                        with open(file, mode='r', encoding='utf-8') as f:
                            data.append(json.load(f)['cut_words'])
        json.dump(data, file_obj, ensure_ascii=False)
    print("Congratulate!")


def prepareNum(folder_path, num_path, start, end, per):
    data_list = getDateList(start, end)
    data = {}  # 按照月份存储数据 2019-12->2020-00-01
    if os.path.exists(folder_path):
        num = 0
        cnt = 0
        for date in data_list:
            cnt += 1
            folder = folder_path + "\\" + date
            file_num = 0
            if os.path.exists(folder):
                file_num = os.listdir(folder).__len__()
            if cnt % per == 0:
                data[cnt//per] = num
                num = file_num
            else:
                num += file_num
        data[cnt//per] = num
    with open(num_path, mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
    print("Congratulate!")


if __name__ == "__main__":
    folder_path = r"/main_workFlow/cut_words/rm_cut_words"
    filename1 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\First\data.txt"
    filename2 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Second\data.txt"
    filename3 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Third\data.txt"
    filename4 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Forth\data.txt"
    start1 = "2019-12-08"
    end1 = "2020-01-22"
    start2 = "2020-01-23"
    end2 = "2020-02-07"
    start3 = "2020-02-08"
    end3 = "2020-02-29"
    start4 = "2020-03-01"
    end4 = "2020-06-20"
    # formatFile(folder_path, start4, end4, filename4)
    num_path = r"/main_workFlow/charts/num.txt"
    prepareNum(folder_path, num_path, start1, end4, 14)
