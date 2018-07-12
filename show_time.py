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

new_resp = requests.get(url = 'http://www.moko.cc/profile/lijiaji.html', headers = HEADERS_DEFAULT)
new_html = etree.HTML(new_resp.text)
info_list = new_html.xpath('//div[@class="profile-module-box profile-line-module"]//*')
position_list = new_html.xpath('//*[@class="b gC"]/text()')
logging.debug(info_list,position_list)