"""
测试文档
"""
import logging
import re

import requests
from lxml import etree

from Model.models import WomanModels
from setting import HEADERS_DEFAULT, COOKIES, db_session, URL_DEFAULT

new_resp = requests.get(url = URL_DEFAULT + '/post/lijiaji/new/4.html', headers = HEADERS_DEFAULT, cookies = COOKIES)
new_html = etree.HTML(new_resp.text)
n = new_html.xpath('//*[@class="coverBg wC"]/@href')
logging.debug(n)
next_url = n[0]
logging.debug(next_url)