import os
import time
import hmac, hashlib
import urllib.parse
import urllib.request
import ssl
import json
import sys
import json
from pprint import pprint
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
import threading
import requests

os.environ['TZ'] = 'GMT+0'

key = ""
secret = ""
to_phone = ""
from_phone = ""

datetime=time.strftime('%y%m%d')+'T'+time.strftime('%H%M%S')+'Z'
method = "GET"
#replace with your own vendorId
path = "/v2/providers/openapi/apis/api/v4/vendors/상점코드/ordersheets"
query = urllib.parse.urlencode({"createdAtFrom": "2020-03-09", "createdAtTo": "2020-04-07","status":"FINAL_DELIVERY"})

message = datetime+method+path+query

accesskey = ""
secretkey = ""

signature=hmac.new(secretkey.encode('utf-8'),message.encode('utf-8'),hashlib.sha256).hexdigest()

authorization  = "CEA algorithm=HmacSHA256, access-key="+accesskey+", signed-date="+datetime+", signature="+signature
#print(authorization)

# ************* SEND THE REQUEST *************
url = "https://api-gateway.coupang.com"+path+"?%s" % query
print('BEGIN REQUEST++++++++++++++++++++++++++++++++++++')
req = urllib.request.Request(url)
#print(req)

req.add_header("Content-type","application/json;charset=UTF-8")
req.add_header("Authorization",authorization)

req.get_method = lambda: method

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print(req.get_full_url())
print(req.get_header("Content-type"))
print(req.get_header("Authorization"))
print(req.get_method())

print('RESPONSE++++++++++++++++++++++++++++++++++++')
#resp = urllib.request.urlopen(req)

try:
    resp = urllib.request.urlopen(req,context=ctx)
except urllib.request.HTTPError as e:
    if e.code == 404:
        print("404")
    else:
        print("NOT 404")
except urllib.request.URLError as e:
    print(e.errno)
else:
    # 200
    body = resp.read().decode(resp.headers.get_content_charset())
    print(body)
print("=========JSON 출력=========")
json_data = json.loads(body)
print(json_data)
print("=========특정 값 출력=========")
for i, e in enumerate(json_data['data']):
    orderinfo = "====주문 정보===\n"
    delivery_number = "배송번호:"
    order_number = "주문번호:"
    info = "===배송지 정보===\n"
    addr1 = "주소1:"
    addr2 = "주소2:"
    postcode = "우편 번호: "
    # =========================주문 관련=================================
    # 배송번호(묶음배송번호)
    shipment_Box_Id= e['shipmentBoxId']
    order_id = e['orderId']
    order_at = e['orderedAt']
    name = e['receiver']['name']
    addr_1 =  e['receiver']['addr1']
    addr_2 = e['receiver']['addr2']
    addr_3 = addr_1 + addr_2
    post_code = e['receiver']['postCode']