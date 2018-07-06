"""
模特对应的数据对象模型
分对象存放，便于整个项目的轻量运行
需要爬哪个数据，就调用哪个模型
"""
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey

from setting import Base


class WomanModels(Base):
	__tablename__ = 'models'
	id = Column(Integer, primary_key = True, autoincrement = True)
	# 发布人
	publisher = Column(String(64), nullable = True)
	# 职业
	job = Column(String(32), nullable = True)
	# 点击量
	hits = Column(Integer, nullable = True)


class ModelInfo(Base):
	__tablename__ = 'model_info'
	id = Column(Integer, primary_key = True, autoincrement = True)
	birthday = Column(Date, nullable = True)
	# 星座
	constellation = Column(String(16), nullable = True)
	# 身高
	height = Column(Integer, nullable = True)
	# 体重
	weight = Column(Integer, nullable = True)
	# 三围
	shape = Column(String(16), nullable = True)
	# 发色
	hair_color = Column(String(8), nullable = True)
	# 眼睛颜色
	eye_color = Column(String(8), nullable = True)
	# 鞋码
	shoe_size = Column(Integer, nullable = True)
	# 工作经历
	work_experience = Column(Text, nullable = True)
	
	def __init__(self):
		super(ModelInfo, self)


class Contact(Base):
	pass
