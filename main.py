# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/7/28
@Author: Haojun Gao
@Description: 
"""

from get_topic import get_topic
from get_answer import get_answer

# 自然语言处理 NLP 19560026 3896
# 漫威 Marvel 19647712 24692
# NBA NBA 19552439 31495
# 中国近代史 ZhongGuoJinDaiShi 19574423 19138

if __name__ == '__main__':

    topic_id = "19552439"
    topic_name = "NBA"
    topic_ansnum = 31495

    get_topic(topic_id, topic_name, topic_ansnum)

    get_answer(topic_id, topic_name)