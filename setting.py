from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_DEFAULT = {
	'DB': 'mysql',
	'USER': 'guest',
	'PASSWORD': 'test_guest',
	'HOST': 'localhost',
	'PORT': '3306',
	'NAME': 'moko',
	'DRIVE': 'pymysql',
	'CHARSET': 'utf8'
	}


def get_db_uri(database: dict):
	db = database.get('DB') or 'mysql'
	user = database.get('USER') or 'root'
	password = database.get('PASSWORD') or 'root'
	host = database.get('HOST') or 'localhost'
	port = database.get('PORT') or '3306'
	drive = database.get('DRIVE') or 'pymysql'
	name = database.get('NAME')
	charset = database.get('CHARSET') or 'utf8'
	return '{}+{}://{}:{}@{}:{}/{}?charset={}'.format(db, drive, user, password, host, port, name, charset)


"""
使用SQLAlchemy
"""
# 创建连接数据库
engine = create_engine(get_db_uri(DATABASE_DEFAULT), echo = True)

# ORM基类
Base = declarative_base(bind = engine)

# 定义一个orm的入口 Session()类
Session = sessionmaker(bind = engine)
# 实例化这个类，后面需要用这个实例来执行sql操作
db_session = Session()


# 定义一个实现orm映射model到DB的类
class OrmSql(object):
	def __init__(self):
		self.engine = engine
		self.base = Base
		self.session = db_session
		# 把表创建进内存
		self.base.metadata.create_all(self.engine)
		# 把内存里的表写进数据库
		self.session.commit()
