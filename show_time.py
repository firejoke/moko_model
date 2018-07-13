"""
测试文档
"""
import logging

from Model.models import WomanModels, ModelInfo
from setting import db_session

model_info = db_session.query(ModelInfo).filter_by(model_id = 225).all()
logging.debug(model_info)
