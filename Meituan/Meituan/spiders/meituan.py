# -*- coding: utf-8 -*-
import base64
import random
import time
import zlib
import scrapy
import datetime
import json
import re
from copy import deepcopy
# from scrapy_redis.spiders import RedisSpider


class MeituanSpider(scrapy.Spider):
    name = 'meituan'
    allowed_domains = ['meituan.com','meituan.net']
    start_urls = ['https://www.meituan.com/ptapi/getprovincecityinfo/']

    def parse(self, response):
        item = {}
        citys_list = json.loads(response.text)
#       此处过滤掉了信息[:1]
        for citys in citys_list:
            item['provinceName'] = citys['provinceName']
            if item['provinceName'] == '广西':
    #           此处过滤掉了信息[:2]
    #             for city in citys['cityInfoList'][:1]:
                for city in citys['cityInfoList']:
                    item['city_id'] = city['id']
                    item['city_name'] = city['name']
                    item['city_pinyin'] = city['pinyin']
                    url = "https://hotel.meituan.com/{}/".format(item['city_pinyin'])
                    # print(item,url)
                    # if item['city_name'] not in '重庆涪陵万州北碚':
                    # if item['city_name'] == '北碚':
                        # print(item['city_name'])
                        # print(url)
                    yield scrapy.Request(url,meta={'item':deepcopy(item)},callback=self.get_area)

    def get_area(self, response):
        item = response.meta['item']
        id_list = response.xpath('//div[@class="search-filter-classify"]/div[2]/div/a[1]/@href').extract()[1:]
        name_list = response.xpath('//div[@class="search-filter-classify"]/div[2]/div/a[1]/text()').extract()[1:]
        if len(id_list) < 2:
            id_list = response.xpath('//div[@class="search-filter-classify"]/div[1]/div/a[1]/@href').extract()[1:]
            name_list = response.xpath('//div[@class="search-filter-classify"]/div[1]/div/a[1]/text()').extract()[1:]
        # print(id_list,name_list)

        if len(id_list) == len(name_list):
#           此处过滤
            id_list = dict(zip(name_list,id_list))
            # id_list = dict(zip(name_list[:3],id_list[:2]))
            for area in id_list.keys():
                if '（' in area:
                    item['city_area'] = area.split('（')[0]
                else:
                    item['city_area'] = area
                area_id = id_list[area].split('/')[-2][2:]
                dtime = datetime.date.today().strftime('%Y%m%d')
                timestemp = '40' + str(int(time.time() * 1000))
                # url = 'https://ihotel.meituan.com/hbsearch/HotelSearch?utm_medium=pc&version_name=999.9&cateId=20&attr_28=129&uuid=9E5699C008293BA09214D3D1672F572663290AC624B5C7C0DD5716A3712B6C2A%401554436038066&cityId={0}&offset=0&limit=50&startDay={1}&endDay={2}&q=&sort=defaults&areaId={3}&X-FOR-WITH=py4LjkWjRGicIXFR3rh0Xu5HphZwfHdU7VlZnwFI3TnybDh2C2JB1ce0Y6xSHUF%2BSRtpf09%2FdP3qYA714fzgVDkAtwB3s5CzAsmtMA01E9n2Bc1qL0h%2FzticZ5BqbTAKJciwTKXm2wv9ztYdemU%2B5Q%3D%3D'.format(item['city_id'],time, time, area_id)
                url = 'https://ihotel.meituan.com/hbsearch/HotelSearch?utm_medium=pc&version_name=999.9&cateId=20&attr_28=129&uuid=9E5699C008293BA09214D3D1672F572663290AC624B5C7C0DD5716A3712B6C2A%{0}&cityId={1}&offset=0&limit=50&startDay={2}&endDay={3}&q=&sort=defaults&areaId={4}&X-FOR-WITH=py4LjkWjRGicIXFR3rh0Xu5HphZwfHdU7VlZnwFI3TnybDh2C2JB1ce0Y6xSHUF%2BSRtpf09%2FdP3qYA714fzgVDkAtwB3s5CzAsmtMA01E9n2Bc1qL0h%2FzticZ5BqbTAKJciwTKXm2wv9ztYdemU%2B5Q%3D%3D'.format(timestemp,item['city_id'],dtime, dtime, area_id)
                # print(item['city_area'],area_id,url)
                headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
                    "Cookie": "iuuid=ADE79379F7354FB5992E6A40E169720D01736880CBA4980D684AB8C6F5714693",
                }
                # yield scrapy.Request(url,headers=headers,callback=self.get_count,meta={'item':deepcopy(item)})
                yield scrapy.Request(url,callback=self.get_count,meta={'item':deepcopy(item)})
        else:
            print('get_city中 id_list 的值和 name_list 中的值不匹配')


    def get_count(self,response):
        item = response.meta['item']
        try:
            results = json.loads(response.text)['data']['searchresult']
        except KeyError:
            print(json.loads(response.text))
            print('get_count KeyError')
            return None
            # print(json.loads(response.text))
            # results = json.loads(response.text)['data']['recommend']['data']
