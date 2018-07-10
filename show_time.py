"""
测试文档
"""
import logging
import re
from multiprocessing.pool import Pool

import requests
from lxml import etree

from Model.models import WomanModels
from setting import HEADERS_DEFAULT, COOKIES, db_session, URL_DEFAULT


new_resp = requests.get(url = URL_DEFAULT + '/post/686235.html', headers = HEADERS_DEFAULT, cookies = COOKIES)
new_html = etree.HTML(new_resp.text)
photo_list = new_html.xpath('//p[@class="picBox"]//img/@src2')
model_home = new_html.xpath('//a[@id="workNickName"]/@href')[0]
hits = new_html.xpath('//a[@class="sPoint gC"]/text()')[0]
create_time = new_html.xpath('//p[@class="date gC1"]/text()')[0]
title = new_html.xpath('//h2[@class="text dBd_1"]/a/text()')[0]
logging.debug(photo_list)