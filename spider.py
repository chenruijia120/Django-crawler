from bs4 import BeautifulSoup
import re
import xlwt
from lxml import etree
import time
import requests
import json
import random
import pickle

def main():
    baseurl="https://movie.douban.com/j/search_subjects?type=movie&tag=韩国&sort=rank&page_limit=20&page_start="
    getData(baseurl)
    






#1.爬取网页
def getData(baseurl):
    movies=[]
    for i in range(6,7):
        url=baseurl+str(i*20)
        datas=askdynamicURL(url)
        print(i)
        for data in datas['subjects']:
            url = data['url']
            movie=getDetailedData(url)
            filename = "movie.pkl"
            with open(filename,'ab') as f:
                pickle.dump(movie,f)
                f.close()

def getDetailedData(baseurl):
    data={}
    r=askURL(baseurl)
    s = etree.HTML(r)
    title=s.xpath('//*[@id="content"]/h1/span[1]/text()')
    if len(title)==0:
        return
    title=title[0]
    data['title']=title
    actor=s.xpath('//*[@id="info"]/span[3]/span[2]/a/text()')
    actor=actor[:10]
    actorlink=s.xpath('//*[@id="info"]/span[3]/span[2]/a/@href')
    actorlink=actorlink[:10]
    actorinfo=[]
    for str in actorlink:
        html="https://movie.douban.com"+str
        actorinfo.append(getActors(html))
    data['actor']=actor
    data['actorlink']=actorlink
    data['actorinfo']=actorinfo
    img=s.xpath('//*[@class="nbgnbg"]/img/@src')
    img=img[0]
    data['img']=img
    info=s.xpath('//*[@id="link-report"]/span[1]/text()')
    des=""
    for it in info:
        des=des+it.strip()
    data['description']=des
    director=s.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')
    screenwriter=s.xpath('//*[@id="info"]/span[2]/span[2]/a/text()')
    type=s.xpath('//*[@id="info"]/span[5]/text()')
    data['director']=director
    data['screenwriter']=screenwriter
    data['type']=type
    url=baseurl+"comments/"
    comments=getComments(url)
    data['comments']=comments
    return data;


def getComments(url):
    r=askURL(url)
    s=etree.HTML(r)
    comments=[]
    for i in range(1,6):
        comment=s.xpath('//*[@id="comments"]/div['+str(i)+']/div[2]/p/span/text()')
        comments.append(comment)
    return comments

def getActors(url):
    r=askURL(url)
    s=etree.HTML(r)
    actor={}
    name=s.xpath('//*[@id="content"]/h1/text()')
    if len(name)==0:
        return
    name=name[0]
    actor['name']=name
    info=s.xpath('//*[@id="intro"]/div[2]/span/text()')
    des=""
    for it in info:
        des=des+it.strip()
    actor['description']=des
    img=s.xpath('//*[@class="nbg"]/@href')
    img=img[0]
    actor['img']=img
    othername=s.xpath('//*[@id="headline"]/div[2]/ul/li/span/text()')
    othername=othername[:3]
    other=s.xpath('//*[@id="headline"]/div[2]/ul/li/text()')
    otherinfo=[]
    i=0
    for item in other:
        i=i+1
        if i%2==0:
            item=item.strip()
            item=item.replace(" ","")
            item=item.replace("\n","")
            item=item.replace(":","")
            otherinfo.append(item)
    otherinfo=otherinfo[:1]
    for j in range(0,1):
        actor[othername[j]]=otherinfo[j]
    return actor

def askdynamicURL(url):
    response=askURL(url)
    json_data=json.loads(response)
    return json_data



def askURL(url):
    #pro={'http':'http://175.174.132.225:34907'}
    head={ 'user-Agent':'Mozilla/5.0(Windows NT 10.0;Win64 x64)AppleWebkit/537.36(KHTML,like Gecko) chrome/58.0.3029.110 Safari/537.36'}
    #response=requests.get(url,proxies=pro,headers=head).text
    response=requests.get(url,headers=head).text
    time.sleep(5)
    return response








if __name__=="__main__":
    #当程序执行时
    main()
    print("爬取完毕")
