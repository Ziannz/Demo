import requests
import json,re
import datetime,time

# url = 'https://ihotel.meituan.com/hbsearch/HotelSearch?utm_medium=pc&version_name=999.9&cateId=20&attr_28=129&uuid=9E5699C008293BA09214D3D1672F572663290AC624B5C7C0DD5716A3712B6C2A%401554436038066&cityId=953&offset=0&limit=50&startDay=20190415&endDay=20190415&q=&sort=defaults&areaId=14&X-FOR-WITH=py4LjkWjRGicIXFR3rh0Xu5HphZwfHdU7VlZnwFI3TnybDh2C2JB1ce0Y6xSHUF%2BSRtpf09%2FdP3qYA714fzgVDkAtwB3s5CzAsmtMA01E9n2Bc1qL0h%2FzticZ5BqbTAKJciwTKXm2wv9ztYdemU%2B5Q%3D%3D'

'iuuid=ADE79379F7354FB5992E6A40E169720D01736880CBA4980D684AB8C6F5714693'
'9E5699C008293BA09214D3D1672F572663290AC624B5C7C0DD5716A3712B6C2A%401554436038066'
'9E5699C008293BA09214D3D1672F572663290AC624B5C7C0DD5716A3712B6C2A%401554436038066'
''
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
    "Cookie":"iuuid=ADE79379F7354FB5992E6A40E169720D01736880CBA4980D684AB8C6F5714693",
    'referer': 'https://hotel.meituan.com/xinjinxian/'
}

# headers = {
#     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
#     "Accept-Encoding":"gzip, deflate, br",
#     "Accept-Language":"zh-CN,zh;q=0.9",
#     #
#     # "Cache-Control":"max-age=0",
#     # "Connection":"keep-alive",
#     # "Cookie":"uuid=9eee3d9e90904edfb76d.1555299212.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=16a1f0e9cc5c8-01b64bc00575ea-e323069-1fa400-16a1f0e9cc5c8; _hc.v=a999101b-d78a-4176-b190-3d0229af8b19.1555299225; lat=30.788126; lng=104.361724; IJSESSIONID=1s02rqkvbro291qgrdnilq27cx; iuuid=ADE79379F7354FB5992E6A40E169720D01736880CBA4980D684AB8C6F5714693; _lxsdk=ADE79379F7354FB5992E6A40E169720D01736880CBA4980D684AB8C6F5714693; ci=317; rvct=317%2C585%2C1168%2C1207%2C910%2C59; cityname=%E5%B7%B4%E4%B8%AD; _lxsdk_s=16a202d1d81-a1e-987-2df%7C%7C31",
#     "Cookie":"iuuid=ADE79379F7354FB5992E6A40E169720D01736880CBA4980D684AB8C6F5714693",
#     # "Host":"ihotel.meituan.com",
#     # "Upgrade-Insecure-Requests":"1",
#     # "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
# }
#
url = 'http://p0.meituan.net/deal/61ef68c28106569e68ade3ac95bfe9a6424136.jpg@600w_600h_1l'

# resp = requests.get(url,headers=headers)
# if resp.status_code == 200:
#     with open('123.jpg','wb') as f:
#         f.write(resp.content)


# goods = json.loads(resp.text)['mergeList']['data']
# for good in goods:
#     item = {}
#     item['rname'] = good['roomCellName']
#     item['info'] = good['roomCellDesc']
#     image_urls = good['aggregateGoods']
#     # print(image_urls[0]['prepayGood']['extInfo']['imgs'])
#     image_urls = [x for x in image_urls[0]['prepayGood']['extInfo']['imgs']]
#
#     if image_urls:
#         images = re.sub('/w.h', '', '='.join(image_urls)).split('=')
#         images = [x + 'jpg' if x.endswith('.') else x for x in images]
#         print(images)
    # print(item)

# data = 'https://ihotel.meituan.com/hbsearch/HotelSearch?utm_medium=pc&version_name=999.9&cateId=20&attr_28=129&uuid=9E5699C008293BA09214D3D1672F572663290AC624B5C7C0DD5716A3712B6C2A%401554436038066&cityId=59&offset=50&limit=50&startDay=20190408&endDay=20190408&q=&sort=defaults&areaId=38&X-FOR-WITH=py4LjkWjRGicIXFR3rh0Xu5HphZwfHdU7VlZnwFI3TnybDh2C2JB1ce0Y6xSHUF%2BSRtpf09%2FdP3qYA714fzgVDkAtwB3s5CzAsmtMA01E9n2Bc1qL0h%2FzticZ5BqbTAKJciwTKXm2wv9ztYdemU%2B5Q%3D%3D'
# resp = re.search(r'.*?offset=(.*?)&',data).group(1)
# print(type(resp))




# import datetime,time
# today = datetime.date.today()
# today_start_time = int(time.mktime(time.strptime(str(today), '%Y-%m-%d'))) * 1000
# tomorrow = today + datetime.timedelta(days=1)
# today_end_time = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) * 1000
#
# print(today_start_time,today_end_time)
#
# print(1554652800000,1554739200000)


