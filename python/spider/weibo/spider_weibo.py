import time

# from selenium import webdriver
import requests
import re
from lxml import etree


def get_res(url, cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400',
        'cookie': cookie
    }

    print(url)
    i = 0

    while 1:
        try:
            i += 1
            time.sleep(1)
            res = requests.get(url, headers=headers, timeout=(21, 60))
        except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
            print(e)
            print('           ~~~try ' + str(i) + ' times again~~~            ')
            if i > 3:
                return None
        else:
            print('success')
            return res
    # return None


def parse(html):
    pass


def get_user_comment(url, cookie):
    res = get_res(url, cookie)
    parse(res.text)
    res2 = get_res('https://weibo.com/ajax/statuses/show?id=LkgMPADdB', cookie)
    # id 在返回的字典里
    comment_url = 'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=4748310918730567&is_show_bulletin=2&is_mix=0&count=10&uid=1282440983'
    # 将id取出拼接进comment—_url中， 下一个id在comment_url 的返回字典里
    # uid 就是https://weibo.com/1282440983/LkgMPADdB 这个评论页面里的这串数字
    # 其他参数比如count可以改成 20，代表获取20个（搞多了容易出事）


def save_people_url():
    """保存搜索中用户的个人信息网址"""
    pass


def save_text():
    """保存用户在该话题下的发言等内容"""
    pass


def get_key_word(key_word='每天啥都不想干怎么办', page=2,
                 cookie='SINAGLOBAL=2291628449280.6514.1646918921232; SUB=_2A25PNbeCDeRhGeNP6FoZ9C7Iyj6IHXVs2dnKrDV8PUJbkNAKLUShkW1NSbWLCZYmHW4qAjrscEue0r5wnQo6QIFg; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5NSkNLqgONq9X2AFplTF2U5NHD95QfeKeR1hB7Sh2EWs4DqcjZdsLkwsLVwg8V97tt; UOR=,,weibo.cn; _s_tentry=-; Apache=7268522129070.696.1647436983956; ULV=1647436984017:4:4:2:7268522129070.696.1647436983956:1647435536143'
                 ):
    for i in range(1, page):
        res = get_res(
            'https://s.weibo.com/weibo?q=' + key_word + '&page=' + str(i), cookie)
        # 关键词搜索不用加%23
        print(res.text)  # 打印html源码看看（
        # with open('test.txt', 'w+', encoding='utf-8') as file:
        #     file.write(res.text)
        html = etree.HTML(res.text)  # lxml解析网页
        print(html.xpath('//*[@id="pl_feedlist_index"]/div[4]/div[1]/div[2]/div[1]/div[2]/p[2]/text()'))
        # xpath语句定位
        save_people_url()
        save_text()


def get_topic(key_word='每天啥都不想干怎么办', page=2,
              cookie='SINAGLOBAL=2291628449280.6514.1646918921232; SUB=_2A25PNbeCDeRhGeNP6FoZ9C7Iyj6IHXVs2dnKrDV8PUJbkNAKLUShkW1NSbWLCZYmHW4qAjrscEue0r5wnQo6QIFg; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5NSkNLqgONq9X2AFplTF2U5NHD95QfeKeR1hB7Sh2EWs4DqcjZdsLkwsLVwg8V97tt; UOR=,,weibo.cn; _s_tentry=-; Apache=7268522129070.696.1647436983956; ULV=1647436984017:4:4:2:7268522129070.696.1647436983956:1647435536143'
              ):
    for i in range(1, page):
        res = get_res(
            'https://s.weibo.com/weibo?q=%23' + key_word + '%23&page=' + str(i), cookie)
        # 话题需要加上%23才能搜索
        print(res.text)
        # with open('test.txt', 'w+', encoding='utf-8') as file:
        #     file.write(res.text)
        html = etree.HTML(res.text)
        print(html.xpath('//*[@id="pl_feedlist_index"]/div[4]/div[1]/div[2]/div[1]/div[2]/p[2]/text()'))
        # xpath语句定位
        user_url = html.xpath('//*[@id="scroller"]/div[1]/div[6]/div/article/div/header/div[1]/div/div[2]/a')
        # xpath匹配用户的详细界面
        get_user_comment(user_url, cookie)

        save_people_url()
        save_text()


get_topic()
