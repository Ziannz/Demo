import requests
import json,re
import datetime,time

# url = 'https://ihotel.meituan.com/hbsearch/HotelSearch?utm_medium=pc&version_name=999.9&cateId=20&attr_28=129&uuid=9E5699C008293BA09214D3D1672F572663290AC624B5C7C0DD5716A3712B6C2A%401554436038066&cityId=953&offset=0&limit=50&startDay=20190415&endDay=20190415&q=&sort=defaults&areaId=14&X-FOR-WITH=py4LjkWjRGicIXFR3rh0Xu5HphZwfHdU7VlZnwFI3TnybDh2C2JB1ce0Y6xSHUF%2BSRtpf09%2FdP3qYA714fzgVDkAtwB3s5CzAsmtMA01E9n2Bc1qL0h%2FzticZ5BqbTAKJciwTKXm2wv9ztYdemU%2B5Q%3D%3D'

'iuuid=ADE79379F7354FB5992E6A40E169720D01736880CBA4980D684AB8C6F5714693'
'9E5699C008293BA09214D3D1672F572663290AC624B5C7C0DD5716A3712B6C2A%401554436038066'
'9E5699C008293BA09214D3D1672F572663290AC624B5C7C0DD5716A3712B6C2A%401554436038066'
'https://verify.meituan.com/v2/web/general_page?action=spiderindefence&requestCode=8210d3c7348141bebffddad3d146bd69&platform=1000&adaptor=auto&succCallbackUrl=https%3A%2F%2Foptimus-mtsi.meituan.com%2Foptimus%2FverifyResult%3ForiginUrl%3Dhttp%253A%252F%252Fwww.meituan.com%252Fmeishi%252F157204239%252F'
'https://verify.meituan.com/v2/web/general_page?action=spiderindefence&requestCode=c5b9bd6f30404058a4ea2b38851611b8&platform=1000&adaptor=auto&succCallbackUrl=https%3A%2F%2Foptimus-mtsi.meituan.com%2Foptimus%2FverifyResult%3ForiginUrl%3Dhttp%253A%252F%252Fwww.meituan.com%252Fmeishi%252F157204239%252F'
'https://verify.meituan.com/v2/web/general_page?action=spiderindefence&requestCode=fc9ff97de7a04bffb81b62a440bcccbf&platform=1000&adaptor=auto&succCallbackUrl=https%3A%2F%2Foptimus-mtsi.meituan.com%2Foptimus%2FverifyResult%3ForiginUrl%3Dhttp%253A%252F%252Fwww.meituan.com%252Fmeishi%252F6594046%252F'
'http://liangshan.meituan.com/meishi/api/poi/getPoiList? cityName=%E5%87%89%E5%B1%B1 &cateId=0 &areaId=3954 &sort= &dinnerCountAttrId= &page=1 &userId=389492223 &uuid=05968e1846b8496c8d7b.1557123574.3.0.0 &platform=1 &partner=126 &originUrl=http%3A%2F%2Fliangshan.meituan.com%2Fmeishi%2Fb3954%2F &riskLevel=1 &optimusCode=1 &_token=eJxVj1uPokAQhf9Lv0Kkm6YRTOZBVgfEEdABGZnMQ3PRRkSWu%2B5m%2F%2Fs2yc7DJpWcU1%2FVSap%2Bg2aTggWCUIdQBEPWgAVAMzhTgQi6lk8ImctQx3NEZCSC5H%2BmQiyCuDmuwOITaXNdVObK10QOHHwiXYYighr8Er%2B9wr2s8Jq2NnwJsK77uZCkW07vl5bR%2B6zM8q7nmlSlxH3LcinGOlEkfhHgsdKfYqomi1hWJ1BMgCv9p913v%2BO%2F8FCbX%2B7cZfZ4vBZdPz6Xe9YL70bQjm%2BPtm5p%2FqzZAaHRuZR6VZF8fdoMwfp4Evy9EGQPOhDHayQhi%2FJ8vjvXwiv90RxOiQ2tzroqQuwbZXoesDCQw7b3YHRsKLOyZdB4le0bDNGBfoRmdfM10jsfbjK6haNt3PjphDrqHrtXQi3Yb6OVm57TwivhOor7FIfjm%2B72Zsus26jZeFubQ65KuMS9UmHHMfaPGkWobhp%2Ff12Zbjh4eqjeLEIv74r6XFssQ%2F7VLYNCDRK%2FsH955pJprWTUuhMtX17An789bpiI'

