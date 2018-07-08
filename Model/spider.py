import logging
import time
from multiprocessing import Queue, Process
from multiprocessing.pool import Pool

import requests
from lxml import etree

from setting import db_session, HEADERS_DEFAULT, COOKIES, URL_DEFAULT
from .models import *


# 首页spider
def list_spider(url, q: Queue):
	new_resp = requests.get(url = URL_DEFAULT + url, headers = HEADERS_DEFAULT, cookies = COOKIES)
	new_html = etree.HTML(new_resp.text)
	"""
	1) Xpath模糊查找后用python处理
		/descendant::* 所有后代元素，等同于//*
	Elements = new_html.xpath('//*[@class="post small-post"]/descendant::*')
		| 管道符号，可以同时匹配前后两个条件，而且貌似是节点延伸匹配，可以用来自动排序
	elements_a_label = new_html.xpath(
			'//*[@class="post small-post"]//a|//*[@class="post small-post"]//img|//*[@class="post small-post"]//li//*')
		一步步分析需要的东西，减少匹配元素，提高效率，
		elements_a_label = new_html.xpath('//*[@class="post small-post"]//a|//*[@class="post small-post"]//li//*')
			==>Elements_a_img = new_html.xpath('//*[@class="post small-post"]//img')
				==>Elements_a_li = new_html.xpath('//*[@class="post small-post"]//li//*')
					==>获得包含全部元素的ElementList处理成pythonList，进一步过滤
	2) 直接用Xpath语法
		xpath_time = time.time()
		Elements_nickname = new_html.xpath('//*[@class="post small-post"]//a[@class="nickname"]')
		Elements_job = new_html.xpath(
				'//*[@class="post small-post"]//label[contains(text(),"职业")]/following::span[1]/text()')
		Elements_hits = new_html.xpath(
				'//*[@class="post small-post"]//label[contains(text(),"点击量")]/following::span[1]/text()')
		xpath_time = time.time() - xpath_time
	第二种方法，每多一条xpath语法，就比第一种慢一倍
	
	1) 实际情况发现不需要在首页获得点击量，但下面这种过于繁琐，不符合zen of python
		elements_a_label = new_html.xpath('//*[@class="post small-post"]//li//*')
		p = []
		element_list = []
		for i in range(len(elements_a_label)):
			if not i % 6 and elements_a_label[i + 1].attrib['title'] not in p:
				if db_session.query(WomanModels).filter(
						WomanModels.publisher == elements_a_label[i + 1].attrib['title']):
					p.append(elements_a_label[i + 1].attrib['title'])
					element_list.append(
							{
								y.text: elements_a_label[i + x + 1].text if not elements_a_label[i + x + 1].attrib else
								{
									'href': elements_a_label[i + x + 1].attrib['href'],
									'title': elements_a_label[i + x + 1].attrib['title']
								} for x, y in enumerate(elements_a_label[i:i + 4]) if not x % 2
							}
					)
		logging.debug(elements_a_label, element_list)
		# 进一步过滤掉男模
		elements_filter = [e for e in element_list if '男' not in e['发布人/']['title']]
	"""
	
	elements_nickname = new_html.xpath('//*[@class="post small-post"]//a[@class="nickname"]')
	elements_job = new_html.xpath(
			'//*[@class="post small-post"]//label[contains(text(),"职业")]/following::span[1]/text()')
	p = []
	model_list = []
	elements_nickname = [
		e for e in elements_nickname if '男' not in e.attrib['title']
		                                and '先生' not in e.attrib['title']
		                                and '绅士' not in e.attrib['title']
	]
	for i, e in enumerate(elements_nickname):
		if e.attrib['title'] not in p and db_session.query(
				WomanModels).filter(WomanModels.publisher == e.attrib['title']):
			p.append(e.attrib['title'])
			model_list.append(
					{
						'publisher': e.attrib['title'],
						'href': e.attrib['href'],
						'job': elements_job[i]
					}
			)
	if model_list:
		model_list = [
			WomanModels(
					model_home = model['href'], publisher = model['publisher'],
					job = [Job(company = model['job'])]) for model in model_list
		]
		db_session.add_all(model_list)
	next_url = new_html.xpath('//p[@class="page"]/a[@class="mBC wC"]/following::a[1:2]/@href')
	if next_url.startswith('/'):
		return next_url
	else:
		return None


# model个人信息spider
def model_post(url):
	new_resp = requests.get(url = URL_DEFAULT + 'profile' + url[:-1] + '.html', headers = HEADERS_DEFAULT,
			cookies = COOKIES)
	new_html = etree.HTML(new_resp.text)
	publisher = new_html.xpath('//a[@id=workNickName]/text()')
	w_model = db_session.query(WomanModels).filter_by(publisher = publisher)[0]
	
	w_model.mode_info = ModelInfo()


# model_show的spider
def model_show(url):
	new_resp = requests.get(url = URL_DEFAULT + 'post' + url + 'new/1.html', headers = HEADERS_DEFAULT,
			cookies = COOKIES)
	new_html = etree.HTML(new_resp.text)


# 一切的开始
def spider(url):
	list_q = Queue()
	list_q.put(url)
	_q = Queue()
	show_q = Queue()
	list_p = Pool(processes = 1)
	while True:
		# 当首页spider返回值为空的时候就关闭Pool并退出循环
		res = list_p.apply_async(func = list_spider, args = (list_q,), callback = list_q.put).get()
		list_p.close()
		time.sleep(2)
		if not res:
			break
	time.sleep(60)
	# 等首页spider至少运行一分钟，获得足够多的连接后，再开启其他spider
	
