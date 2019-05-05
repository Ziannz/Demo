# -*- coding: utf-8 -*-
import re

import scrapy
import json
from copy import deepcopy


class MeishiSpider(scrapy.Spider):
    name = 'meishi'
    allowed_domains = ['meituan.com','meituan.net']
    start_urls = ['https://www.meituan.com/ptapi/getprovincecityinfo/']

    def parse(self, response):
        item = {}
        citys_list = json.loads(response.text)
        for citys in citys_list:
            item['provinceName'] = citys['provinceName']
            if item['provinceName'] == '四川':
                for city in citys['cityInfoList']:
                    item['city_id'] = city['id']
                    item['city_name'] = city['name']
                    item['city_pinyin'] = city['pinyin']
                    item['acronym'] = city['acronym']
                    url = 'https://{}.meituan.com/meishi/'.format(item['acronym'])
#                   if item['city_name'] in '成都自贡攀枝花泸州德阳':
                    if item['city_name'] == '凉山':
                        # print(url)
                        yield scrapy.Request(url, meta={'item': deepcopy(item)}, callback=self.get_district)


    def get_district(self,response):
        '''
        获取每个区域的链接
        '''
        item = response.meta['item']
        data = response.text
        # 数据在网页中是以json格式出现的
        state = re.findall(r'.*?window._appState = (.*?);</script>.*?',data)[0]
        if state:
            try:
                dis_list = json.loads(state)['filters']['areas']
                for dis in dis_list:
                    item['dis_name'] =dis['name']
                    item['areaId'] = dis['id']
                    url = dis['subAreas'][0]['url']
        #           此处过滤显示区域个数
                    if item['dis_name'] == '西昌市':
                        yield scrapy.Request(url,meta={'item':deepcopy(item)},callback=self.get_article)
            except KeyError:
                print('取值区域错误，查看get_district函数')
        else:
            print('正则匹配区域错误，查看get_district函数')


    def get_article(self,response):
        '''
        所有数据均在原网页中以json格式出现
        匹配每个店铺的 poiId 拼接店铺链接 http://www.meituan.com/meishi/177925227/
        '''
        item = response.meta['item']
        data = response.text
        # 数据在网页中是以json格式出现的
        state = re.findall(r'.*?window._appState = (.*?);</script>.*?', data)[0]
        j_state = json.loads(state)
        if state:
            try:
                detail_list = j_state['poiLists']['poiInfos']
#               此处过滤显示店铺个数,单页15个
                for detail in detail_list:
                    id = detail['poiId']
                    url = 'http://www.meituan.com/meishi/{}/'.format(id)
                    yield scrapy.Request(url,meta={'item':item},callback=self.get_detail)

            except KeyError:
                print('取值店铺错误，查看get_article函数')
        else:
            print('正则匹配店铺错误，查看get_article函数')

    def get_detail(self,response):
        '''
        获取每个店铺的详细信息
        所有数据均在原网页中以json格式出现
        '''
        item = response.meta['item']
        data = response.text
        # 数据在网页中是以json格式出现的
        state = re.findall(r'.*?window._appState = (.*?);</script>.*?', data)[0]
        j_state = json.loads(state)
        try:
            item['title'] = j_state['detailInfo']['name'].strip()
            item['address'] = j_state['detailInfo']['address']
            item['phone'] = j_state['detailInfo']['phone']
            item['openTime'] = j_state['detailInfo']['openTime']
            item['lng'] = j_state['detailInfo']['longitude']
            item['lat'] = j_state['detailInfo']['latitude']
            item['image_urls'] = j_state['photos']['albumImgUrls']
            foods = j_state['recommended']
            if foods:
                for food in foods:
                    pass

            else:
                print('没有匹配到菜品')
        except:
            pass