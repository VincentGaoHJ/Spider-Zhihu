# Spider-Zhihu

## Description
* This is a project to crawl the [知乎](https://zhihu.com) website.
* The goal of the project is to achieve all the QAs (Question and Answer pairs) of a specific topic, and the input is the topic id and the total number of the questions under this topic.
* The code for interacting with [Zhihu API](https://github.com/strangestring/aiofetch) is provided by [@strangestring](https://github.com/strangestring), which provides asynchronous and multi-threading functions, greatly improving the crawl speed.


## Dependencies

```
import os
import csv
from zhihu_APIs import *
from data_getter import get_data
from w3lib.html import remove_tags
from headers_pool import HEADERS_POOL
```

## Operation

+ run `main.py` to start the overall work-flow.

The input is the topic name, topic id and the total number of the questions under this topic. For example:

```
{
topic_id : "19560026"
topic_name : "NLP"
topic_ansnum : 3896
}
```



## Output Format

* **NLP_topic.csv**
```
question_id	num	question_content
326383964	1	Bert预训练得到的是什么？
46464898	1	有人做术语抽取吗？
328252434	2	最大化互信息和最小化相对熵和交叉熵有什么区别?
19861557	4	文档向量直接通过距离聚类和通过LSI降维后再聚类效果会有怎么样的差异？
336521778	2	ImageCaption看图说话到底在找工作时投CV岗还是还是NLP岗呢？
315197632	12	公司里的算法工程师都用什么 IDE 或编辑器？
20162965	13	情感分类（sentiment classification）推荐使用什么算法和软件包？
19684735	2	自然语言搜索引擎 Lexxe 怎么样？
318731473	4	注意力机制为什么可以有效应对梯度消失问题？
```

* **NLP_answers.csv**
```
question_id	answer_id	question_context	answer_context
328929662	716582184	请问大家知道哪些中介语语料库?	你要是想专门找 西语母语者的...
52368821	130362228	知识图谱怎样入门？	到CNKI搜索一些比较不错期刊的中文综述，...
52368821	138745422	知识图谱怎样入门？	任何一个学科，重要的不是静态的知识本身
53643203	137622897	liblinear的特征选取是什么算法？	F值
20598511	68876891	自然语言是否是可计算的？怎么理解？	自然语言无法计算，自然语言是高级语言，也就是在我们的维度只是投影，无法全息计算，更加无法应用，只是偶尔能惊鸿一瞥！
330103469	731276217	图神经网络如何在自然语言处理中应用？	毕竟一直对graph neural network (GNN)的应用比较感兴趣。...
330103469	731798592	图神经网络如何在自然语言处理中应用？	用到representation的地方其实都有机会用到图...
330103469	724394005	图神经网络如何在自然语言处理中应用？	图神经网络可以简单的理解为深度神经网络和知识图谱的有机结合，所以在NLP领域也是其重要的应用领域，比如知识推理、知识问答等
330103469	740440288	图神经网络如何在自然语言处理中应用？	我之前也问过类似的问题，下面也有大佬的分享。meta-learning或者GNN在NLP哪些方向可以尝试的，或有什么推荐的论文？

```

