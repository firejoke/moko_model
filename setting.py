"""
使用SQLAlchemy
"""

import os
import re
from importlib import import_module
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 获取数据库配置文档
db_config = os.path.join(os.path.dirname(__file__), 'db_config')
with open(db_config, 'r') as f:
	f = f.read()
	db = re.search(r"DB=(\w.*)?", f).group()[3:] or 'mysql'
	user = re.search(r"USER=(\w.*)?", f).group()[5:] or 'root'
	password = re.search(r"PASSWORD=(\w.*)?", f).group()[9:] or 'root'
	host = re.search(r"HOST=(\w.*)?", f).group()[5:] or 'localhost'
	port = re.search(r"PORT=(\w.*)?", f).group()[5:] or '3306'
	drive = re.search(r"DRIVE=(\w.*)?", f).group()[6:] or 'pymysql'
	name = re.search(r"NAME=(\w.*)?", f).group()[5:]
	charset = re.search(r"CHARSET=(\w.*)?", f, flags = re.I).group()[8:] or 'utf8'
	DATABASE_DEFAULT = '{}+{}://{}:{}@{}:{}/{}?charset={}'.format(db, drive, user, password, host, port, name, charset)

# 创建连接数据库
engine = create_engine('mysql+pymysql://guest:test_guest@localhost:3306/moko?charset=utf8', echo = True)
# ORM基类
Base = declarative_base(bind = engine)
# 配置orm数据库入口 Session()类
Session = sessionmaker(bind = engine)
# 实例化，后面需要用这个实例来执行sql操作
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
		Base.metadata.create_all()
		# 把内存里的表写进数据库
		db_session.commit()
	
	except (ImportError, TypeError) as e:
		print(e)
		db_session.rollback()


HEADERS_DEFAULT = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 '
	              'Safari/537.36'
	}

COOKIES = dict(
		LAST_LOGIN_EMAIL='335856032@qq.com',
		NEWMOKO_USER_LOGINKEY='0419d041-65c2-4f8d-82a3-ba696270338e',
		Hm_lvt_8d82e75c6168ba4bc0135a08edae2a2e='1530839622,1530925845,1530941756,1531019852',
		JSESSIONID='E1666EF3E6CC39F5B4F382F7386CFC72',
		Hm_lpvt_8d82e75c6168ba4bc0135a08edae2a2e='1531038268'
)

URL_DEFAULT = 'http://www.moko.cc/'