# a = '花田•囍筑精奢酒店式公寓'
#
# with open('123.txt','w') as f:
#     f.write(a)

# a = [{'a':'','b':[{'c':1,"d":2}]}]
# b = json.dumps(a)
#
# with open('123.txt','w') as f:
#     f.write(b)

# print(type(b))
# print(type(json.loads(b)))

# import codecs
# # codecs.open ( "test" , 'w' , 'utf-8' )
#
#
# data = [{'spec_name': '自主大床房(部分有窗)', 'spec_Id': '', 'value': [{'spec_value_name': '20', 'spec_name': '面积', 'spec_value_Id': ''}, {'spec_value_name': '128', 'spec_name': '价格', 'spec_value_Id': ''}, {'spec_value_name': '2', 'spec_name': '可住', 'spec_value_Id': ''}, {'spec_value_name': '1', 'spec_name': '窗户', 'spec_value_Id': ''}, {'spec_value_name': '含早餐', 'spec_name': '早餐', 'spec_value_Id': ''}]}]
#
# with codecs.open('123.txt','w',encoding='gbk') as f:
#     f.write(json.dumps(data,ensure_ascii=False))


# url = 'http://p0.meituan.net/tdchotel/cf4d242becc696ee36b184a7673181be849755.png'
# headers = {
#     'referer':'https://www.meituan.com/jiudian/42603805/'
# }
#
# resp = requests.get(url)
# with open('123.jpg','wb') as f:
#     f.write(resp.content)

# a ='6-35㎡'
# a ='6㎡'
# b = a.split('㎡')
# if '-' in b[0]:
#     c = b[0].split('-')[1]
# else:
#     c = b[0]
# print(c)

import os

'''
https://ihotel.meituan.com/productapi/v2/prepayList?type=1&utm_medium=PC&version_name=7.3.0&poiId=4898045&start=1554912000000&end=1554998400000&uuid=090D706B8CF5DB7255BA1F6AAD52A089479FB1B89DD4CCF15B7B8FB6913E47EC&401554976014832&_token=eJxNjEtvgkAURv+KYdENWmaGQQcT0/CwirQ+wKJSu0BEJeKgMArY9L8XXNAubnK+k5vzzSXGlus2
https://ihotel.meituan.com/productapi/v2/prepayList?type=1&utm_medium=PC&version_name=7.3.0&poiId=73043960&start=1554912000000&end=1554998400000&uuid=090D706B8CF5DB7255BA1F6AAD52A089479FB1B89DD4CCF15B7B8FB6913E47EC&_token=eJxVjNtugkAURf9lHvoilplxuCZNg1iqJShQsIXGB0DkqiAgFpv+e8fEpmlykrXPys7+As1iC2QEIeQQA7qWZo4jkkBEiRCRqui/EzjCgLBZz4D8gSRIGILQ5mpsKqjBkEFQhBvmNxOaMaF3bS1oCaRdV7cyy6ZVF5f3+zjrTsHhPqr2rDCBZCLxkH2MsgcMkTSGZIzQXVT9fRgwANCtvUO3KIsbgxu7G9ssOQAZxC/ncsjbVaoqlrJUhTdNDayQc9xZkgzvvqBgQ51a66M2C32MRdz31TJ2Ryt9cO3Gs9htKpSlf7YXyvrozXdh03uu2WoO7ndG3pgxX9YXvcF8h2OpHFnKws4tf47cJBoKzYAifyhWQd1Mq9zyMt/UnnRnUry2g68ua+5Zt/1+3hb8SJibJz68uIJBKjtNxc+Ter6A7x+Qa3i+

r https://ihotel.meituan.com/productapi/v2/prepayList?type=1&utm_medium=PC&version_name=7.3.0&poiId=2728678&start=1554912000000&end=1554998400000&uuid=090D706B8CF5DB7255BA1F6AAD52A089479FB1B89DD4CCF15B7B8FB6913E47EC&401554976284963&_token=eJxNkE1vgkAURf+KYdFN1RlwGBiTpsGC8mFsAUWa2gUilQ8BC6NUm/73Di5oFy859+TlvuR9c5Wx




end=1554998400000&poiId=73043960&start=1554912000000&type=1&utm_medium=PC&uuid=090D706B8CF5DB7255BA1F6AAD52A089479FB1B89DD4CCF15B7B8FB6913E47EC&version_name=7.3.0
end=1554652800000&poiId={}&start=1554566400000&type=1&utm_medium=PC&uuid=9E5699C008293BA09214D3D1672F572663290AC624B5C7C0DD5716A3712B6C2A&version_name=7.3.0
end=1554998400000&poiId=73043960&start=1554912000000&type=1&utm_medium=PC&uuid=090D706B8CF5DB7255BA1F6AAD52A089479FB1B89DD4CCF15B7B8FB6913E47EC&version_name=7.3.0

1554998400000
1554998400000
1554912000000
//div[@class="search-filter-classify"]/div[2]/div/a[1]/@href
//div[@class="search-filter-classify"]/div[2]/div/a[1]/@href

m 401555378016.7429638   401555378101278645
c 401555378001461        401555378097869
                         401555378151623
海口三亚琼海儋州文昌
SCHEDULER_PERSIST = True
'''
# today = datetime.date.today()
# today_start_time = int(time.mktime(time.strptime(str(today), '%Y-%m-%d'))) * 1000
# tomorrow = today + datetime.timedelta(days=1)
# today_end_time = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) * 1000
# print(today_end_time,today_start_time)


