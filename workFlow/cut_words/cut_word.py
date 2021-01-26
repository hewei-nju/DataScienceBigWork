import jieba.posseg as pseg
import json
import re
import os
from scripts.get_sina_PaperText import getDateList


def readFile(filename):
    """
    读取文件名问filename的文件的内容并返回
    :param filename:
    :return:
    """
    # 匹配除汉字外所有字符
    # regex = re.compile("[^\u4E00-\u9FFF]")
    # 匹配除汉字数字外所有字符
    regex = re.compile("[^\d\u4e00-\u9fa5]")
    with open(filename, 'rt', encoding="utf-8")as file:
        text = json.load(file)['sina']
        text = re.sub(regex, '\n', text).replace("\n\n", '\n')
        lines = text.split("\n")
        for line in lines:
            if len(line) < 1:
                lines.remove(line)
        if len(lines) > 0:
            return lines
        else:
            return None


def cutWord(lines, stop_words_file):
    """
    分词保存长度大于等于2的词
    去停用词
    将分好词的内容存到cut_word_file中
    分完词，我把文件格式还是设为json格式
    cut_words:对应于分词后的词语，一个列表
    true_words:对应于那些反映大众心态情绪的词，是一个字典
    内容是一个字典{'cut_words':['word1', 'word2', ...], 'true_words':{word<1>, word<2>, ...}}
    :param lines:
    :param cut_word_file:
    Returns word_dict
    """
    if lines != None:
        stop_words = loadStopWords(stop_words_file)
        word_dict = dict()
        cut_words = list()
        true_words = None
        for line in lines:
            words = pseg.cut(line)
            for item in words:
                # word是词，flag是词的性质
                if len(item.word) > 1 and item.word not in stop_words:
                    cut_words.append(item.word)
        word_dict['cut_words'] = cut_words
        word_dict['true_words'] = true_words
        return word_dict


def loadStopWords(filename):
    """
    加载自定义的stop_words
    :param filename:
    :return: 停用词set
    """
    stop_words = set()
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            stop_words.add(line.strip())
    return stop_words


def loadEmotionalWords(filename):
    """
    感觉这个地方有待讨论！！！
    加载自己定义好的情感词
    Args:
        filename:

    Returns:

    """


def saveFile(word_dict, path, filename):
    """
    :param word_dict: 切词后的内容
    :param path: 文件夹
    :param filename:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + r"/" + filename, 'w', encoding='utf-8') as file_object:
        json.dump(word_dict, file_object, ensure_ascii=False)  # 中文编码问题


def start_work(start_date, end_date, stop_words_file, row_file_folder, folder_path):
    """
    将日期从start_date -> end_date的新闻内容进行分词
    :param start_date:
    :param end_date:
    :param row_file_folder: 带分词文件存储的文件夹
    :param folder_path: 分词后数据存放的文件夹
    :return:
    """
    date_list = getDateList(start_date, end_date)
    for date in date_list:
        file_path = row_file_folder + '\\' + date
        if os.path.exists(file_path):
            files = os.listdir(file_path)
            for file in files:
                filename = file_path + '\\' + file
                lines = readFile(filename)
                word_dict = cutWord(lines, stop_words_file)
                path = folder_path + '\\' + date
                saveFile(word_dict, path, file)


if __name__ == '__main__':
    stop_words_file = 'scu_stop_words.txt'
    start_date = '2019-12-08'
    end_date = '2020-06-20'
    sina_row_file_folder = r'/workFlow/sina'
    rm_row_file_folder = r'/workFlow-branch/rm'
    sina_folder_path = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\cut_words\sina_cut_words'
    rm_folder_path = r'F:\Pycharm_Git\DataScienceBigWork\main_workFlow\cut_words\rm_cut_words'
    start_work(start_date, end_date, stop_words_file, rm_row_file_folder, rm_folder_path)
