from sqlalchemy.orm import sessionmaker


# 定义一个实现orm映射sql的类
class OrmSql(object):
	# 首先初始化orm，模型表不存在就创建
	def __init__(self, engine, Base, models: object):
		self.engine = engine
		self.Base = Base
		self.models = models
		# 定义一个orm的入口 Session()类
		Session = sessionmaker(bind = self.engine)
		# 实例化这个类，后面需要用这个实例来执行sql操作
		self.session = Session()
		# 把表创建进数据库
		self.Base.metadata.create_all(self.engine)
		self.session.commit()
	
	def add_sql(self, d: dict):
		self.session.add(self.models.update_d(d))

