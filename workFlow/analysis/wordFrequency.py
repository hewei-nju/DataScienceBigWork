# -*- coding: utf-8 -*-
import json
import math
from functools import reduce


def computeFrequency(data_path, frequency_path):
    with open(frequency_path, mode='w', encoding='utf-8') as file_obj:
        word_frequency = []
        with open(data_path, mode='r', encoding='utf-8') as file:
            data_list = json.load(file)
            for word_list in data_list:
                word_dict = {}
                for word in word_list:
                    if word not in list(word_dict.keys()):
                        word_dict[word] = 1.0
                    else:
                        word_dict[word] += 1.0
                # word_dict = sorted(word_dict.items(), key=lambda item: item[0], reverse=True)
                word_frequency.append(word_dict)
        # print(word_frequency)
        json.dump(word_frequency, file_obj, ensure_ascii=False)


def compute_tf(frequency_path, tf_path):
    with open(tf_path, mode='w', encoding='utf-8') as file_obj:
        with open(frequency_path, mode='r', encoding='utf-8') as file:
            word_frequency = json.load(file)
            for word_dict in word_frequency:
                nums = reduce(lambda x, y: x + y, word_dict.values())
                for key in word_dict.keys():
                    word_dict[key] /= nums
            json.dump(word_frequency, file_obj, ensure_ascii=False)


def compute_num_of_files(frequency_path, cnt_path):
    with open(cnt_path, mode='w', encoding='utf-8') as file_obj:
        with open(frequency_path, mode='r', encoding='utf-8') as file:
            word_frequency = json.load(file)
            for word_dict in word_frequency:
                for key in word_dict.keys():
                    word_dict[key] = 0.0
                    for dic in word_frequency:
                        if key in dic.keys():
                            word_dict[key] += 1.0
        json.dump(word_frequency, file_obj, ensure_ascii=False)


def compute_idf(cnt_path, idf_path):
    with open(idf_path, mode='w', encoding='utf-8') as file_obj:
        with open(cnt_path, mode='r', encoding='utf-8') as file:
            word_cnt = json.load(file)
            nums = len(word_cnt)
            for word_dict in word_cnt:
                for key in word_dict:
                    word_dict[key] = math.log10(nums / (word_dict[key] + 1))
        json.dump(word_cnt, file_obj, ensure_ascii=False)


def compute_tf_idf(tf_path, idf_path, tf_idf_path):
    with open(tf_idf_path, mode='w', encoding='utf-8') as file_obj:
        with open(tf_path, mode='r', encoding='utf-8') as file:
            with open(idf_path, mode='r', encoding='utf-8') as f:
                word_tf = json.load(file)
                word_idf = json.load(f)
                for i in range(0, len(word_tf)):
                    word_tf_dict = word_tf[i]
                    word_idf_dict = word_idf[i]
                    for key in word_tf_dict.keys():
                        word_tf_dict[key] = word_tf_dict[key] * word_idf_dict[key]
                json.dump(word_tf, file_obj, ensure_ascii=False)


def allFrequency(frequency_path, all_frequency_path):
    with open(all_frequency_path, mode='w', encoding='utf-8') as file_obj:
        with open(frequency_path, mode='r', encoding='utf-8') as file:
            freq = {}
            data = json.load(file)
            for word_dict in data:
                for key in word_dict.keys():
                    if key not in freq.keys():
                        freq[key] = word_dict[key]
                    else:
                        freq[key] += word_dict[key]
            freq = sorted(freq.items(), key=lambda item: item[1], reverse=True)
            json.dump(freq, file_obj, ensure_ascii=False)


if __name__ == "__main__":
    data1 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\First\data.txt'
    data2 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Second\data.txt'
    data3 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Third\data.txt'
    data4 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Forth\data.txt'

    frequency1 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\First\Frequency.txt'
    frequency2 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Second\Frequency.txt'
    frequency3 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Third\Frequency.txt'
    frequency4 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Forth\Frequency.txt'

    tf1 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\First\tf.txt'
    tf2 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Second\tf.txt'
    tf3 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Third\tf.txt'
    tf4 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Forth\tf.txt'

    cnt1 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\First\cnt.txt'
    cnt2 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Second\cnt.txt'
    cnt3 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Third\cnt.txt'
    cnt4 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Forth\cnt.txt'

    idf1 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\First\idf.txt'
    idf2 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Second\idf.txt'
    idf3 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Third\idf.txt'
    idf4 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Forth\idf.txt'

    tf_idf1 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\First\tf_idf.txt'
    tf_idf2 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Second\tf_idf.txt'
    tf_idf3 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Third\tf_idf.txt'
    tf_idf4 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Forth\tf_idf.txt'

    all_frequency1 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\First\all_frequency.txt'
    all_frequency2 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Second\all_frequency.txt'
    all_frequency3 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Third\all_frequency.txt'
    all_frequency4 = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Forth\all_frequency.txt'
    # computeFrequency(data4, frequency4)
    # compute_tf(frequency4, tf4)
    # compute_num_of_files(frequency4, cnt4)
    # compute_idf(cnt4, idf4)
    # compute_tf_idf(tf4, idf4, tf_idf4)
    allFrequency(frequency4, all_frequency4)



