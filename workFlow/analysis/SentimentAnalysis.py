# -*- coding:utf-8 -*-
import json
import numpy as np
from sklearn.decomposition import PCA


def load_dict(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        return file.read().split(" ")


def get_tf_idf(catagory, tf_idf):
    dic = {"积极": r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\MentalityDictionary\positive.txt",
           "担忧": r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\MentalityDictionary\trepidation.txt",
           "质疑": r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\MentalityDictionary\incredulity.txt",
           "感激": r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\MentalityDictionary\grateful.txt",
           "严阵以待": r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\MentalityDictionary\embattled.txt"}
    res = 0.0
    keys = load_dict(dic[catagory])
    for key in tf_idf.keys():
        if key in keys:
            res += tf_idf[key]
    return res


def filter_Main_emotion(tf_idf_path, main_emotion_path):
    with open(tf_idf_path, mode='r', encoding='utf-8') as file:
        dic = json.load(file)
        data = []
        for tf_idf in dic:
            data_dic = {'积极': get_tf_idf('积极', tf_idf),
                        '担忧': get_tf_idf('担忧', tf_idf),
                        '质疑': get_tf_idf('质疑', tf_idf),
                        '感激': get_tf_idf('感激', tf_idf),
                        '严阵以待': get_tf_idf('严阵以待', tf_idf)}
            data.append(data_dic)
        with open(main_emotion_path, mode='w', encoding='utf-8') as file_obj:
            json.dump(data, file_obj, ensure_ascii=False)


def to_emotion_vector(main_emotion_path, vector_path):
    # 将情感向量化 vector[v, w, x, y, z]
    # v->积极,w->担忧,x->质疑,y->感激,z->严阵以待
    with open(main_emotion_path, mode='r', encoding='utf-8') as file:
        dic = json.load(file)
        data = []
        for emotion in dic:
            vector = [emotion['积极'], emotion['担忧'], emotion['质疑'], emotion['感激'], emotion['严阵以待']]
            vector = [100 * i for i in vector]
            data.append(vector)
        with open(vector_path, mode='w', encoding='utf-8') as file_obj:
            json.dump(data, file_obj, ensure_ascii=False)


def do_PCA(vector_path, dimension_path, dimension=3):
    with open(vector_path, mode='r', encoding='utf-8') as file:
        vectors = json.load(file)
        X = np.array(vectors)
        pca = PCA(n_components=dimension, copy=True, random_state=8)
        data = pca.fit_transform(X).tolist()
        print(pca.transform(X))
        with open(dimension_path, mode='w', encoding='utf-8') as file_obj:
            json.dump(data, file_obj)
        print(pca.fit_transform(X).shape)
        """
        m = len(vectors)
        X = np.array(vectors).T
        X = X - X.mean(axis=0)
        print(X)
        C = np.cov(X) / m
        print(C)
        lambdas, P = np.linalg.eig(C)
        print(lambdas)
        print(P)
        """


def integrateData(dimension_path, analysisResult_path):
    with open(dimension_path, mode='r', encoding='utf-8') as file:
        vectors = json.load(file)
        x = 0
        y = 0
        z = 0
        for vector in vectors:
            x += vector[0]
            y += vector[1]
            z += vector[2]
        data = [x, y, z]
        with open(analysisResult_path, mode='w', encoding='utf-8') as file_obj:
            json.dump(data, file_obj, ensure_ascii=False)


if __name__ == "__main__":
    tf_idf1 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\First\tf_idf.txt"
    tf_idf2 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Second\tf_idf.txt"
    tf_idf3 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Third\tf_idf.txt"
    tf_idf4 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Forth\tf_idf.txt"

    main_emotion1 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\First\main_emotion.txt"
    main_emotion2 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Second\main_emotion.txt"
    main_emotion3 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Third\main_emotion.txt"
    main_emotion4 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Forth\main_emotion.txt"

    vector1 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\First\vector.txt"
    vector2 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Second\vector.txt"
    vector3 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Third\vector.txt"
    vector4 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Forth\vector.txt"

    dimension1 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\First\3dimension.txt"
    dimension2 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Second\3dimension.txt"
    dimension3 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Third\3dimension.txt"
    dimension4 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Forth\3dimension.txt"

    dimension_1 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\First\1dimension.txt"
    # filter_Main_emotion(tf_idf1, main_emotion1)
    # filter_Main_emotion(tf_idf2, main_emotion2)
    # filter_Main_emotion(tf_idf3, main_emotion3)
    # filter_Main_emotion(tf_idf4, main_emotion4)
    # to_emotion_vector(main_emotion1, vector1)
    # to_emotion_vector(main_emotion2, vector2)
    # to_emotion_vector(main_emotion3, vector3)
    # to_emotion_vector(main_emotion4, vector4)
    dimension = 1
    # do_PCA(vector1, dimension1, dimension)
    # do_PCA(vector2, dimension2, dimension)
    # do_PCA(vector3, dimension3, dimension)
    do_PCA(vector1, dimension_1, dimension)

    # analysisResult1 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\First\analysisResult.txt"
    # analysisResult2 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Second\analysisResult.txt"
    # analysisResult3 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Third\analysisResult.txt"
    # analysisResult4 = r"F:\Pycharm_Git\DataScienceBigWork\main_workFlow\rm_data\Forth\analysisResult.txt"
    # integrateData(dimension1, analysisResult1)
    # integrateData(dimension2, analysisResult2)
    # integrateData(dimension3, analysisResult3)
    # integrateData(dimension4, analysisResult4)
