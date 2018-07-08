import logging

from setting import db_session
from .models import *


def spider(new_html):
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
		try:
			model_list = [
				WomanModels(
						model_home = model['href'], publisher = model['publisher'],
						job = [Job(company = model['job'])]) for model in model_list
			]
			db_session.add_all(model_list)
			db_session.commit()
		except Exception as error:
			db_session.rollback()
			print(error)
	else:
		return None
