# -*- coding: utf-8 -*-
import base64
import datetime
import random
import re
import math
import time
import zlib
from urllib.parse import urljoin

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
            if item['provinceName'] == '四川':
                for city in citys['cityInfoList']:
                    item['city_id'] = city['id']
                    item['city_name'] = city['name'].strip()
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
                uuid = json.loads(state)['$meta']['uuid']
                filters = json.loads(state)['filters']
                dis_list = filters['areas']
                for dis in dis_list:
                    item['dis_name'] =dis['name'].strip()
                    item['areaId'] = dis['id']
                    for cate in filters['cates']:
                        if cate['name'] in '日韩料理西餐东北菜川湘菜江浙菜粤菜西北菜京菜鲁菜云贵菜东南亚菜台湾/客家菜蒙餐新疆菜其他美食':
                            item['cateId'] = cate['id']
                            item['catename'] = cate['name']
                            # 获取 token
                            base_url = 'http://liangshan.meituan.com/meishi/api/poi/getPoiList?'
                            data = {
                                'cityName':item['city_name'],
                                'cateId':item['cateId'],
                                'areaId':item['areaId'],
                                'sort':'',
                                'dinnerCountAttrId': '',
                                'page':'1',
                                'userId':'',
                                'uuid':uuid,
                                'platform': '1',
                                'partner': '126',
                                'originUrl': response.url,
                                'riskLevel': '1',
                                'optimusCode': '1',
                            }
                            # poiId = self.get_token(data)
                            # url = urljoin(base_url,data)
                            print(data)


            except KeyError:
                print('取值区域错误，查看get_district函数')
        else:
            print('正则匹配区域错误，查看get_district函数')


    def get_article(self,response):
        '''
        所有数据均在原网页中以json格式出现
        匹配每个店铺的 poiId 拼接店铺链接 http://www.meituan.com/meishi/177925227/
        '''
        # item = response.meta['item']
        # 判定页数
        # totalCounts = j_state['poiLists']['totalCounts']
        # total_page = math.ceil(totalCounts / 15)

        # page = re.findall(r'.*?pn(.*?)/', response.url)
        # if page:page = page[0]
        # else:page = '1'
        # print('正在爬取 %s 第 %s 页，共 %s 页' % (item['dis_name'], page, total_page))
        #
        #
        #
        #
        #
        #
        # if int(page) < int(total_page):
        #     if page == '1':url = response.url + 'pn2/'
        #     else:
        #         page = int(page) + 1
        #         url = re.sub('pn.*?/','pn{}/'.format(page),response.url)
        #     if page == 4:
        #         return None
        #     # print(url)
        #     yield scrapy.Request(url,meta={'item':deepcopy(item)},callback=self.get_article)



    def get_detail(self,response):
        '''
        获取每个店铺的详细信息
        所有数据均在原网页中以json格式出现
        '''
        if '验证中心' in response.text:
            print('出现验证码！')
            return None

        item = response.meta['item']
        item['url'] = response.url
        data = response.text
        # 数据在网页中是以json格式出现的
        state = re.findall(r'.*?window._appState = (.*?);</script>.*?', data)
        if state:
            state = state[0]
        else:
            print('网页数据为:',response.url)
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


    def get_token(self,poiId):

        times = datetime.date.today()
        today = times.strftime('%Y-%m-%d')
        tomorrow = datetime.date.fromordinal(times.toordinal() + 1).strftime('%Y-%m-%d')
        url = 'https://hotel.meituan.com/{0}/?ci={1}&co={2}'.format(poiId, today, tomorrow)
        today = datetime.date.today()
        start = int(time.mktime(time.strptime(str(today), '%Y-%m-%d'))) * 1000
        tomorrow = today + datetime.timedelta(days=1)
        end = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) * 1000

        string = 'end={}&poiId={}&start={}&type=1&utm_medium=PC&uuid=9E5699C008293BA09214D3D1672F572663290AC624B5C7C0DD5716A3712B6C2A&version_name=7.3.0'.format(end, start, poiId)
        gz = zlib.compress(string.encode())
        base_string = base64.encodestring(gz).decode()
        # print(base_string)
        ts = int(time.time() * 1000)
        token_dict = {
            "rId": 100900,
            "ts": ts,
            "cts": ts + 1000000,
            "brVD": [1920, 290],
            "brR": [[1920, 1080], [1920, 1040], 24, 24],
            "bI": [url, ''],
            "mT": [],
            "kT": [],
            "aT": [],
            "tT": [],
            "sign": base_string,
        }
        json_string = json.dumps(token_dict)
        token_string = zlib.compress(json_string.encode())
        token_base = base64.encodebytes(token_string).decode()
        # print(token_base)
        # encodebytes有默认的换行符和空格 replace('\r', '').replace('\n', '').replace('\t', '') 去掉
        return token_base.replace('\r', '').replace('\n', '').replace('\t', '')