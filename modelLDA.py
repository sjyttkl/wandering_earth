# -*- coding: utf-8 -*-
"""
Created on Thur Feb  14 11:49:02 2019

@author: songdongdong
"""

"""
DA是一种非监督机器学习技术，可以用来识别大规模文档集（document collection）或语料库（corpus）中潜藏的主题信息。
影评虽然不多，但是用起来也不是不行。通过LDA提取topic，我们就可以根据关键词对这些主题进行提炼，
能够把三个分数段的影评很好的聚集起来
https://mbd.baidu.com/newspage/data/landingshare?pageType=1&isBdboxFrom=1&context=%7B"nid"%3A"news_9960210956876342565"%2C"sourceFrom"%3A"bjh"%7D
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import jieba
import pyLDAvis
import pyLDAvis.sklearn

# 读取评论数据
hComments = []
with open('hComments.txt', 'r', encoding="utf-8") as f1:
    for line in f1:
        hComments.append(" ".join(jieba.cut(line)))

mComments = []
with open('mComments.txt', 'r', encoding="utf-8") as f2:
    for line in f2:
        mComments.append(" ".join(jieba.cut(line)))
        
lComments = []
with open('lComments.txt', 'r', encoding="utf-8") as f3:
    for line in f3:
        lComments.append(" ".join(jieba.cut(line)))

# 合并评论数据
comments = hComments + mComments + lComments
df = pd.DataFrame(comments)

# 关键词提取和向量转化
tfVectorizer = CountVectorizer(strip_accents = 'unicode',
                                max_features = 1000,
                                max_df = 0.5,
                                min_df = 10
                                )
tf = tfVectorizer.fit_transform(df[0]) #这里取出第一列进行计算  tf
# print(tfVectorizer.vocabulary_)
# print(tfVectorizer.get_feature_names())
# 初始化lda
lda = LatentDirichletAllocation(n_topics = 3,
                                max_iter =50,
                                learning_method = 'online',
                                learning_offset = 50,
                                random_state = 0)
lda.fit(tf)  # 训练

# 可视化lda
data = pyLDAvis.sklearn.prepare(lda, tf, tfVectorizer)
pyLDAvis.show(data)