"""
测试文档
"""
import logging
import re
from multiprocessing import Queue
from multiprocessing.pool import Pool

import requests
from lxml import etree

# from Model.models import WomanModels
from setting import HEADERS_DEFAULT, COOKIES, db_session, URL_DEFAULT

new_resp = requests.get(url = 'http://www.moko.cc/post/1256601.html', headers = HEADERS_DEFAULT)
new_html = etree.HTML(new_resp.text)
create_time = new_html.xpath('//p[@class="date gC1"]/text()')[0]
title = new_html.xpath('//h2[@class="text dBd_1"]/a/text()')
title = title if title else new_html.xpath('//h2[@class="text dBd_1"]/a/@title')[0]
photo_list = new_html.xpath('//p[@class="picBox"]//img/@src2')
logging.debug(create_time,title,photo_list)
