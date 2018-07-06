"""
模特对应的数据对象模型
分对象存放，便于整个项目的轻量运行
需要爬哪个数据，就调用哪个模型
"""
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Table
from sqlalchemy.orm import relationship

from setting import Base


# 经纪人
class UserBroker(Base):
	__tablename__ = 'user_broker'
	id = Column(Integer, primary_key = True, autoincrement = True)
	
	def __repr__(self):
		return "< model_name is %s >" % self.__name__


# UserBroker与WomanModels的多对多中间表
registrations = Table(
		'UserBroker_WomanModels_Relation', Base.metadata,
		Column('models_id', ForeignKey('woman_models.id'), primary_key = True, ),
		Column('broker_id', ForeignKey('user_broker.id'), primary_key = True)
		)
UserBroker.woman_models = relationship(
		'woman_models', secondary = registrations, back_populates = 'user_broker'
		)


class WomanModels(Base):
	__tablename__ = 'woman_models'
	id = Column(Integer, primary_key = True, autoincrement = True)
	# 发布人
	publisher = Column(String(64), nullable = True)
	# 职业
	job = Column(String(32), nullable = True)
	# 点击量
	hits = Column(Integer, nullable = True)
	# 连接model_info与woman_models的双向关系
	model_info = relationship(
			'model_info', back_populates = 'woman_models', userlist = False
			)
	user_broker = relationship(
			'user_broker', secondary = registrations, back_populates = 'woman_models'
			)
	
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
	# 连接contact与model_info
	contact = relationship('contact', back_populates = 'model_info', userlist = False)
	
	def __repr__(self):
		return "< model_name is %s >" % self.__name__


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
	model_info_id = Column(Integer, ForeignKey('model_info.id'))
	
	def __repr__(self):
		return "< model_name is %s >" % self.__name__
