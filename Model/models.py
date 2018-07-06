"""
模特对应的数据对象模型
分对象存放，便于整个项目的轻量运行
需要爬哪个数据，就调用哪个模型
"""
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship

from setting import Base


class WomanModels(Base):
	__tablename__ = 'woman_models'
	id = Column(Integer, primary_key = True, autoincrement = True)
	# 发布人
	publisher = Column(String(64), nullable = True)
	# 职业
	job = Column(String(32), nullable = True)
	# 点击量
	hits = Column(Integer, nullable = True)
	
	def __repr__(self):
		return "< model_name is %s >" % self.__name__


class ModelInfo(Base):
	__tablename__ = 'model_info'
	id = Column(Integer, primary_key = True, autoincrement = True)
	# 生日
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
	# 血型
	blood_group = Column(String(8))
	model_id = Column(Integer, ForeignKey('woman_models.id'))
	
	def __repr__(self):
		return "< model_name is %s >" % self.__name__


# 连接model_info与woman_models的双向关系
WomanModels.model_info = relationship('model_info', order_by = 'model_info.id', back_populates = 'woman_models',
		userlist = False)


# 联系方式
class Contact(Base):
	id = Column(Integer, primary_key = True, autoincrement = True)
	# 真实姓名，估计没有
	m_name = Column(String(128), nullable = True)
	email = Column(String(255), nullable = True)
	msn = Column(String(255), nullable = True)
	phone = Column(String(16), nullable = True)
	phone_b = Column(String(16), nullable = True)
	wechat = Column(String(64), nullable = True)
	qq = Column(String(16), nullable = True)
	
	def __repr__(self):
		return "< model_name is %s >" % self.__name__


# 经纪人
class UserBroker(Base):
	pass