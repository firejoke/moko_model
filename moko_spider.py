import logging

import requests
from lxml import etree

headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 '
	              'Safari/537.36'
	}

url = 'http://www.moko.cc/channels/post/23/1.html'
new_resp = requests.get(url = url, headers = headers)
new_html = etree.HTML(new_resp.text)
# /descendant::* 所有后代元素，等同于//*
# Elements = new_html.xpath('//*[@class="post small-post"]/descendant::*')
# | 管道符号，可以同时匹配前后两个条件，而且貌似是节点延伸匹配，可以用来自动排序
# Elements_a_img_label = new_html.xpath('//*[@class="post small-post"]//a|//*[@class="post small-post"]//img|//*[
# @class="post small-post"]//li//*')
# 一步步分析需要的东西，减少匹配元素，提高效率，
# Elements_a_img_label = new_html.xpath('//*[@class="post small-post"]//a|//*[@class="post small-post"]//li//*')
# Elements_a_img = new_html.xpath('//*[@class="post small-post"]//img')
# Elements_a_li = new_html.xpath('//*[@class="post small-post"]//li//*')
# logging.debug(Elements_a)
# Elements_a_img_label = new_html.xpath('//*[@class="post small-post"]//li//*')
Elements_a_img_label = new_html.xpath('//*[@class="post small-post"]//li//*')
# 过滤信息
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
logging.debug(Elements_filter)