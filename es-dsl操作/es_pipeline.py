#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/9 9:00
# @Author  : ZhangChaowei
from es_types import ArticleType
from elasticsearch_dsl.connections import connections
es = connections.create_connection(ArticleType._doc_type.using)


def gen_suggestion(index, info_tuple):
    # 根据字符串生成搜索建议组
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            # 调用es的analyze接口分析字符串
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter': ["lowercase"]}, body=text)
            analyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = analyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})
    return suggests


# es测试版本
class ElasticsearchPipeline(object):
    # 将数据写入到es中
    def process_item(self):
        article = ArticleType()
        article.title = "Python的MySQL数据库操作"
        article.body = "MySQL的快捷操作，数据库的处理，ORM操作..."
        article.tags = "快速的数据读写"
        article.published_from = "2019-1-10"
        article.lines = "5519147"
        article.suggestion = gen_suggestion(ArticleType._doc_type.index, ((article.title, 10), (article.body, 7)))
        article.save()


if __name__ == '__main__':
    a = ElasticsearchPipeline()
    a.process_item()

















