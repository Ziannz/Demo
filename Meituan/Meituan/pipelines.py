# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import time
import os,csv
import random
from copy import deepcopy
import requests


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



