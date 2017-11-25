# -*- coding=utf8 -*-

import sys
import time
import requests
from bs4 import BeautifulSoup
from sendMsg import send_message
from random import choice
import pickle

#豆瓣小组地址
link_address = 'https://www.douban.com/group/beijing/discussion'

headers = {'Host': 'www.douban.com', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding': 'gzip, deflate, br',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0', 'Content-Type': 'application/x-www-form-urlencoded'}

headers['Referer'] = link_address

# 直接复制浏览器post时候的cookie
# ck和dbcl2配对使用，其它都不变
cookies = {
    'cookie': 'bid=Vx-ox_zzrl8; _pk_id.100001.8cb4=ceadb9b05b5fbbf1.1510362607.5.1511075585.1511063662.; __utma=30149280.1472864593.1510362611.1511062523.1511070214.5; __utmz=30149280.1510362611.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __yadk_uid=SqtZsWCoLdfVNBSaDJefXdZjaHJhg9Hr; ps=y; ue="mengqi1984@gmail.com"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.446; ap=1; ll="108288"; __utmc=30149280; _pk_ses.100001.8cb4=*; __utmb=30149280.154.5.1511075587345; ct=y; dbcl2="4462152:JX6267qxQvU"; ck=DFIy; __utmt=1'}

#回复内容， 会随机从中选一条内容进行回复
g_comments = []

#某小组某页的帖子主题链接
g_topics_cache = []

g_my_groups = ['https://www.douban.com/group/beijing/', 'https://www.douban.com/group/166127/', 'https://www.douban.com/group/596374/', 'https://www.douban.com/group/519193/']

def reconstructHeaders():
    #change link address
    # select on link from my groups
    global link_address
    global headers

    headers['Referer'] = link_address
    link_address = choice(g_my_groups) + 'discussion'

    print (link_address)
    print (headers)


def autoreply_douban_links(topic_address):
    #randomly choose a comment to reply
    comment = choice(g_comments)
    print ('adding comment {} to address {}'.format(comment, topic_address))

    post_url = topic_address + 'add_comment'

    # ck 是从浏览器post中看出来的
    payload = dict(ck='DFIy', rv_comment=comment, start='0', submit_btn='加上去')

    r = requests.post(post_url, data=payload, cookies=cookies, headers=headers)
    # print(r.text)


def getAllTopicLinks(page = 50):
    content = requests.get(url = link_address, params={'start' : page}, cookies=cookies, headers=headers).content
    soup = BeautifulSoup(content, 'html.parser')
    # print soup

    if '检测到有异常' in soup.encode('utf-8'):
        print ('检测到有异常请求从你的 IP 发出, cookie超时')
        send_message(["27130723@qq.com"], "douban-cookie超时", 'douban-cookie超时')
        exit()
    
    #clear topics cache
    g_topics_cache[:] = []

    for tr in soup.find_all('tr'):
        # print tr 
        tr_topic = '' # a link for that topic
        tr_people = '' # a link for that people
        for tr_a in tr.find_all('a'):
            tr_a_href = tr_a.get('href')
            if 'topic' in tr_a_href:
                tr_topic = tr_a_href
            elif 'people' in tr_a_href:
                tr_people = tr_a_href

        # this is a topic
        if tr_topic is not '' and tr_people is not '':
            if tr_topic in g_topics_cache:
                pass
            else:
                #cache it
                g_topics_cache.append(tr_topic)
        else:
            pass


def loopTask():
    # start loop
    while(True):
        try:
            print ('randomly change group')
            reconstructHeaders()
            print ('spidering topics')
            getAllTopicLinks()
            print (g_topics_cache)

            durations = [10,5]  # reply durations
            for duration in durations:
                #random choose a topic to reply
                reply_topic_link = choice(g_topics_cache)
                autoreply_douban_links(reply_topic_link)

                time.sleep(60 * duration)
        except Exception, e:
            print e


def load_comments_fromfile(filename='xljt.txt', content=g_comments):
    with open(filename) as fh:
        for line in fh:
            content.append(line)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    print ("reply-randomly main starts")

    print ('loading comments')
    load_comments_fromfile()

    print ('start looping')
    loopTask()
