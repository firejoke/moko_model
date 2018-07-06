"""
使用SQLAlchemy
"""
from importlib import import_module
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


# 创建连接数据库
engine = create_engine(get_db_uri(DATABASE_DEFAULT), echo = True)
# ORM基类
Base = declarative_base(bind = engine)
# 配置一个orm的写入数据库入口 Session()类
Session = sessionmaker(bind = engine)
# 实例化这个类，后面需要用这个实例来执行sql操作
db_session = Session()


def migrate(model_path: str = None):
	"""
	定义一个实现orm映射model到DB的方法
	因为在commit之前，所有的表创建与操作实际上是在内存里
	试着用实例化某个模型的方式来实现自由映射模型
	避免用create_all()来映射所有继承Base的模型
	但不行
	所以尝试动态导入模型来自由映射
		main_dir/
			test/
				models
	import_module("test.models")
	"""
	try:
		# 动态导入要映射的模型
		import_module(model_path + "." + "models" if model_path else "models")
		# 把表创建进内存
		Base.metadata.create_all(engine)
		# 把内存里的表写进数据库
		db_session.commit()
	except (ImportError, TypeError):
		db_session.rollback()


HEADERS_DEFAULT = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 '
	              'Safari/537.36'
	}

URL_DEFAULT = 'http://www.moko.cc/channels/post'
