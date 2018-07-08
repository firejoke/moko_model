"""
测试文档
"""
import logging

import requests
from lxml import etree

from Model.models import WomanModels
from setting import HEADERS_DEFAULT, COOKIES, db_session

q = db_session.query(WomanModels).order_by(WomanModels.id)[0].model_home
logging.debug(q)