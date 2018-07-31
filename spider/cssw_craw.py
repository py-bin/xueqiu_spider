# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 10:18:12 2018

@author: bin

因为雪球讨论仅能爬取前100页，因此需要按照不同的排序抽取前100页，再去重，
得到更多的评价。更改排序在craw_html()中paras的sort。第一次爬取时间是2018-07-24 10:30
"""

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
import time
import random
import mysqls
from datetime import datetime
from datetime import timedelta
ua = UserAgent()
dt_now = datetime.now()

def craw_html(myurl, page_n):
    headers = {
        'User-Agent':ua.random,
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Host': 'xueqiu.com',
        'Upgrade-Insecure-Requests':'1',
        'Cookie':'_ga=GA1.2.1905714326.1532395769; _gid=GA1.2.919312161.1532395769; device_id=be9593a249df60ae51b867286720b231; __utmz=1.1532398933.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); s=eu15gphfkh; xq_a_token=f43ff28fe0acc77123e46a2c2d7f1c845fd07937; xqat=f43ff28fe0acc77123e46a2c2d7f1c845fd07937; xq_r_token=821c39fc7da3072d6bbf86fa6f0168da62863f2b; xq_token_expire=Sat%20Aug%2018%202018%2017%3A04%3A05%20GMT%2B0800%20(CST); xq_is_login=1; u=7390884115; __utma=1.1905714326.1532395769.1532398933.1532434163.2; aliyungf_tc=AQAAAAed2SQy+gUAgrpscUgXW0sYjseA; Hm_lvt_1db88642e346389874251b5a1eded6e3=1532395769,1532398921,1532434152,1532480485; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1532480490'
    }
    paras = {
#        'sort':'relevance',
        'sort':'time',
#        'sort':'reply',
        'source':'user',
        'q':'长生生物',
        'count':10,
        'page':page_n
        }
    response = requests.get(myurl,headers=headers,params=paras)
    try:
        response.raise_for_status()
        return response.text
    except:
        print('爬取异常')

def parse_time(thetime):
    #处理爬取时间格式异常问题，如“今天 08:30”、“20分钟前”
    
    if '今天' in thetime:
        rst = thetime.replace('今天',dt_now.strftime('%Y-%m-%d'))
    elif '昨天' in thetime:
        the_time = dt_now - timedelta(days=1)
        rst = thetime.replace('昨天',the_time.strftime('%Y-%m-%d'))
    elif '分钟前' in thetime:
        the_min = int(thetime[:-3])
        the_time = dt_now - timedelta(minutes=the_min)
        rst = the_time.strftime('%Y-%m-%d %H:%M')
    elif '秒前' in thetime:
        rst = dt_now.strftime('%Y-%m-%d %H:%M')
    elif len(thetime)== 11:
        rst = '2018-' + thetime
    else:
        rst = thetime
    return rst     
        
def parse_onepage(html):
    data = json.loads(html)['list']
    for item in data:
        yield {
        'id':item['id'],
        'user_id':item["user_id"], #用户ID
        'title':html_parser(item["title"]), #评论标题
        'text':html_parser(item["text"]), #评论正文
        "retweet_count":item["retweet_count"], #转发数量
        "reply_count":item["reply_count"], #回复数量
        "fav_count":item["fav_count"], #点赞数量
        "type":item["type"],
        'user_friends_count':item["user"]['friends_count'], #被关注量
        'user_followers_count':item["user"]['followers_count'], #粉丝数
        'user_status_count':item["user"]['status_count'], #发帖量
        'user_province':item["user"]['province'], #用户省份
        'timeBefore':parse_time(item['timeBefore']) #时间
        }

def html_parser(jsontxt):
    data_soup = BeautifulSoup(jsontxt,'html.parser')
    parser_txt = data_soup.text.replace('\xa0','')
    return parser_txt

def main_craw():
    url = 'https://xueqiu.com/statuses/search.json'
    for i in range(1,100):
        html = craw_html(url,i)
        print('正在保存第%d页。'% i)
        for item in parse_onepage(html):
            mysqls.save_data(item)
        time.sleep(1 + float(random.randint(1, 100)) / 20)
        
if __name__ == '__main__':
	main_craw()