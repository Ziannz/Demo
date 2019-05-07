import base64
import zlib
import json
import requests
from urllib.parse import urlencode

str = "areaId=38&cateId=0&cityName=成都&dinnerCountAttrId=&optimusCode=1&originUrl=http://cd.meituan.com/meishi/b38/&page=1&partner=126&platform=1&riskLevel=1&sort=&userId=&uuid=b3f8513a2d2145aca2ac.1557226163.1.0.0"
sign = zlib.compress(str.encode())
base_str = base64.b64encode(sign).decode()



dic = {"rId":100900,"ver":"1.0.6","ts":1557228325371,"cts":1557228325572,"brVD":[1440,151],"brR":[[1440,900],[1440,900],24,24],"bI":["http://cd.meituan.com/meishi/b38/",""],"mT":[],"kT":[],"aT":[],"tT":[],"aM":"","sign":base_str}

token = zlib.compress(json.dumps(dic).encode())
base_token = base64.b64encode(token).decode()
# print(base_token)

data = {
    "cityName":"成都",
    "cateId":"0",
    "areaId":"38",
    "sort":"",
    "dinnerCountAttrId":"",
    "page":"1",
    "userId":"",
    "uuid":"b3f8513a2d2145aca2ac.1557226163.1.0.0",
    "platform":"1",
    "partner":"126",
    "originUrl":"http://cd.meituan.com/meishi/b38/",
    "riskLevel":"1",
    "optimusCode":"1",
    # "_token":"eJxVjltvozAQhf+LX0HBBhtKpD6QC6mTJikuaRKqPgRwgBDIBQenrPa/r6ttpV1ppHPmzKfR+QWuNAV9BKELoQ5afgV9gHqwZwMdiEZdCHFM88EyieUgHST/Z9gxdRBf30ag/44whjoi6OMrYSr4m6i/H/o/1sRqvhiqEJALce4bRpL2Kl6I267uJafKUL7JCyO2HgxVAyi6ChWttPzW3beKn32ueiu2KbJaOT6V6SFES68bBznXXuVl7QpxPOY8GJ5X02E6qr37FJf+rdkfkpSiUXBObD8Z4GO8XWbaS2y1LYOBLIVM8xWfeOlClnttT5djpxW2ZlR2cR90TFw2dVtF1Sp6Os5Pdzfetl4E1zmnhGQL4TTTpCbhZ/C6m1tD/3lD6M4aEvbEzQujm65GswGn0o5ZxBbaIDyFrChuluuHrpy4ctawpYv37sHpJvjUmaJxoiwT45e5lUk8W3MC04N/RdsLX5VnF7ZUYzTwHh/B7z9apI1i",
    "_token":base_token,
}

base_url = 'http://cd.meituan.com/meishi/api/poi/getPoiList?'

headers = {
    "Accept":"application/json",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Connection":"keep-alive",
    "Cookie":"_lxsdk_cuid=169e87e811cc8-076c6039841c43-181f7c51-1fa400-169e87e811cc8; iuuid=9E5699C008293BA09214D3D1672F572663290AC624B5C7C0DD5716A3712B6C2A; _lxsdk=9E5699C008293BA09214D3D1672F572663290AC624B5C7C0DD5716A3712B6C2A; cityname=%E6%88%90%E9%83%BD; _hc.v=da32afa4-d732-3d0d-c593-480f24846509.1555069153; ci=59; rvct=59%2C318%2C576%2C50; uuid=b3f8513a2d2145aca2ac.1557226163.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=154433159.1555589066711.1555589066711.1557226181685.2; client-id=ec74dc21-a813-4d3e-816c-97b7affee9a0; lat=30.612763; lng=104.06258; _lxsdk_s=16a91e9bded-3e6-c30-711%7C%7C10",
    "Host":"cd.meituan.com",
    "Referer":"http://cd.meituan.com/meishi/b38/",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3569.0 Safari/537.36",
}
url = base_url + urlencode(data)
# print(url)
while True:
    resp = requests.get(url,headers=headers)
    if resp.status_code == 200:
        if '抱歉，页面暂时无法访问' in resp.text:
            print('获取页面失败，重新获取')
            continue

        else:
            print(json.loads(resp.text))
            break



# msg = 'eJwdjT1OAzEQhe+SwqW9ttllheQCpUJCdDnAxJ4kFusfjcdI1DQpc6FcB4lbYOg+Pb3vvR0QwktwdhUeGAdNwkf+fIOE7vt6+/m6ixBzRtqXnvmZmUZHlMox9bYvAZ0WheI55gNt7sJcn5TyQSaM3CFLX5Ia3C5RHe2qRIXzn1KBeIw6bRZRN+BToTRiiu39FT9wG9wKsRO94f9j7zG4oz2ts7ZggtEPM3gw4KWe50djFr1YqeUkp90vI+RIQA=='
# base_msg = base64.b64decode(msg.encode())
# zlib_url = zlib.decompress(base_msg).decode()
# print(zlib_url)