# a = 'http://p0.meituan.net/tdchotel/3619e1b5809b20904b3c5933312e66396532214.bmp.jpg'
# b = a.split('/')[-1].split('.')
# c = b[1]
# r ='.' + '.'.join(b[1:])
# print(r)
# d = a.replace(r,'.' + c)
# print(d)

# images = ['http://p1.meituan.net/tdchotel/d5d5a4639ac14dbfa4a6e4e1e4c30f951920054.bmp.jpg', 'http://p1.meituan.net/tdchotel/e1fd65218a91d79137752581f22a8a6e251279.jpg']
#
# urls = []
# for image in images:
#     b = image.split('/')[-1].split('.')
#     c = b[1]
#     r = '.' + '.'.join(b[1:])
#     d = image.replace(r, '.' + c)
#     urls.append(d)
#
# print(urls)

'''
cityName: 凉山
cateId: 0
areaId: 3954
sort: 
dinnerCountAttrId: 
page: 1
userId: 
uuid: f4dad639017f4aa59ee6.1555893041.4.0.0
platform: 1
partner: 126
originUrl: http://liangshan.meituan.com/meishi/b3954/
riskLevel: 1
optimusCode: 1
_token: eJxNj1FvokAUhf/LvEpkZhhhMOnDUFSwpSpVa9n0ARBlQBiFQSub/e87zbbJJjc553733OTe36Dx92CMILQh1MA1a8AYoCEcmkADslWT0cg0ESSWbVtIA+n/jEKILQ0kzdYF41/IxlAj0Pr4IqEC/wiCFH5oP54oj4mqr5SvQiCX8jzW9ROP62Obx/WwyrjslKai0pVvc64nhj0iuroIqLVqrdaUlt8af6v86QP1gsq2/Fgrl81v+2IjF58uW4ULen+820Vlc8f3KicSbxPszdi8I2XzXuqtlH7NnM/arTcGC5YXQ1xQlk6czNt2xgyHvGd4Ws3zQ2F5qycTU/1q7cS2rp4naUkkPcreDKswOL0IO7rRBUev4t3gYV+n/fl+OK9vPjlFBp+8MCIj9LqZ4qa4znu9S6ZOhbN+75LE6uwgKOlxRs/5k7mL88y4sueCEjTdxXx7uOuJwPSNQG9JcA/FoGEJ60kRinhgrJePl8LpF2IVGQPmydnaFQ/gz1851pFP


cityName: 凉山
cateId: 0
areaId: 3955
sort: 
dinnerCountAttrId: 
page: 1
userId: 
uuid: f4dad639017f4aa59ee6.1555893041.4.0.0
platform: 1
partner: 126
originUrl: http://liangshan.meituan.com/meishi/b3955/
riskLevel: 1
optimusCode: 1
_token: eJyNT11vqkAQ/S/7KpFdgZU18UFBe1GRD6XlctMHhOVDykdgUUrT/95tYl/6dJNJzpkzJ3NmPkBrxGCBICQQCuBGW7AAaAqnGAiAdXyiKBgjqKpYQkgA0S8NzwVwaZ91sPiHyAwKSCav34rLhYcCVfgq/HCZ85nM69tlcBPIGGsWoviWh1XaZWE1LWnOeo5RXYqcd1kuXiSiKCK/6H/Nsgh4QHnmARyLB4YPZD+9yZ/lW7s8rTiju3t89d6sQV85LhVP2rtKCj11dhpxWmXlWHfFGXYvBbI3aS+PG83V/2DPRravjZOCJMmYrR3/ii5NzrZOd49ZkBuJMslkvSe347xHeNsM+VBtrYNo7iJahMW4dkP7RO2xzrxwb8uegyVzEleNg7X+6MV1OhjSoe734dWKTwmiPjkb3XE2n/2tpSONaZBt7Fr3nzd7SSP+4UmaZ/BSlvcCw/wm+m2wlfDkuj6rVjdSE69YGkTB4enl1kFdqmHUuCFmZpIYa9NeLZfg8wvipaAA
'''

'''
1.套餐内形式不一样，有的在内容后面的模块中写出套餐详情
2.有部分在内容处出现套餐详情
2.有部分只有套餐描述，没有物品
3.部分没有套餐
4.部分只有代金券


解决：
    1.套餐内容在 dealList - deals 中
        1.
    2.若没有套餐内容则检查有没有代金券 在 dealList - vouchers 中
    3.若既没有套餐，也没有代金券则看是否添加菜品
'''