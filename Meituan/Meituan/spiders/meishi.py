# -*- coding: utf-8 -*-
import re
import math
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
            item['provinceName'] = citys['provinceName'].strip()
            if item['provinceName'] == '海南':
                for city in citys['cityInfoList']:
                    item['city_id'] = city['id']
                    item['city_name'] = city['name'].strip()
                    item['city_pinyin'] = city['pinyin']
                    item['acronym'] = city['acronym']
                    url = 'https://{}.meituan.com/meishi/'.format(item['acronym'])
#                   if item['city_name'] in '成都自贡攀枝花泸州德阳':
                    if item['city_name'] == '海口':
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
                    item['dis_name'] =dis['name'].strip()
                    item['areaId'] = dis['id']
                    url = dis['subAreas'][0]['url']
        #           此处过滤显示区域个数
                    if item['dis_name'] == '龙华区':
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
        # 判定页数
        totalCounts = j_state['poiLists']['totalCounts']
        total_page = math.ceil(totalCounts / 15)

        page = re.findall(r'.*?pn(.*?)/', response.url)
        if page:
            page = page[0]
        else:
            page = '1'
        print('正在爬取 %s 第 %s 页，共 %s 页' % (item['dis_name'], page, total_page))

        if state:
            try:
                detail_list = j_state['poiLists']['poiInfos']
                #               此处过滤显示店铺个数,单页15个
                for detail in detail_list:
                    id = detail['poiId']
                    url = 'http://www.meituan.com/meishi/{}/'.format(id)
                    yield scrapy.Request(url,meta={'item':deepcopy(item)},callback=self.get_detail)

            except KeyError:
                print('取值店铺错误，查看get_article函数')
        else:
            print('正则匹配店铺错误，查看get_article函数')


        if int(page) < int(total_page):
            if page == '1':url = response.url + 'pn2/'
            else:
                page = int(page) + 1
                url = re.sub('pn.*?/','pn{}/'.format(page),response.url)
            if page == 3:
                return None
            # print(url)
            yield scrapy.Request(url,meta={'item':deepcopy(item)},callback=self.get_article)



    def get_detail(self,response):
        '''
        获取每个店铺的详细信息
        所有数据均在原网页中以json格式出现
        '''
        item = response.meta['item']
        item['url'] = response.url
        data = response.text
        # 数据在网页中是以json格式出现的
        state = re.findall(r'.*?window._appState = (.*?);</script>.*?', data)
        if state:
            state = state[0]
        else:
            print('detail网页匹配出现问题117')
            return None
        j_state = json.loads(state)
        try:
            item['title'] = j_state['detailInfo']['name'].strip()
            item['title'] = re.sub(r'\W+', '', item['title'])
            item['address'] = j_state['detailInfo']['address']
            item['phone'] = j_state['detailInfo']['phone']
            item['openTime'] = j_state['detailInfo']['openTime']
            item['lng'] = j_state['detailInfo']['longitude']
            item['lat'] = j_state['detailInfo']['latitude']
            item['image_urls'] = j_state['photos']['albumImgUrls'][:3]
            # item['image_urls'] = [x.split('@')[0] for x in item['image_urls']]

            # 有套餐的情况
            if j_state['dealList']['deals']:
                foods = j_state['dealList']['deals']

            # 无套餐，有代金券的情况
            elif j_state['dealList']['vouchers']:
                foods = j_state['dealList']['vouchers']

            # 无套餐也无代金券的情况
            else:
                item['food_urls'] = []
                yield deepcopy(item)
                return None

            for food in foods:
                item['gname'] = food['title'].strip().split('，')[0]
                # 去除异常字符引起的新建文件错误
                item['gname'] = re.sub(r'\W+','',item['gname'])
                item['gprice'] = food['price']
                item['food_urls'] = [food['frontImgUrl'].split('@')[0].replace('208.126', '600.800')]
                id = food['id']
                url = 'http://www.meituan.com/meishi/d{}.html'.format(str(id))
                # if item['title'] == '疯狂烤翅（名店街店）':

                yield scrapy.Request(url, meta={'item': deepcopy(item)}, callback=self.get_meal)

        except KeyError:
            print('取值详情页错误，查看get_detail函数')

    def get_meal(self, response):
        item = response.meta['item']
        total_list = response.xpath("//table[@class='deal-menus']/tbody/tr")
        # print(total_list)

        if total_list:
            msg = []
            for total in total_list:
                detail = total.xpath("./td/text()").extract()
                if len(detail) > 3:
                    str = "{'4','%s','%s'}" % (detail[0], detail[2])
                    # print(str)

                    msg.append(str)
            item['info'] = msg
            # print(item['gname'],msg)
        # else:
        #     print('匹配失败')

        # 正则匹配，速度过慢
        # data = response.text
        # state = re.findall(r'.*?window._appState = (.*?);</script>.*?', data)[0]
        # j_state = json.loads(state)
        # meals = j_state['dealInfo']['menus']
        # menu = []
        # for meal in meals:
        #     if meal['type'] == 4:
        #         info = "{%s,%s,%s}" % (meal['type'],meal['content'],meal['specification'],)
        #         menu.append(info)
        # item['info'] = menu

        yield deepcopy(item)