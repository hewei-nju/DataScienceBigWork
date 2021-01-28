import os
import random
import json
from scripts import get_sina_PaperText


def getSizeOfFiles(file_folder):
    return len(os.listdir(file_folder))


def getSampleNews(sample_rate, start_date, end_date, path):
    """
    返回抽样的新闻字典
    :param sample_rate:样本比例
    :param start_date:开始日期
    :param end_date:结束日期
    :param path:文件夹路径
    :return:
    """
    date_list = get_sina_PaperText.getDateList(start_date, end_date)
    sample_news = dict()
    for date in date_list:
        dir_path = path + "\\" + date
        if os.path.exists(dir_path):
            nums = getSizeOfFiles(dir_path)
            file_list = []
            if nums >= 10:
                cnt = int(sample_rate * nums)
                sample_nums = random.sample(range(1, nums + 1), cnt)
                sample_nums.sort()
            else:
                sample_nums = [i for i in range(1, nums + 1)]
            for num in sample_nums:
                filename = str(num) + ".txt"
                file_list.append(filename)
            sample_news[date] = file_list
    return sample_news


if __name__ == "__main__":
    sina_filename = r"sina_sample_news.txt"
    sina_file_path = r'/workFlow/sina'
    rmNews_filename = "rmNews_sample_news.txt"
    rmNews_file_path = r'/workFlow-branch/sina'

    with open(sina_filename, mode='w', encoding='utf-8') as file:
        sampleNewsDict = getSampleNews(0.2, '2019-12-08', '2020-06-20', sina_file_path)
        json.dump(sampleNewsDict, file)
    with open(rmNews_filename, mode='w', encoding='utf-8') as file:
        sampleNewsDict = getSampleNews(0.2, '2019-12-08', '2020-06-20', rmNews_file_path)
        json.dump(sampleNewsDict, file)
    # print(getSampleNews(0.2, '2020-01-01', '2020-01-11', 'F:\Pycharm_Git\DataScienceBigWork\workFlow\\sina'))