'https://qd.meituan.com/meishi/api/poi/getPoiList?cityName=%E9%9D%92%E5%B2%9B&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1&userId=389492223&uuid=05968e1846b8496c8d7b.1557123574.3.0.0&platform=1&partner=126&originUrl=https%3A%2F%2Fqd.meituan.com%2Fmeishi%2F&riskLevel=1&optimusCode=1&_token=eJx1j0tvqzAUhP%2BLt6BgU4NJdqHQlDQklIakoeqCV8AUwssQwtX973WldtFFpSPN5zmj0fE%2F0FoxWCAI5xCKYEhasABoBmcqEAHr%2BEZRiIxkKKsynIsg%2Bu3dIVUEYXswwOINaWQuYoLfvxyXG29oLkMRQQ2%2Biz%2BMOcuYz1fK4iGQMVZ3C0lq4lmZUNYHl1lUlRLnLqMSv%2BKPAOAN5Z43cP341uBb2c%2Fb5r%2FhFR1NL5yS9bXIc7bTDfPZ3Qm31HMc2XEmyyiWq5uZ2SlJH%2FcJaV0kBZvE7ZenGmebiJ70EOuvvieUdZOqu6uBsIyHrX2%2BGtrQ7%2B9lXRomRRhy4WEcqZ43xWook1KpqLfybDYKe%2F2pNq1ppOcgjF6VYur7nhxuV8NC3lGp4yXaZOfOfQwvpaLF0bGHL51GCVbOZuUdTSVsLTLpd236caKsSeMhOm39ER0qpyr8zlBjtG0Me7eW7N5WQy1i66YsgkJXS99%2FMcjqIAlLx25groL%2FnynKl4U%3D'
'https://qd.meituan.com/meishi/api/poi/getPoiList?cityName=%E9%9D%92%E5%B2%9B&cateId=0&areaId=133&sort=&dinnerCountAttrId=&page=1&userId=389492223&uuid=05968e1846b8496c8d7b.1557123574.3.0.0&platform=1&partner=126&originUrl=http%3A%2F%2Fqd.meituan.com%2Fmeishi%2Fb133%2F&riskLevel=1&optimusCode=1&_token=eJxVjstuqzAURf%2FF06BgY17OLIS8SimFEGipOgBiEpJCeJhwnav779eR2kGlI%2B119lmD8xd02wOYIQgJhBK40Q7MAJrCqQ4kwHpx0TRDQQrUsGIaEsh%2Fd1hDEsi6yAazD2QaRFIN9fPRBKL4QESBEoIm%2FJR%2BWBWsqGIe1lZI4MRYM5Pl9jCtaMmGtJ7m10oW3J9KOUMYy%2BITIPQqFLrIy3em38l%2Bdle8Lty%2BPNaC6NMYnS%2FMsxbLfVAUu7ma%2BP4GXpdjWgU8W1f%2BcCyrApdmtKFPpWqnxTrMjrU10Ra0TniOzToy54QuBpR0%2FVm3y3FD6zP347Egk%2BJ2J8V97bl7V2%2BC7Fo7DNv78t3tEj20OEuc%2BmxNVqNH%2BZtzgI5JA3XeZvWW%2FAmWGm5WfbGPxswxsP2crGjLorZNtPw12PH2xMe3TueeOZK11lycmPkt3sU4zqPISQ%2FvKWmK0DsNftKM2NWNe3bjPA%2B%2FXkoU6PElHSb5YgPvZmItrzH49x9BGZK3'
'https://qd.meituan.com/meishi/api/poi/getPoiList?cityName=%E9%9D%92%E5%B2%9B&cateId=28&areaId=133&sort=&dinnerCountAttrId=&page=1&userId=389492223&uuid=05968e1846b8496c8d7b.1557123574.3.0.0&platform=1&partner=126&originUrl=http%3A%2F%2Fqd.meituan.com%2Fmeishi%2Fc28b133%2F&riskLevel=1&optimusCode=1&_token=eJx9j0tvozAUhf%2BLt0XBNuYVqQs6hGeTUp6ZqbrgleCAKQUSmhn1v9fVtIvZjHSl8%2Fnco6PrP2B0K7BGEOoQCuBSj2AN0AquFCCAeeIbWVYxwlDFmGgCKP%2F1JKQIoBhTE6yfkKbqAlHJ86cTcuMJ6RgKCGrwWfhmwhkTPp8pl4dAM8%2FDWhRfqxWr6XzO%2B1X5wkTOU0PFEmsFkiSRH%2FPf3N8Q72Qx7%2BTafmn%2BpfP3e8v%2Fx9smeuw51d6SnuL5bFw3SXg40GPj2szQYhp5VyvqfHlJFs32T6YnGi7yMYkL3xuX3tI7q3QqWNWafocC42KedkMUZ67zmNCOBhLW2DFQ1UslXwItlm1%2FUybkQk5Wo9A82gZjqMQGgZ7Sk4nc9NN5uv%2FZy1TdBaFxpxS0ithijnuKq%2BzVx4W97ZnoNV2iGof8KrO2r01VYRunqQ4BUpsfYvGwC%2FfJYKUk89P8DSWum3SjdO6ajJXW3pV%2BD9MvNE8vs32zj2fHaAacte1Rhg%2FBYnpteu883t6C9w%2FFrZ47'
'''
cateId
日韩料理 28
西餐  35
'''

