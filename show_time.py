"""
测试文档
"""
import logging

import requests
from lxml import etree

# from Model.models import WomanModels
from setting import HEADERS_DEFAULT, COOKIES, db_session, URL_DEFAULT

new_resp = requests.get(url = URL_DEFAULT + 'channels/post/23/10.html', headers = HEADERS_DEFAULT,
			cookies = COOKIES)
new_html = etree.HTML(new_resp.text)
info_list = new_html.xpath('//*[@class="post small-post"]//a/@*')
logging.debug(info_list)
