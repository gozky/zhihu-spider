# -*- coding: utf-8 -*-
# libray
import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://www.zhihu.com/people/jixin'
home_url = 'http://www.zhihu.com'
#dict()  存储话题名称，对应链接
topicDict = {}
# http请求头
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:32.0) Gecko/20100101 Firefox/32.0'}

homepage = requests.get(url, headers=headers)
soup = BeautifulSoup(homepage.content)

topic_tag = soup.find('div', id='zh-profile-following-topic')
topicList = topic_tag.find_all('a', class_='link')
for topic in topicList:
	name = topic.img['alt']
	topicDict[name] = home_url + topic['href']
# 生活 http://www.zhihu.com/topic/19551147	
for key in topicDict.keys():
	#print key, topicDict[key]
	topic_r = requests.get(topicDict[key], headers=headers)
	topic_soup = BeautifulSoup(topic_r.content)
	topStoryList_tag = topic_soup.find_all('div', id='zh-topic-top-page-list')
	#print len(topStoryList_tag)
	feed_item_list_tag = topStoryList_tag[0].find_all('div', class_='feed-item feed-item-hook folding')[0]
	# 获取每个话题第一篇文章
	topStory_tag = feed_item_list_tag.find('div',class_='feed-main')
	#print feed_item_list_tag
	title = topStory_tag.find('h2').string
	
	vote = topStory_tag.find('div', class_='zm-item-vote').a.string

	#detail = topStory_tag.find('div', class_='zm-editable-content')
	
	detail_url = home_url + topStory_tag.find('div', class_='zh-summary summary clearfix').a['href']
	print detail_url

	detail_r = requests.get(detail_url, headers=headers, verify=False)
	detail_soup = BeautifulSoup(detail_r.content)
	detail = detail_soup.find('div', class_='zm-editable-content clearfix')
	
	print title, vote
	print detail.get_text('\n')