# headers = {

#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'Accept-Language': 'en',
#     "Cache-Control": "max-age=0",
#     "Connection": "keep-alive",
#     # "Host": "www.meituan.com",
#     # "Upgrade-Insecure-Requests": "1",
#     # "Cookie":"lxsdk_cuid=169e60ad4efc8-00c8ad2eab0cb1-7a1b34-1fa400-169e60ad4f0c8; ci=59; rvct=59; iuuid=090D706B8CF5DB7255BA1F6AAD52A089479FB1B89DD4CCF15B7B8FB6913E47EC; cityname=%E6%88%90%E9%83%BD; _lxsdk=090D706B8CF5DB7255BA1F6AAD52A089479FB1B89DD4CCF15B7B8FB6913E47EC; _hc.v=b7fc0e60-73df-004d-20ee-912c615c79de.1554368252; uuid=67b52569e6f04625b1f6.1554685268.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=248992056.1554342671290.1554685269369.1554685525187.6; IJSESSIONID=11v3yovx77rb5le1cn9b8hlzm; _lxsdk_s=169faeabd5a-1d8-408-629%7C%7C5",
#     # "Cookie": "_lxsdk_cuid=16a1f0e9cc5c8-01b64bc00575ea-e323069-1fa400-16a1f0e9cc5c8; __mta=251508409.1555299213429.1555299213429.1555299213429.1; _hc.v=a999101b-d78a-4176-b190-3d0229af8b19.1555299225; iuuid=ADE79379F7354FB5992E6A40E169720D01736880CBA4980D684AB8C6F5714693; _lxsdk=ADE79379F7354FB5992E6A40E169720D01736880CBA4980D684AB8C6F5714693; lsu=; isid=B36645019AC054EF7DFE25E423F164DB; logintype=normal; oops=-ZzPPdMHG5BnbFfFJvh-2YnWUg8AAAAAUggAAOsaHsVz22MXAvVUROUsg8UfO89o6QXX9f_Yu6zuPa0c5SgT4r22yre6RdNotfJwqg; cityname=%E5%87%89%E5%B1%B1; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; client-id=a205b22e-8ade-4410-b2ed-13d7179e0667; mtcdn=K; u=389492223; n=BxG446002397; lt=CXtJZyd9hV_7N2B_ayLPO1uoKnAAAAAAUggAAAm5n1-qqylGE4FPUW76csyCkMc6isvZykjO5DkXfF_hcThT08TZXKzjCQ-Wg66KoQ; token2=CXtJZyd9hV_7N2B_ayLPO1uoKnAAAAAAUggAAAm5n1-qqylGE4FPUW76csyCkMc6isvZykjO5DkXfF_hcThT08TZXKzjCQ-Wg66KoQ; unc=BxG446002397; uuid=a3d58f800cf2490ab87d.1557017027.4.0.0; ci=94; rvct=94%2C321%2C59%2C313%2C107%2C323%2C1268%2C1128%2C1114%2C981%2C871; lat=19.97196; lng=110.34327; _lxsdk_s=16a8aa88b77-786-aa-a5f%7C%7C53",
#     "Cookie": "uuid=a3d58f800cf2490ab87d.1557017027.4.0.0",
#     # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
# }
headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Cookie":"_lxsdk_cuid=16a1f0e9cc5c8-01b64bc00575ea-e323069-1fa400-16a1f0e9cc5c8; __mta=251508409.1555299213429.1555299213429.1555299213429.1; _hc.v=a999101b-d78a-4176-b190-3d0229af8b19.1555299225; iuuid=ADE79379F7354FB5992E6A40E169720D01736880CBA4980D684AB8C6F5714693; _lxsdk=ADE79379F7354FB5992E6A40E169720D01736880CBA4980D684AB8C6F5714693; lsu=; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; client-id=a205b22e-8ade-4410-b2ed-13d7179e0667; mtcdn=K; uuid=a3d58f800cf2490ab87d.1557017027.4.0.0; ci=94; rvct=94%2C321%2C59%2C313%2C107%2C323%2C1268%2C1128%2C1114%2C981%2C871; IJSESSIONID=13sb3c7ohnw5112na4a0o1xsbg; cityname=%E6%B5%B7%E5%8F%A3; lat=19.992046; lng=110.314352; _lxsdk_s=16a8aa88b77-786-aa-a5f%7C%7C232",
    "Host":"www.meituan.com",
    "Referer":"http://haikou.meituan.com/meishi/b5312/",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
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
url = 'http://www.meituan.com/meishi/4018896/'

resp = requests.get(url,headers=headers)
if resp.status_code == 200:
    print(resp.text)


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