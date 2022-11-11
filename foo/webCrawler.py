from unittest import result
from flask import flash
from matplotlib.pyplot import flag
from numpy import result_type
from pyparsing import null_debug_action
import requests
import time
import os
from bs4 import BeautifulSoup
import json
import re
from lxml import etree

urlMovie = 'https://movie.douban.com/subject/{}/'
urlBook = 'https://book.douban.com/subject/{}/'

def getMovieURL():
    with open('../docs/Movie_id.txt','r') as movieFile:
        print(movieFile.readline())
        lines = movieFile.readlines()
        lines = map(lambda x:x.strip(),lines)
        URLs = map(lambda x:urlMovie.format(x),lines)
        return list(URLs)

def getBookURL():
    with open('../docs/Book_id.txt','r') as bookFile:
        print(bookFile.readline())
        lines = bookFile.readlines()
        lines = map(lambda x:x.strip(),lines)
        URLs = map(lambda x:urlMovie.format(x),lines)
        return list(URLs)

def doubanMovie(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    r = requests.get(url,headers=head)
    return r.text
    result = {
        "电影名:":[],
        "导演:":[],
        "编剧:":[],
        "主演:":[],
        "类型:":[],
        "制片国家/地区:":[],
        "语言:":[],
        "上映日期:":[],
        "片长:":[],
        "又名:":[],
        "IMDb:":[]
    }
    # return r
    # soup = BeautifulSoup(r.text,features='lxml')
    # print(soup.prettify())    
    # movieName = soup.h1.span.string
    # print(soup.select('#info > span')[1])
    s = etree.HTML(r.text)
    # print('电影名:',s.xpath('//*[@id="content"]/h1/span[1]/text()'))
    # print('导演:',s.xpath('//*[@id="info"]/span[1]/span[2]/a/text()'))
    # print('编剧:',s.xpath('//*[@id="info"]/span[2]/span[2]/a/text()'))
    # print('主演:',s.xpath('//*[@id="info"]/span[3]/span[2]/a/text()'))
    result['导演:'] = s.xpath('//*[@id="content"]/h1/span[1]/text()')
    result['编剧:'] = s.xpath('//*[@id="info"]/span[2]/span[2]/a/text()')
    result['主演:'] = s.xpath('//*[@id="info"]/span[3]/span[2]/a/text()')
    result['电影名:'] = s.xpath('//*[@id="content"]/h1/span[1]/text()')
    soup = BeautifulSoup(r.text,features='lxml')
    datas = str(soup.find_all(id='info')).split('\n')
    del datas[0:4]
    del datas[-1]
    for data in datas:
        reResult = re.findall('>(.*?)</span>',data)
        for _r in reResult[1:]:
            result[reResult[0]].append(_r)

        r1 = re.sub('>(.*?)</span>','',data)
        r2 = re.findall('<span class="pl"(.*?)<br/>',r1)
        if(result[reResult[0]] == []):
            result[reResult[0]].append(r2[0].strip(' '))

    return result
    

def handleMovieData(text):
    result = {
        "基本信息":{},
        "剧情简介":{},
        "演职员表":{}
    }
    s = etree.HTML(text)
    result["基本信息"]['电影名:'] = s.xpath('//*[@id="content"]/h1/span[1]/text()')
    result["基本信息"]['导演:'] = s.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')
    result["基本信息"]['编剧:'] = s.xpath('//*[@id="info"]/span[2]/span[2]/a/text()')
    result["基本信息"]['主演:'] = s.xpath('//*[@id="info"]/span[3]/span[2]/a/text()')
    
    # print(s.xpath('//*[@id="link-report-intra"]/span[2]/text()'))

    soup = BeautifulSoup(text,features='lxml')
    
    datas = str(soup.find_all(id='info')).split('\n')
    del datas[0:4]
    del datas[-1]
    for data in datas:
        try:
            reResult = re.findall('>(.*?)</span>',data)
            result["基本信息"][reResult[0]] = reResult[1:]

            r1 = re.sub('>(.*?)</span>','',data)
            r2 = re.findall('<span class="pl"(.*?)<br/>',r1)
            if(result["基本信息"][reResult[0]] == []):
                result["基本信息"][reResult[0]].append(r2[0].strip(' '))
        except:
            pass

        
    intro = str(soup.select('span[class="all hidden"]')[0])
    intro = intro.replace(' ','').replace('<br/>','').replace('\n','').replace(chr(12288),'')
    reResult = re.findall('<spanclass="allhidden">(.*?)</span>',intro)
    result['剧情简介'] = reResult[0]


    actors = soup.select('div[class="info"]')
    actList = []
    for i in actors:
        act = {
            "actor":"",
            "character":""
        }
        i = str(i)
        reS = re.findall('title="(.*)">',i)
        # print(reS[0],'========>',reS[1])
        act['actor'] = reS[0]
        act['character'] = reS[1]
        actList.append(act)

    result['演职员表']['data'] = actList
    return result


def doubanBook(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    r = requests.get(url,headers=head)
    return r.text

def handleBook(text):

    result = {
        "基本信息":{},
        "内容简介":{},
        "作者简介":{}
    }


    s = etree.HTML(text)
    soup = BeautifulSoup(text,features='lxml')
    
    
    
    result['基本信息']['书名'] = s.xpath('//*[@id="wrapper"]/h1/span/text()')[0]

    info = soup.select('div[id="info"]')
    flag = 0
    lastKey = ""
    for i in info[0].contents:
        a = i.get_text().strip()
        a = re.sub('\\s|\n','',a)
        if(a != ""):
            # print('a[-1]',a[-1])
            if(a[-1] != ':' and flag == 0):
                b = a.split(":")
                result['基本信息'][b[0]] = b[1]
            else:
                if(flag == 0):
                    result['基本信息'][a] = ""
                    lastKey = a
                else:
                    result['基本信息'][lastKey] = a

                flag = (flag + 1) % 2
                

    

    a = str(soup.select('div[class="related_info"]'))
    if(re.findall('内容简介',a)):
        if(re.findall('all hidden',a)):
            contentIntro = soup.select('span[class="all hidden"] > div > div[class="intro"] > p')[0].get_text()
            # print(contentIntro)
        else:
            contentIntro = soup.select('div[class="indent"] > div > div[class="intro"] > p')[0].get_text()
            # print(contentIntro)
        result['内容简介']['intro'] = contentIntro
    if(re.findall('作者简介',a)):
        authorIntro = soup.select('div[class="indent"] > div > div[class="intro"]')[0].get_text().strip()
        result['作者简介']['intro'] = authorIntro


    # try:
    #     contentIntro = soup.select('span[class="all hidden"] > div > div[class="intro"] > p')[0].get_text()
    #     result['内容简介']['intro'] = contentIntro
    # except:
    #     pass

    # try:
    #     authorIntro = soup.select('div[class="indent"] > div > div[class="intro"]')[0].get_text().strip()
    #     result['作者简介']['intro'] = authorIntro
    # except:
    #     pass

    return result

if __name__ == '__main__':
    # print(getMovieURL())
    # responseText = doubanMovie('https://movie.douban.com/subject/1292052/')
    # result = handleMovieData(responseText)
    # print(result)
    responText = doubanBook('https://book.douban.com/subject/1046265/')
    result = handleBook(responText)
    print(result)