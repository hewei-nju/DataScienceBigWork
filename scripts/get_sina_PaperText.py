# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import re
import os
import datetime
import requests
import newspaper
from newspaper import Config, ArticleException
import json
import warnings


def getURL(url):
    """
    访问 url 网页， 获取网页内容
    :param url:
    :return:
    """
    headers = {
        "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      r"Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47 "
    }
    req = requests.get(url, headers=headers, timeout=30)
    # if req.raise_for_status() != 200:  # 判断是否返回异常
    # pass
    # if req.timeout > 10:
    #    pass
    req.encoding = 'utf-8'
    return req.text


def getNewsList(date):  # 默认传入的日期是 2020-01-10 这种格式
    """
    根据新浪新闻链接的特点，从而找出所有date这天的所有新闻链接，并封装成一个列表返回
    :param date:
    :return:
    """
    # http://news.sina.com.cn/head/news20201129am.shtml
    url = r'http://news.sina.com.cn/head/news' + date[0:4] + date[5:7] + date[8:10] + 'am.shtml'
    html = getURL(url)
    soup = BeautifulSoup(html, 'html.parser')
    findLink = re.compile(r'<a href="(.*?)" target="_blank">')
    linkList = []
    for item in soup.find_all('a', attrs={'target': '_blank'}):
        item = str(item)
        link = re.findall(findLink, item)
        if len(link) == 0:
            continue
        elif date in link[0]:
            linkList.append(link[0])
    return linkList


def remove_duplicates(linkList):
    """
    remove duplicates and unURL string
    :param linkList:
    :return:
    """
    links = []
    for item in linkList:
        match = re.search("(?P<url>https?://[^\s]+)", item)
        if match is not None:
            links.append((match.group("url")))
    return links


def filterNews(url, keyword):
    """
    对新闻进行筛选，通过关键词，以新闻标题为对象筛查
    通过user_agent和timeout来解决访问超时问题
    https://stackoverflow.com/questions/63061172/newspaper3k-api-article-download-failed-with-httpsconnectionpool-port-443-read
    :param url:
    :param keyword:
    :return:
    """
    user_agent = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    r"Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47 "
    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 30
    # Try-Except-Continue will skip to the next article in the For loop if there is an exception
    # https://github.com/codelucas/newspaper/issues/444  solve the bugs for not found url
    try:
        news = newspaper.Article(url, config=config)
        news.download()
        news.parse()
        for word in keyword:
            if word in news.title:
                # print(word)
                return True
        return False
    except ArticleException:
        return False
    # print(news.title)


def formatToJson(url, date):
    """
    把新闻文本变成json格式
    如：{"链接": "...", "标题": "...", "内容": "...", "日期": "...", "情感词": "..."}
    :param url:
    :param date:
    :return:
    """
    user_agent = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    r"Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47 "
    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 30
    news = newspaper.Article(url, language='zh', config=config)
    news.download()
    news.parse()
    jsonFormat = dict()
    jsonFormat["url"] = url
    jsonFormat["title"] = news.title
    jsonFormat["sina"] = news.text.replace("\n\n", '\n')
    jsonFormat["date"] = date
    jsonFormat["EmotionalWords"] = []
    jsonFormat["comments"] = []
    return jsonFormat


def saveFile(jsonFormat, path, filename):
    """
    将文章的内容以json格式存入txt文件
    :param jsonFormat:
    :param path:
    :param filename:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + r"/" + filename + ".txt", 'w', encoding='utf-8') as file_object:
        json.dump(jsonFormat, file_object, ensure_ascii=False)  # 中文编码问题
        # 虽然也是txt文本格式，但写入的是一个半结构化数据，有对象索引
        # file.write(str(jsonFormat))  # 写入的直接是字符串，没有对象索引


def getDateList(start_date, end_date):
    """
    返回所需日期的列表，日期格式为"2020-02-02"
    :param start_date:
    :param end_date:
    :return:
    """
    date_list = []
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    date_list.append(start_date.strftime('%Y-%m-%d'))
    while start_date < end_date:
        start_date += datetime.timedelta(days=1)
        date_list.append(start_date.strftime('%Y-%m-%d'))
    return date_list


def download_sina(datelist, destdir, keyword):
    """
    下载新闻
    :param keyword:
    :param datelist:
    :param destdir:
    :return:
    """
    for date in datelist:
        newsList = getNewsList(date)
        newsList = remove_duplicates(newsList)
        filename = 1
        for url in newsList:
            boolean = filterNews(url, keyword=keyword)
            # print(str(boolean))
            if boolean:
                # print(url)
                jsonFormat = formatToJson(url, date)
                saveFile(jsonFormat, destdir + r"/" + date, str(filename))
                filename += 1


if __name__ == "__main__":
    destdir = "sina"
    start_date = "2020-06-18"
    end_date = "2020-06-18"
    dateList = getDateList(start_date, end_date)
    KeyWordFile = "KeyWord.txt"
    keyword = []
    warnings.filterwarnings('ignore')
    with open(KeyWordFile, 'r') as file:
        words = file.read().split(" ")
    for word in words:
        if word != ' ' and word != '':
            keyword.append(word)
    # print(keyword)
    download_sina(dateList, destdir, keyword)
