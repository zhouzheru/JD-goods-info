import requests
from urllib.parse import urlencode
from lxml import etree
import json
import csv

base_url = 'https://sclub.jd.com/comment/productPageComments.action?'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}

def get_page(page):
    params = {'callback':'fetchJSON_comment98vv14177',
                'productId':'100000287163',
                'score':'0',
                "sortType":'5',
                'page':page,
                'pageSize':10,
                'isShadowSku':'0',
                'rid':"0",
                "fold":'1'}
    url = base_url+urlencode(params)

    result = requests.get(url,headers = headers)
    text = result.text
    jd=text.lstrip("fetchJSON_comment98vv1418177(")
    jd = jd.rstrip(');')
    jd = json.loads(jd)
    return jd
comments = []
id =[]
color = []
saleValue = []

def getcomments(jd):

    list1=jd.get('comments')
    for i in range(len(list1)):
        id.append((list1[i]['id']))
        comments.append((list1[i]['content']))
        color.append(list1[i]['productColor'])
        saleValue.append(list1[i]['productSales'][0].get('saleValue'))
    return (id,color,saleValue,comments)
def savetocsv(id,color,saleValue,comments):
    with open('JD.csv',"w",encoding= 'utf8',newline ="\n") as f:
        writer = csv.writer(f)
        writer.writerow(['用户id',"颜色","内存","评论"])
        for i in range(len(id)):
            writer.writerow([id[i],color[i],saleValue[i],comments[i]])


for page in range(1,321):
    s=get_page(page)
    id,color,saleValue,comments=getcomments(s)
    savetocsv(id,color,saleValue,comments)
    print("第"+str(page)+'页已加载完成..........................')
