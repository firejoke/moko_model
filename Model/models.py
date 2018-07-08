"""
模特对应的数据对象模型
分对象存放，便于整个项目的轻量运行
需要爬哪个数据，就调用哪个模型
"""

from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Table
from sqlalchemy.orm import relationship

from setting import Base

"""
model列表页没有经纪人信息，
但经纪人和model应该是对应的关系
所以设置一个UserBroker与WomanModels的中间表
"""
model_broker = Table(
		'UserBroker_WomanModels_Relation', Base.metadata,
		Column('id', Integer, primary_key = True),
		Column('models_id', Integer, ForeignKey('woman_models.id')),
		Column('broker_id', Integer, ForeignKey('user_broker.id'))
		)


# 经纪人
class UserBroker(Base):
	__tablename__ = 'user_broker'
	id = Column(Integer, primary_key = True, autoincrement = True)
	company = Column(String(128), nullable = True, index = True)
	broker = Column(String(16), nullable = True)
	broker_phone = Column(String(32), nullable = True)
	email = Column(String(128), nullable = True)
	woman_models = relationship(
			'WomanModels', secondary = model_broker, back_populates = 'user_broker', lazy = 'dynamic')
	
	def __repr__(self):
		return "< table_name: %s Model_property: %s>" % (self.__tablename__, self.__dict__)


class WomanModels(Base):
	__tablename__ = 'woman_models'
	id = Column(Integer, primary_key = True, autoincrement = True)
	# 个人首页
	model_home = Column(String(128))
	# 发布人
	publisher = Column(String(64), nullable = True, index = True, unique = True)
	model_info = relationship('ModelInfo', uselist = False)
	user_broker = relationship('UserBroker', secondary = model_broker, back_populates = 'woman_models')
	# moko账号可以设置最多三个职业
	job = relationship('Job', back_populates = 'models')
	
	def __repr__(self):
		return "< table_name: %s Model_property: %s>" % (self.__tablename__, self.__dict__)


class Job(Base):
	__tablename__ = 'job'
	id = Column(Integer, primary_key = True, autoincrement = True)
	company = Column(String(128), nullable = True)
	# 职位
	position = Column(String(32), nullable = True, index = True)
	# 工作经历
	experience = Column(Text, nullable = True)
	woman_models_id = Column(Integer, ForeignKey('woman_models.id'))
	models = relationship('WomanModels', back_populates = 'job')
	job_price = relationship('JobPrice', back_populates = 'job', lazy = 'dynamic')
	
	def __repr__(self):
		return "< table_name: %s Model_property: %s>" % (self.__tablename__, self.__dict__)


# 接单价格
class JobPrice(Base):
	__tablename__ = 'job_price'
	id = Column(Integer, primary_key = True, autoincrement = True)
	job_name = Column(String(128))
	price = Column(Integer)
	job_id = Column(Integer, ForeignKey('job.id'))
	job = relationship('Job', back_populates = 'job_price')
	
	def __repr__(self):
		return "< table_name: %s Model_property: %s>" % (self.__tablename__, self.__dict__)


class ModelInfo(Base):
	__tablename__ = 'model_info'
	id = Column(Integer, primary_key = True, autoincrement = True)
	# 生日
	birthday = Column(Date, nullable = True)
	# 星座
	constellation = Column(String(16), nullable = True, index = True)
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
	blood_group = Column(String(8), nullable = True)
	model_id = Column(Integer, ForeignKey('woman_models.id'))
	# woman_models = relationship('WomanModels',back_populates = 'models')
	school = relationship('School', back_populates = 'model_info')
	
	def __repr__(self):
		return "< table_name: %s Model_property: %s>" % (self.__tablename__, self.__dict__)


# 联系方式
class Contact(Base):
	__tablename__ = 'contact'
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
		return "< table_name: %s Model_property: %s>" % (self.__tablename__, self.__dict__)


class School(Base):
	__tablename__ = 'school'
	id = Column(Integer, primary_key = True, autoincrement = True)
	school_name = Column(String(128), nullable = True)
	model_info_id = Column(Integer, ForeignKey('model_info.id'))
	model_info = relationship('ModelInfo', back_populates = 'school')
	
	def __repr__(self):
		return "< table_name: %s Model_property: %s>" % (self.__tablename__, self.__dict__)
