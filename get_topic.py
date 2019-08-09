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
from headers_pool import HEADERS_POOL

# default args
PROCESS_NUM = 4
MAX_PROCESS_NUM = 8
FLOOD_DISCHARGE_RATIO = 0.3
FLOODPLAIN_RATIO = 0.1
HEADERS_POOL = HEADERS_POOL


def get_topic(topic_id, topic_name, topic_ansnum):
    # 不考虑云端数据变化,step小于limit时,取样必然有重叠
    time.perf_counter()  # 计时
    zhi = ZhiHu()
    func = zhi.topic.timeline_question

    print("[获取问题] ===== 正在获取数据 {} 共有回答数 {} =====".format(topic_name, topic_ansnum))

    fetch_dict = [{"identifier": topic_id,
                   "query_args": ["answer_count"],
                   "range": [0, topic_ansnum]}]

    res = get_data(fetch_dict, func, process_num=PROCESS_NUM,
                   max_process_num=MAX_PROCESS_NUM,
                   flood_discharge_ratio=FLOOD_DISCHARGE_RATIO,
                   floodplain_ratio=FLOODPLAIN_RATIO,
                   headers_pool=HEADERS_POOL)

    print("[获取问题] ===== 正在处理回答 {} 共有回答数 {} =====".format(topic_name, topic_ansnum))

    data = res[topic_id]["data"]
    num = len(data)
    question_set = set()
    for item in data:
        question_id = item["target"]["id"]
        question_title = item["target"]["title"]
        ans_count = item["target"]["answer_count"]
        if ans_count == 0:
            continue
        question_set.add((question_id, ans_count, question_title))

    print("[获取问题] ===== 正在保存回答 {} 共有回答数 {} =====".format(topic_name, topic_ansnum))

    file_name = str(topic_name) + "_topic.csv"
    file_path = os.path.join("./data", file_name)
    with open(file_path, "a", encoding="utf-8-sig", newline='') as file:
        writer = csv.writer(file)
        for item in question_set:
            writer.writerows([item])


if __name__ == '__main__':
    # 自然语言处理 19560026 3896
    # 漫威 19647712 24692
    # NBA 19552439 31495
    # 中国近代史 19574423 19138
    topic_id = "19574423"
    topic_name = "ZhongGuoJinDaiShi"
    topic_ansnum = 19138

    get_topic(topic_id, topic_name, topic_ansnum)
