# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/7/26
@Author: Haojun Gao
@Description: 
"""

import os
import csv
from zhihu_APIs import *
from data_getter import get_data
from w3lib.html import remove_tags
from headers_pool import HEADERS_POOL

# default args
PROCESS_NUM = 4
MAX_PROCESS_NUM = 8
FLOOD_DISCHARGE_RATIO = 0.3
FLOODPLAIN_RATIO = 0.1
HEADERS_POOL = HEADERS_POOL


def load_question(topic_id):
    file_name = str(topic_id) + "_topic.csv"
    file_path = os.path.join("./data", file_name)

    data = []
    with open(file_path, encoding="utf-8-sig") as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        for row in csv_reader:  # 将csv 文件中的数据保存到birth_data中
            data.append(row)

    return data


def get_answer(topic_id, topic_name):
    # 不考虑云端数据变化,step小于limit时,取样必然有重叠
    time.perf_counter()  # 计时
    zhi = ZhiHu()
    func = zhi.questions.answers

    question_list = load_question(topic_name)
    total_num = len(question_list)
    print("[获取回答] ===== 正在准备请求 {} 共有问题数 {} =====".format(topic_name, total_num))
    i = 0
    answer_all = []
    fetch_body = []
    for question in question_list:
        i += 1
        question_id = question[0]
        question_ansnum = int(question[1])

        fetch_body.append({"identifier": question_id,
                           "query_args": ["content"],
                           "range": [0, question_ansnum]})
        # break

    print("[获取回答] ===== 正在请求数据 {} 共有问题数 {} =====".format(topic_name, total_num))
    res = get_data(fetch_body, func, process_num=PROCESS_NUM,
                   max_process_num=MAX_PROCESS_NUM,
                   flood_discharge_ratio=FLOOD_DISCHARGE_RATIO,
                   floodplain_ratio=FLOODPLAIN_RATIO,
                   headers_pool=HEADERS_POOL)

    # print(res)

    print("[获取回答] ===== 正在处理数据 {} 共有问题数 {} =====".format(topic_name, total_num))
    i = 0
    for question_id, question_result in res.items():
        i += 1
        answer_list = question_result["data"]
        if i % 1000 == 0:
            print("[处理问题 {} / {}]".format(i, total_num), question_id)
        for item in answer_list:
            answer_id = item["id"]
            raw_ans = item["content"]
            question_content = item["question"]["title"]
            answer_content = remove_tags(raw_ans)
            answer_all.append((question_id, answer_id, question_content, answer_content))

    print("[获取回答] ===== 正在保存数据 {} 共有问题数 {} =====".format(topic_name, total_num))
    file_name = str(topic_name) + "_answers.csv"
    file_path = os.path.join("./data", file_name)
    with open(file_path, "a", encoding="utf-8-sig", newline='') as file:
        writer = csv.writer(file)
        for item in answer_all:
            writer.writerows([item])


if __name__ == '__main__':

    topic_id = "19574423"
    topic_name = "ZhongGuoJinDaiShi"

    get_answer(topic_id, topic_name)
