from sqlalchemy import create_engine

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
使用sqlalchemy模型
"""
# 创建连接数据库
engine = create_engine(get_db_uri(DATABASE_DEFAULT), echo = True)

# ORM基类
Base = declarative_base(bind = engine)