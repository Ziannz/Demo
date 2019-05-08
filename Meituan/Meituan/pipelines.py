# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import time
import os,csv
import random
from copy import deepcopy
import requests

from scrapy.utils.defer import mustbe_deferred
from scrapy.utils.request import request_fingerprint
from twisted.internet.defer import Deferred



class MeituanPipeline(object):
    def process_item(self, item, spider):
        return item

class MyImagesPipeline(ImagesPipeline):
    # 下载器
    def get_media_requests(self,item,info):
        if item['room_urls']:
            try:
                # 下载所有图片
                # for room_url in item['room_urls']:
                #     referer = room_url
                #     yield Request(room_url,meta={'item':deepcopy(item)})

                # 下载单张图片
                room_url = random.choice(item['room_urls'])
                referer = room_url
                yield Request(room_url, meta={'item': deepcopy(item)}, headers={'Referer': item['referer']},dont_filter=True)

            except ValueError as e:
                resp = requests.get(item['room_urls']).content
                paths = 'E://' + self.filename
                # print(paths,item['room_urls'],sep='\n')
                try:
                    with open(paths, 'wb') as f:
                        f.write(resp)
                except FileNotFoundError:
                    files = '/'.join(paths.split('/')[:-1])
                    if (not os.path.exists(files)):
                        os.makedirs(files)
                        with open(paths, 'wb') as f:
                            f.write(resp)
                print('e',item)
                # pass


    # 文件路径
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        # folder = item['name'] + '/' + item['rname']
        folder = item['provinceName'] + '/' + item['city_name'] + '/' + item['city_area'] + '/' +  item['name'] + '/' +  item['rname']
        folder_strip = folder.strip()
        # image_guid = item['rname'] + str(time.time())[-7:] + '.jpg'
        image_guid = '1' + request.url.split('/')[-1]
        self.filename = u'Meituan/{0}/{1}'.format(folder_strip, image_guid)
        return self.filename

    # 获取结果
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            # print('room',results,item)

            url = random.choice(item['image_urls'])
            resp = requests.get(url).content
            paths = 'E://' + self.filename
            print(paths,item['room_urls'],sep='\n')
            try:
                with open(paths,'wb') as f:
                    f.write(resp)
            except FileNotFoundError:
                files = '/'.join(paths.split('/')[:-1])
                if(not os.path.exists(files)):
                    os.makedirs(files)
                    with open(paths, 'wb') as f:
                        f.write(resp)
            # raise DropItem('Item contains no images')
        # print(item['rname'],results)
        item['room_paths'] = image_paths
        return item
        # print(results)

class MImagesPipeline(ImagesPipeline):
    # 下载器
    def get_media_requests(self,item,info):
        try:
            # 下载所有图片
            # for image_url in item['image_urls']:
            #     referer = image_url
            #     yield Request(image_url,meta={'item':deepcopy(item)})

            # 下载单张图片
            room_url = item['image_urls'][0]
            referer = room_url
            yield Request(room_url, meta={'item': deepcopy(item)},headers={'Referer':item['referer']},dont_filter=True)

        except ValueError:
            print('image中ValueError错误')

    # 文件路径
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        # folder = item['name']
        folder = item['provinceName'] + '/' + item['city_name'] + '/' + item['city_area'] + '/' +  item['name']
        folder_strip = folder.strip()
        # 爬多张图片时用的文件名
        # image_guid = item['name'] + str(time.time())[-7:] + '.jpg'
        image_guid = '1' + request.url.split('/')[-1]
        filename = u'Meituan/{0}/{1}'.format(folder_strip, image_guid)
        return filename

    # 获取结果
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            print('image',results,item)
            raise DropItem('Item contains no images')

        return item



