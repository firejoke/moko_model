# main
import logging
import os
import sys
from importlib import import_module

import requests
from lxml import etree

from setting import HEADERS_DEFAULT, URL_DEFAULT, migrate, db_session

if __name__ == '__main__':
	# [print(dir_name) for dir_name in os.listdir('./')]
	"""
	Terminal
		$ python3 moko_spider.py model_name
	"""
	try:
		# sys.argv[1].title()
		model_name = 'Model'
		# 模型表映射
		migrate(model_name)
		model_path = os.path.join(os.path.dirname(__file__), model_name, 'config')
		with open(model_path, 'r') as md:
			index_url = md.read()
		print(URL_DEFAULT + index_url)
		new_resp = requests.get(url = URL_DEFAULT + index_url, headers = HEADERS_DEFAULT)
		new_html = etree.HTML(new_resp.text)
		# 动态导入对应模块的spider
		module = import_module(model_name + "." + "spider")
		module.spider(new_html)
		# logging.debug(db_session)
	except Exception as e:
		print(e, '\n', '没有该模块')
