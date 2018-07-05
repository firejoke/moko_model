from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey

from setting import Base


class DbModels(Base):
	# 提供一个用字典给字段赋值的方法
	def update_d(self, d: dict):
		"""
		一个用来检查传进来的dict的keys是否属于模型字段的集合，用于避免脏数据
		class U(object):
			def __init__(self, name, age, sex):
				self.name = name
				self.age = age
				self.sex = sex
			def update_d(self, d):
				if 'id' not in d.keys():
					if set(d).issubset(set(self.__dict__)):
						raise KeyError('%s.keys is range out self' % d)
					else:
						for k, v in d.items():
							setattr(self, k, v)
				else:
					raise KeyError("'id' can not be in d.keys")
		"""
		if 'id' not in d.keys():
			if set(d).issubset(set(self.__dict__)):
				for k, v in d.items():
					setattr(self, k, v)
			else:
				return 'd.keys is range out Model.__dict__.keys'
		else:
			return "'id' can not be in d.keys"


class WomanModels(DbModels):
	__tablename__ = 'models'
	id = Column(Integer, primary_key = True, autoincrement = True)
	# 发布人
	publisher = Column(String(64), nullable = True)
	# 职业
	job = Column(String(32), nullable = True)
	# 点击量
	hits = Column(Integer, nullable = True)


class ModelInfo(DbModels):
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


class Contact(DbModels):
	pass


class U(object):
	def __init__(self):
		self.name = 'yy'
		self.age = 20
		self.sex = 'girl'
	
	def update_d(self, d):
		if set(d).issubset(set(self.__dict__)):
			for k, v in d.items():
				setattr(self, k, v)
		else:
			raise KeyError('%s.keys is range out self' % d)


class Sub(U):
	money = 20000
	pass