class Pipeline_ToTXT(object):

    def process_item(self, item, spider):
        # csv文件的位置,无需事先创建
        filename = 'E:/Meituan' + '/' + item['provinceName'] + '/' + item['city_name'] + '/' + item['city_area'] + '/' +  item['name']
        if(not os.path.exists(filename)):
            os.makedirs(filename)

        if item['name']:
            ffilename = filename + '/' + '店铺名称.txt'
            with open(ffilename,'w',encoding='utf-8') as f:
                f.write(item['name'])

        if item['addr']:
            ffilename = filename + '/' + '店铺地址.txt'
            with open(ffilename, 'w',encoding='utf-8') as f:
                f.write(item['addr'])

        if item['lat']:
            ffilename = filename + '/' + '纬度.txt'
            with open(ffilename,'w',encoding='utf-8') as f:
                f.write(str(item['lat']))

        if item['lng']:
            ffilename = filename + '/' + '经度.txt'
            with open(ffilename,'w',encoding='utf-8') as f:
                f.write(str(item['lng']))

        if item['phone']:
            ffilename = filename + '/' + '电话.txt'
            with open(ffilename,'w',encoding='utf-8') as f:
                f.write(str(item['phone']))

        if item['business']:
            ffilename = filename + '/' + '入住时间.txt'
            with open(ffilename, 'w',encoding='utf-8') as f:
                if item['business']:
                    data = item['business']
                else:
                    data = '入住时间: 14:00以后  离店时间: 12:00之前'
                f.write(data)

        rfilename = filename + '/' + item['rname']
        if(os.path.exists(rfilename)):
            if item['rprice']:
                ffilename = filename + '/' + item['rname'] + '/' +'价格.txt'
                with open(ffilename, 'w',encoding='utf-8') as f:
                    f.write(str(item['rprice']))

            if item['area']:
                ffilename = filename + '/' + item['rname'] + '/' +'面积.txt'
                with open(ffilename, 'w',encoding='utf-8') as f:
                    f.write(item['area'])

            if item['number']:
                ffilename = filename + '/' + item['rname'] + '/' +'可住.txt'
                with open(ffilename, 'w',encoding='utf-8') as f:
                    f.write(item['number'])

            if item['infos']:
                ffilename = filename + '/' + item['rname'] + '/' +'窗户.txt'
                with open(ffilename, 'w',encoding='utf-8') as f:
                    f.write(item['infos'])

            if item['rdetail']:
                ffilename = filename + '/' + item['rname'] + '/' + '详细信息.txt'
                with open(ffilename, 'w',encoding='utf-8') as f:
                    f.write(item['rdetail'])

            if item['breakfast']:
                ffilename = filename + '/' + item['rname'] + '/' +'早餐.txt'
                with open(ffilename, 'w',encoding='utf-8') as f:
                    f.write(item['breakfast'])

        print(item['name'],'存储完成')

        return item


