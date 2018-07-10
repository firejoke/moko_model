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
from setting import HEADERS_DEFAULT, COOKIES, db_session, URL_DEFAULT, migrate

# model_show_url_list = db_session.query(WomanModels.model_home, WomanModels.id) \
# 						.filter(WomanModels.id.in_(range(0,10)))
# model_show_url_list = list(model_show_url_list)
# logging.debug(model_show_url_list)
migrate('Model')