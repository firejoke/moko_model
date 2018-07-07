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
	company = Column(String(128), nullable = True, index = True)
	broker = Column(String(16), nullable = True)
	broker_phone = Column(String(32), nullable = True)
	email = Column(String(128), nullable = True)
	
	def __repr__(self):
		return "< model_name is %s, table_name: %s, model_items>" % self.__name__, self.__tablename__, \
			vars(self.__class__).items()


# UserBroker与WomanModels的多对多中间表
model_broker = Table(
		'UserBroker_WomanModels_Relation', Base.metadata,
		Column('id', Integer, primary_key = True),
		Column('models_id', Integer, ForeignKey('woman_models.id')),
		Column('broker_id', Integer, ForeignKey('user_broker.id'))
		)
UserBroker.woman_models = relationship(
		'woman_models', secondary = model_broker, back_populates = 'user_broker'
		)


class WomanModels(Base):
	__tablename__ = 'woman_models'
	id = Column(Integer, primary_key = True, autoincrement = True)
	# 发布人
	publisher = Column(String(64), nullable = True, index = True)
	# 点击量
	hits = Column(Integer, nullable = True)
	model_info = relationship(
			'model_info', back_populates = 'woman_models', userlist = False
			)
	user_broker = relationship(
			'user_broker', secondary = model_broker, back_populates = 'woman_models'
			)
	
	def __repr__(self):
		return "< model_name is %s, table_name: %s, model_items>" % self.__name__, self.__tablename__, \
			vars(self.__class__).items()


# woman_models与job的中间表
model_job = Table(
		'Model_Job_Relation', Base.metadata,
		Column('id', Integer, primary_key = True),
		Column('model_id', Integer, ForeignKey('woman_models.id')),
		Column('job_id', Integer, ForeignKey('job.id'))
		)

# moko账号可以设置最多三个职业
WomanModels.job = relationship('job', secondary = model_job, back_populates = 'woman_models')


class Job(Base):
	__tablename__ = 'job'
	id = Column(Integer, primary_key = True, autoincrement = True)
	company = Column(String(128), nullable = True)
	# 职位
	position = Column(String(32), nullable = True, index = True)
	# 工作经历
	experience = Column(Text, nullable = True)
	models = relationship('woman_models', secondary = model_job, back_populates = 'job')
	job_price = relationship('job_price', back_populates = 'job', userlist = False)
	
	def __repr__(self):
		return "< model_name is %s, table_name: %s, model_items>" % self.__name__, self.__tablename__, \
			vars(self.__class__).items()


# 接单价格
class JobPrice(Base):
	__tablename__ = 'job_price'
	id = Column(Integer, primary_key = True, autoincrement = True)
	job_name = Column(String(128))
	price = Column(Integer)
	job_id = Column(Integer, ForeignKey('job.id'))
	
	def __repr__(self):
		return "< model_name is %s, table_name: %s, model_items>" % self.__name__, self.__tablename__, \
			vars(self.__class__).items()


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
	contact = relationship('contact', back_populates = 'model_info', userlist = False)
	school = relationship('school', back_populates = 'model_info', userlist = False)
	
	def __repr__(self):
		return "< model_name is %s, table_name: %s, model_items>" % self.__name__, self.__tablename__, \
			vars(self.__class__).items()


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
		return "< model_name is %s, table_name: %s, model_items>" % self.__name__, self.__tablename__, \
			vars(self.__class__).items()


class School(Base):
	__tablename__ = 'school'
	id = Column(Integer, primary_key = True, autoincrement = True)
	school_name = Column(String(128), nullable = True)
	model_info_id = Column(Integer, ForeignKey('model_info.id'))
	
	def __repr__(self):
		return "< model_name is %s, table_name: %s, model_items>" % self.__name__, self.__tablename__, \
			vars(self.__class__).items()
