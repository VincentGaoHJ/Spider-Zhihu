# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/7/26
@Author: Haojun Gao
@Description: 
"""

import os
import csv
import json
import urllib.request


def get_data(url):
    response = urllib.request.urlopen(url)
    res = response.read().decode("utf-8")
    data = json.loads(res)
    return data


def get_ans_num(question_id):
    count_url = "https://www.zhihu.com/api/v4/questions/" + str(question_id) + "?include=data[*].answer_count"
    data = get_data(count_url)
    answer_count = data["answer_count"]
    return answer_count


def write_csv(tuple):
    file_name = "hot_topic.csv"
    file_path = os.path.join(".\\data", file_name)
    with open(file_path, "a", encoding="utf-8-sig", newline='') as file:
        writer = csv.writer(file)
        writer.writerows([tuple])
        file.close()


def main(topic_id):
    root_url = "https://www.zhihu.com/api/v4/topics/" + topic_id + "/feeds/top_activity?&limit=20"
    is_end = False
    url = root_url
    question_set = set()
    while not is_end:
        data = get_data(url)
        is_end = data["paging"]["is_end"]
        print(data["paging"])
        url = data["paging"]["next"]
        num = len(data["data"])
        for i in range(num):
            if data["data"][i]["target"]["type"] != "answer":
                continue
            question_id = data["data"][i]["target"]["question"]["id"]
            question_title = data["data"][i]["target"]["question"]["title"]
            answer_count = get_ans_num(question_id)
            print(question_id, question_title)
            question_set.add((question_id, answer_count, question_title))

    for item in question_set:
        print(item)
        write_csv(item)


if __name__ == '__main__':
    # 话题：医学院
    topic_id = "19669154"
    main(topic_id)
