"""
测试文档
"""
import logging

import requests
from lxml import etree

from Model.models import WomanModels
from setting import HEADERS_DEFAULT, COOKIES, db_session

q = db_session.query(WomanModels).filter_by(publisher = '晓琳少年lin')[0]
logging.debug(q)
