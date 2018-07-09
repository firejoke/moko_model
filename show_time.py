"""
测试文档
"""
import logging
import re

import requests
from lxml import etree

from Model.models import WomanModels
from setting import HEADERS_DEFAULT, COOKIES, db_session, URL_DEFAULT



# w_model = db_session.query(WomanModels).filter_by(publisher = publisher)[0].model_info