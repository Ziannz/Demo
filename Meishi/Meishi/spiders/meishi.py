# -*- coding: utf-8 -*-
import scrapy


class MeishiSpider(scrapy.Spider):
    name = 'meishi'
    allowed_domains = ['meituan.com']
    start_urls = ['http://meituan.com/']

    def parse(self, response):
        pass
        pass
