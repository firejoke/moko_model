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
	"""
	elements_a_label = new_html.xpath('//*[@class="post small-post"]//li//*')
	p = []
	element_list = []
	for i, e in enumerate(elements_a_label):
		if not i % 6 and elements_a_label[i + 1].attrib['title'] not in p:
			# if
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
	logging.debug(elements_filter)
	try:
		model_list = [
			WomanModels(
					model_home = element['发布人/']['href'], publisher = element['发布人/']['title'],
					job = [Job(company = element['职业/'])]) for element in elements_filter
		]
		db_session.bulk_save_objects(model_list)
		logging.debug(model_list)
	# model_job_list = [
	# 	model_list[i].job([Job(company = element['职业/'])]) for i, element in enumerate(elements_filter)
	# 	]
	# db_session.bulk_save_objects(model_job_list)
	# db_session.commit()
	except Exception as e:
		db_session.rollback()
		print(e)
