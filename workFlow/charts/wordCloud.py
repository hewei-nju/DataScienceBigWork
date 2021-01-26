from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
import numpy as np

# 数据
filename = r'C:\Users\ThinkPad\PycharmProjects\dataScience\SortedWordFrecuency.txt'
words = open(filename, encoding='utf-8').read()


# 渲染图
def wordcloud_base() -> WordCloud:
    c = (
        WordCloud()
            .add("", words, word_size_range=[20, 100], shape='diamond')  # SymbolType.ROUND_RECT
            .set_global_opts(title_opts=opts.TitleOpts(title='WordCloud词云'))

    )
    return c


# 生成图
wordcloud_base().render('词云图.html')
