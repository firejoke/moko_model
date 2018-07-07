# main
import logging
import os
import sys

import requests
from lxml import etree

from setting import HEADERS_DEFAULT, URL_DEFAULT, migrate

if __name__ == '__main__':
	# [print(dir_name) for dir_name in os.listdir('./')]
	"""
	Terminal
		$ python3 moko_spider.py model_name
	"""
	model_name = sys.argv[1].title()
	# 模型表映射
	migrate(model_name)
	model_path = os.path.join(os.path.dirname(__file__), model_name, 'config')
	with open(model_path, 'r') as md:
		index_url = md.read()
	print(URL_DEFAULT + index_url)
	new_resp = requests.get(url = URL_DEFAULT + index_url, headers = HEADERS_DEFAULT)
	new_html = etree.HTML(new_resp.text)
	"""
	1) Xpath模糊查找后用python处理
		/descendant::* 所有后代元素，等同于//*
	Elements = new_html.xpath('//*[@class="post small-post"]/descendant::*')
		| 管道符号，可以同时匹配前后两个条件，而且貌似是节点延伸匹配，可以用来自动排序
	Elements_a_img_label = new_html.xpath(
			'//*[@class="post small-post"]//a|//*[@class="post small-post"]//img|//*[@class="post small-post"]//li//*')
		一步步分析需要的东西，减少匹配元素，提高效率，
		Elements_a_img_label = new_html.xpath('//*[@class="post small-post"]//a|//*[@class="post small-post"]//li//*')
			==>Elements_a_img = new_html.xpath('//*[@class="post small-post"]//img')
				==>Elements_a_li = new_html.xpath('//*[@class="post small-post"]//li//*')
					==>获得包好全部元素的ElementList处理成pythonList，进一步过滤
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
	Elements_a_img_label = new_html.xpath('//*[@class="post small-post"]//li//*')
	Element_list = [{
		y.text: Elements_a_img_label[i + x + 1].text if not Elements_a_img_label[i + x + 1].attrib else
		{
			'href': Elements_a_img_label[i + x + 1].attrib['href'],
			'title': Elements_a_img_label[i + x + 1].attrib['title']
			} for x, y in enumerate(Elements_a_img_label[i:i + 6]) if not x % 2} for i, e in
		enumerate(Elements_a_img_label) if
		not i % 6]
	logging.debug(Element_list)
	# 进一步过滤掉男模
	Elements_filter = [e for e in Element_list if '男' not in e['发布人/']['title']]
	print(Elements_filter)