class MeishiImagesPipeline(ImagesPipeline):

    # def _process_request(self, request, info):
    #     fp = request_fingerprint(request)
    #     cb = request.callback or (lambda _: _)
    #     eb = request.errback
    #     request.callback = None
    #     request.errback = None
    #
    #     # Return cached result if request was already seen
    #     # if fp in info.downloaded:
    #     #     return defer_result(info.downloaded[fp]).addCallbacks(cb, eb)
    #     #
    #     # # Otherwise, wait for result
    #     wad = Deferred().addCallbacks(cb, eb)
    #     info.waiting[fp].append(wad)
    #
    #     # info.waiting[fp].append(wad)
    #     #
    #     # # Check if request is downloading right now to avoid doing it twice
    #     # if fp in info.downloading:
    #     #     return wad
    #
    #     # Download request checking media_to_download hook output first
    #     info.downloading.add(fp)
    #     dfd = mustbe_deferred(self.media_to_download, request, info)
    #     dfd.addCallback(self._check_media_to_download, request, info)
    #     dfd.addBoth(self._cache_result_and_execute_waiters, fp, info)
    #     # dfd.addErrback(lambda f: logger.error(
    #     #     f.value, exc_info=failure_to_exc_info(f), extra={'spider': info.spider})
    #     # )
    #     return dfd.addBoth(lambda _: wad)  # it must return wad at last


    # 下载器
    def get_media_requests(self,item,info):
        try:
            # for image_url in item['image_urls']:
            #     yield Request(image_url, meta={'item': deepcopy(item),'status':'0'},dont_filter=True)

            if item['food_urls']:
                for food_url in item['food_urls']:
                    yield Request(food_url, meta={'item': deepcopy(item),'status':'1'},dont_filter=True)

        except ValueError as e:
            print('下载图片失败，请查看pipeline')


    # 文件路径
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        status = request.meta['status']
        if status == '0':
            folder = item['provinceName'] + '/' + item['city_name'] + '/' + item['dis_name'] + '/' + item['title']
            folder_strip = folder.strip()
            # print(status)

        else:
            folder = item['provinceName'] + '/' + item['city_name'] + '/' + item['dis_name'] + '/' + item['title'] + '/' + item['gname']
            folder_strip = folder.strip()
            # print(status)

        image_guid = str(int(time.time() * 1000000)) + '.jpg'
        self.filename = u'Meishi/{0}/{1}'.format(folder_strip, image_guid)
        return self.filename

    # 获取结果
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            if item['food_urls']:
                print('food_urls下载图片错误',item['food_urls'],item['url'])
            else:
                print('该商品没有套餐信息',item['url'])

        return deepcopy(item)



class Meishi2ImagesPipeline(ImagesPipeline):
    # 下载器
    def get_media_requests(self,item,info):
        try:
            for image_url in item['image_urls']:
                yield Request(image_url, meta={'item': deepcopy(item),'status':'0'},dont_filter=True)

        except ValueError as e:
            print('下载图片失败，请查看pipeline')


    # 文件路径
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        status = request.meta['status']
        folder = item['provinceName'] + '/' + item['city_name'] + '/' + item['dis_name'] + '/' + item['title']
        folder_strip = folder.strip()
        # print(status)

        image_guid = str(int(time.time() * 1000000)) + '.jpg'
        self.filename = u'Meishi/{0}/{1}'.format(folder_strip, image_guid)
        return self.filename

    # 获取结果
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            if item['image_urls']:
                print('下载图片错误',item['image_urls'])
            else:
                print('该商品没有图片',item['url'])

        return deepcopy(item)


class MeishiPipeline_ToTXT(object):

    def process_item(self, item, spider):
        # csv文件的位置,无需事先创建
        # print(json)

        fname = 'E:/Meishi' + '/' + item['provinceName'] + '/' + item['city_name'] + '/' + item['dis_name'] + '/' + \
                item['title']
        if (os.path.exists(fname)):
            fname = fname + '/' + 'infos.txt'
            fmsg = {'title': item['title'],
                    'address': item['address'],
                    'phone': item['phone'],
                    'openTime': item['openTime'],
                    'lng': item['lng'],
                    'lat': item['lat'],
                    }
            try:
                with open(fname, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(fmsg, ensure_ascii=False))
            except FileNotFoundError:
                print('没有找到文件路径，请检查', item)
                return None

        if 'gname' in item:
            # filename = 'E:/Xiecheng' + '/' + PRIVICE + '/' + item['city'] + '/' + item['title']
            filename = 'E:/Meishi' + '/' + item['provinceName'] + '/' + item['city_name'] + '/' + item['dis_name'] + '/' + item['title']+ '/' + item['gname']
            if(os.path.exists(filename)):
                name = filename + '/' + 'infos.txt'
                msg = {'name':item['gname'],'price':item['gprice'],'info':item['info']}
                try:
                    with open(name,'w',encoding='utf-8') as f:
                        f.write(json.dumps(msg,ensure_ascii=False))
                except FileNotFoundError:
                    print('没有找到文件路径，请检查',item)
                    return None
                print(item['title'],'存储结束')

        return deepcopy(item)
