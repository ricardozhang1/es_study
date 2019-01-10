#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 15:15
# @Author  : ZhangChaowei

from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, analyzer, InnerObjectWrapper, Completion, Keyword, Text, Integer
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=['localhost'])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_max_word = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class ArticleType(DocType):
    suggestion = Completion(analyzer=ik_max_word)
    title = Text(analyzer='ik_max_word')
    body = Text(analyzer='ik_max_word')
    tags = Keyword()
    published_from = Date()
    lines = Integer()

    class Meta:
        index = 'jobbole'
        doc_type = "article"


if __name__ == '__main__':
    # create the mappings in elasticsearch
    ArticleType.init()




