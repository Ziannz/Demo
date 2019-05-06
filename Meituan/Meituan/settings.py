# -*- coding: utf-8 -*-

# Scrapy settings for Meituan project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Meituan'

SPIDER_MODULES = ['Meituan.spiders']
NEWSPIDER_MODULE = 'Meituan.spiders'




# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Meituan (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    # "Host": "www.meituan.com",
    # "Upgrade-Insecure-Requests": "1",
    "Cookie":"lxsdk_cuid=169e60ad4efc8-00c8ad2eab0cb1-7a1b34-1fa400-169e60ad4f0c8; ci=59; rvct=59; iuuid=090D706B8CF5DB7255BA1F6AAD52A089479FB1B89DD4CCF15B7B8FB6913E47EC; cityname=%E6%88%90%E9%83%BD; _lxsdk=090D706B8CF5DB7255BA1F6AAD52A089479FB1B89DD4CCF15B7B8FB6913E47EC; _hc.v=b7fc0e60-73df-004d-20ee-912c615c79de.1554368252; uuid=67b52569e6f04625b1f6.1554685268.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=248992056.1554342671290.1554685269369.1554685525187.6; IJSESSIONID=11v3yovx77rb5le1cn9b8hlzm; _lxsdk_s=169faeabd5a-1d8-408-629%7C%7C5",
    # "Cookie": "_lxsdk_cuid=16a1f0e9cc5c8-01b64bc00575ea-e323069-1fa400-16a1f0e9cc5c8; __mta=251508409.1555299213429.1555299213429.1555299213429.1; _hc.v=a999101b-d78a-4176-b190-3d0229af8b19.1555299225; iuuid=ADE79379F7354FB5992E6A40E169720D01736880CBA4980D684AB8C6F5714693; _lxsdk=ADE79379F7354FB5992E6A40E169720D01736880CBA4980D684AB8C6F5714693; lsu=; isid=B36645019AC054EF7DFE25E423F164DB; logintype=normal; oops=-ZzPPdMHG5BnbFfFJvh-2YnWUg8AAAAAUggAAOsaHsVz22MXAvVUROUsg8UfO89o6QXX9f_Yu6zuPa0c5SgT4r22yre6RdNotfJwqg; cityname=%E5%87%89%E5%B1%B1; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; client-id=a205b22e-8ade-4410-b2ed-13d7179e0667; mtcdn=K; u=389492223; n=BxG446002397; lt=CXtJZyd9hV_7N2B_ayLPO1uoKnAAAAAAUggAAAm5n1-qqylGE4FPUW76csyCkMc6isvZykjO5DkXfF_hcThT08TZXKzjCQ-Wg66KoQ; token2=CXtJZyd9hV_7N2B_ayLPO1uoKnAAAAAAUggAAAm5n1-qqylGE4FPUW76csyCkMc6isvZykjO5DkXfF_hcThT08TZXKzjCQ-Wg66KoQ; unc=BxG446002397; uuid=a3d58f800cf2490ab87d.1557017027.4.0.0; ci=94; rvct=94%2C321%2C59%2C313%2C107%2C323%2C1268%2C1128%2C1114%2C981%2C871; lat=19.97196; lng=110.34327; _lxsdk_s=16a8aa88b77-786-aa-a5f%7C%7C53",
    # "Cookie": "uuid=a3d58f800cf2490ab87d.1557017027.4.0.0",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
}

# DEFAULT_REQUEST_HEADERS = {
#     'Accept': 'application/json, text/plain, */*',
#     'Origin': 'https://hotel.meituan.com',
#     'Referer': 'https://hotel.meituan.com/chengdu/',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.20 Safari/537.36',
#     'Cookie': 'iuuid=4AD267F336B465AAE47290D9CBB4741EBBDECC1316348D674688EDA3DF2F3E9B; latlng=30.656766%2C104.069164%2C1554699008388; ci=59; cityname=%E6%88%90%E9%83%BD; _lxsdk_cuid=169fb48412580-0741b8f44135e6-4a531929-1fa400-169fb484126be; _lxsdk=4AD267F336B465AAE47290D9CBB4741EBBDECC1316348D674688EDA3DF2F3E9B; _lxsdk_s=169fb484129-e32-b71-94c%7C%7C1',
# }


# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Meituan.middlewares.MeituanSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'Meituan.middlewares.MeituanDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'Meituan.pipelines.MeituanPipeline': 300,
    # 'Meituan.pipelines.MyImagesPipeline':200,
    # 'Meituan.pipelines.MImagesPipeline':100,
    # 'Meituan.pipelines.Pipeline_ToTXT': 302,
    'Meituan.pipelines.MeishiImagesPipeline':100,
    'Meituan.pipelines.Meishi2ImagesPipeline':200,
    'Meituan.pipelines.MeishiPipeline_ToTXT': 302,
}

# MEDIA_ALLOW_REDIRECTS =True
REDIRECT_ENALBED = False

IMAGES_STORE = r'E:\\'

# 图像管道避免下载最近已经下载的图片。使用 FILES_EXPIRES (或 IMAGES_EXPIRES) 设置可以调整失效期限，
# 可以用天数来指定
# IMAGES_EXPIRES = 30


# 设置下载延迟
import random
DOWNLOAD_DELAY= round(random.random(),2)

AUTOTHROTTLE_ENABLED = True

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# # 设置日志
# # 日志文件
# import time
# # LOG_FILE = 'Meituan.log' # 最好为爬虫名称
# LOG_FILE = 'spiders/meishi' + '_' + time.strftime("%Y%m%d%H%M", time.localtime()) + '.log'
#
# # 日志等级
# LOG_LEVEL = 'INFO'
# #
# # 是否启用日志（创建日志后，不需开启，进行配置）
# LOG_ENABLED = True  # （默认为True，启用日志）
#
# # 日志编码
# LOG_ENCODING = 'utf-8'
# #
# # 如果是True ，进程当中，所有标准输出（包括错误）将会被重定向到log中;例如：在爬虫代码中的 print（）
# LOG_STDOUT = False  # 默认为False