#       此处过滤
        for result in results:
#         for result in results[:5]:
            name = result['name']
            item['name'] = re.sub(r'\•', '', name)
            item['addr'] = result['addr'].replace('\xa0','')
            item['addr'] = result['addr']
            item['lat'] = result['lat']
            item['lng'] = result['lng']
            item['poiid'] = result['poiid']


            time = datetime.date.today()
            today = time.strftime('%Y-%m-%d')
            tomorrow = datetime.date.fromordinal(time.toordinal() + 1).strftime('%Y-%m-%d')
            url = 'https://hotel.meituan.com/{0}/?ci={1}&co={2}'.format(item['poiid'],today,tomorrow)
            # print(url)
            yield scrapy.Request(url,callback=self.get_phone,meta={'item':deepcopy(item)})

        next_url = response.url
        totalcount = json.loads(response.text)['data']['totalcount']
        count = json.loads(response.text)['data']['count']
        offset = int(re.search(r'.*?offset=(.*?)&', next_url).group(1))

        if offset < totalcount and count == 50:
            offset += 50
            offset = 'offset=' + str(offset) + '&'
            next_url = re.sub(r'offset=(.*?)&', offset, next_url)
            yield scrapy.Request(next_url,callback=self.get_count,meta={'item':item})



    def get_phone(self, response):
        item = response.meta['item']
        item['phone'] = response.xpath('//li[@class="mb10 m20 fc6 fs14"]/div[2]/text()').extract_first()[3:]
        item['business'] = response.xpath('//div[@class="poi-hotelinfo-content clearfix"]/div[4]/dd/span/text()').extract_first()
        # print(item['business'])
        # print(item['phone'])
        url = 'https://ihotel.meituan.com/group/v1/poi/{}/imgs?'.format(item['poiid'])

        item['referer'] = response.url

        yield scrapy.Request(url,callback=self.get_image,meta={'item':deepcopy(item)})

    def get_image(self, response):
        item = response.meta['item']
        try:
            datas = json.loads(response.text)['data'][:2]
        except KeyError:
            return None

        url = []
        for data in datas:
            imgs = data['imgs']
            for img in imgs:
                # url = url.append(img['url'])
                # print(type(img['url']),img['url'])
                url.append(img['url'])
        if len(url) > 10:
            url = url[:10]
        images = re.sub('/w.h', '', '='.join(url)).split('=')
        images = [x if 'jpg' in x or 'png' in x or 'jpeg' in x else x + '.jpg' for x in images]
        images = [x.replace('..', '.') if '..' in x else x for x in images]
        images = [x.replace('jpeg.jpg', 'jpeg') if 'jpeg' in x else x for x in images]
        urls = []
        for image in images:
            b = image.split('/')[-1].split('.')
            c = b[1]
            r = '.' + '.'.join(b[1:])
            d = image.replace(r, '.' + c)
            urls.append(d)
        item['image_urls'] = urls
        # print(images)

        poiId = self.get_token(item['poiid'])

        today = datetime.date.today()
        today_start_time = int(time.mktime(time.strptime(str(today), '%Y-%m-%d'))) * 1000
        tomorrow = today + datetime.timedelta(days=1)
        today_end_time = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) * 1000
        # uuid = re.search(r'.*?"uuid":"(.*?)".*?',response.text).group(1)
        # print(uuid)
        times = '%40' + str(int(time.time() * 1000))
        url = 'https://ihotel.meituan.com/productapi/v2/prepayList?type=1&utm_medium=PC&version_name=7.3.0&poiId={}&start={}&end={}&uuid=090D706B8CF5DB7255BA1F6AAD52A089479FB1B89DD4CCF15B7B8FB6913E47EC{}&_token={}'.format(item['poiid'],today_start_time,today_end_time,times,poiId)

        # print(url)

        yield scrapy.Request(url,callback=self.get_detail,meta={'item':deepcopy(item)})
    #
    def get_detail(self, response):
        item = response.meta['item']
        goods = json.loads(response.text)['mergeList']['data']
        if goods:
            for good in goods:
                item['rname'] = good['roomCellName']
                item['rprice'] = str(good['lowestPrice'])[:-2]
                infos = good['roomCellDesc']
                try:
                    area = infos.split(' ')[0].split('㎡')
                    if '-' in area[0]:item['area'] = area[0].split('-')[1]
                    else:item['area'] = area[0]

                    number = infos.split(' ')[1]
                    if len(number) == 2:item['number'] = '2'
                    else:item['number'] = '1'

                    infos = infos.split(' ')[2]
                    if '有' in infos: item['infos'] = '1'
                    else: item['infos'] = '0'

                    if '有' in infos:item['jinfos'] = '有'
                    else:item['jinfos'] = '无'

                except IndexError:
                    continue

                images = []
                image_list = good['aggregateGoods']
                for image in image_list:
                    try:
                        # item['rdesc'] = image['prepayGood']['goodsName']
                        area = image['prepayGood']['breakfast']
                        if '不' in area or not area:
                            item['breakfast'] = '0'
                            item['jbreakfast'] = '不含早'
                        else:
                            item['breakfast'] = '1'
                            item['jbreakfast'] = area

                        # if not area:item['jbreakfast'] = '不含早'
                        # else: item['jbreakfast'] = area



                        img = image['prepayGood']['extInfo']['imgs']
                        images += img
                    except TypeError:
                        continue
                images = re.sub('/w.h', '', '='.join(images)).split('=')
                # item['room_urls'] = [x + 'jpg' if x.endswith('.') else x for x in images]
                rooms = [x + 'jpg' if x.endswith('.') else x for x in images]
                rooms = [x if x.endswith('.jpg') or x.endswith('.png') or not x else x + '.jpg' for x in rooms]
                rooms = [x.replace('jpeg.jpg', 'jpeg') if 'jpeg' in x else x for x in rooms]

                try:
                    try:
                        if not ''.join(rooms):item['room_urls'] = random.sample(item['image_urls'][1:],3)
                        else:item['room_urls'] = rooms
                    except ValueError:
                        if not ''.join(rooms):item['room_urls'] = [random.choice(item['image_urls'][1:])]
                        else:item['room_urls'] = rooms
                except IndexError:
                    item['room_urls'] = ''

                detail = [{"spec_name": "面积", "spec_Id": "","value": [{"spec_value_name":item['area'] + '㎡', "spec_name": "面积", "spec_value_Id": ""},]},
                          {"spec_name": "价格", "spec_Id": "","value": [{"spec_value_name":item['rprice'] + '元', "spec_name": "价格", "spec_value_Id": ""},]},
                          {"spec_name": "可住", "spec_Id": "","value": [{"spec_value_name":item['number'] + '人', "spec_name": "可住", "spec_value_Id": ""},]},
                          {"spec_name": "窗户", "spec_Id": "","value": [{"spec_value_name":item['jinfos'], "spec_name": "窗户", "spec_value_Id": ""},]},
                          {"spec_name": "早餐", "spec_Id": "","value": [{"spec_value_name":item['jbreakfast'], "spec_name": "早餐", "spec_value_Id": ""},]},
                          ]

                item['rdetail'] = json.dumps(detail,ensure_ascii=False)

                # if item['name'] == "U家公寓(成都理工店)" or item['name'] == "如家酒店(成都红星桥地铁站店)":
                #     print(item)
                #     yield deepcopy(item)

                # print(item)
                yield deepcopy(item)
            # print(item)

        else:
            print(item['poiid'], ':没有匹配到goods')
    #
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
            "rId": 100051,
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





