"""
模特对应的数据对象模型
分对象存放，便于整个项目的轻量运行
需要爬哪个数据，就调用哪个模型
"""

from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Table, \
    DateTime
from sqlalchemy.orm import relationship

from setting import Base

"""
model列表页没有经纪人信息，
但经纪人和model应该是对应的关系
所以设置一个UserBroker与WomanModels的中间表
这种中间表最好只负责用来存两个关系表的关系
不要添加其他字段，用对应两个表的外键做联合主键
"""
model_broker = Table(
    'UserBroker_WomanModels_Relation', Base.metadata,
    Column('models_id', Integer, ForeignKey('woman_models.id')),
    Column('broker_id', Integer, ForeignKey('user_broker.id'))
)


# 经纪人
class UserBroker(Base):
    __tablename__ = 'user_broker'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 签约公司名
    company = Column(String(128), nullable=True, index=True)
    # 经纪人名
    broker = Column(String(16), nullable=True)
    broker_phone = Column(String(32), nullable=True)
    broker_email = Column(String(128), nullable=True)
    # 给relationship字段添加一个secondary属性，指向中间表
    # 另:
    # ！！！第一个坑，relationship 的第一个属性是Base模型的名称，并不是对应的table name
    # ！！！第二个坑，back_populates 是指向的关联表对应的relationship，
    # 并不是Base模型名或者table name
    woman_models = relationship(
        'WomanModels',
        secondary=model_broker,
        back_populates='user_broker',
        lazy='dynamic')

    def __repr__(self):
        return "< table_name: %s Model_property: %s>" % (
            self.__tablename__, self.__dict__)


class WomanModels(Base):
    __tablename__ = 'woman_models'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 个人首页
    model_home = Column(String(128))
    # 发布人
    publisher = Column(String(64), nullable=True, index=True, unique=True)
    # 一对一的关系表，要把uselist设置成 False
    model_info = relationship('ModelInfo', uselist=False)
    user_broker = relationship(
        'UserBroker',
        secondary=model_broker,
        back_populates='woman_models')
    # moko账号可以设置最多三个职业
    # 可是三个职业并没有分配三个类的职业作品展示...所有展示都是一个页面
    # 也许它数据库是分了的，但是没有做分类页面，就不好匹配了
    # (必须要把相册名和相关职业做模糊匹配......)
    job = relationship('Job', uselist=False)
    school = relationship('School', uselist=False)
    # 如果是单纯的one to many 关系，并不需要 many query one，
    # 那就不要设置back_populates属性（我理解为是回调）
    show = relationship('ModelShow', lazy='dynamic')

    def __repr__(self):
        return "< table_name: %s Model_property: %s>" % (
            self.__tablename__, self.__dict__)


# 居然作品没跟工作类关联在一起，moko这个页面真是......
class ModelShow(Base):
    __tablename__ = 'model_show'
    id = Column(Integer, primary_key=True, autoincrement=True)
    href = Column(String(255))
    create_time = Column(DateTime)
    title = Column(String(64))
    hits = Column(Integer)
    # 外键指向的是实际 table 的 column，总之只要是设置 Column 就要用实际 table 属性，
    # 而不是模型属性
    model_id = Column(Integer, ForeignKey('woman_models.id'))

    def __repr__(self):
        return "< table_name: %s Model_property: %s>" % (
            self.__tablename__, self.__dict__)


class Job(Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 所在公司，所在公司和签约公司有啥区别......moko这个数据库真是受不了
    now_company = Column(String(128))
    # 头衔
    title = Column(String(64))
    # 职业
    position = Column(String(32), nullable=True, index=True)
    # 第二职业
    psoition_second = Column(String(32), nullable=True, index=True)
    # 第三职业
    psoition_third = Column(String(32), nullable=True, index=True)
    # 工作经历
    experience = Column(Text, nullable=True)
    # 奖项
    trophies = Column(Text, nullable=True)
    # 最高奖项
    top_trophies = Column(Text, nullable=True)
    # 展览作品描述
    show_works = Column(Text, nullable=True)
    # 其他作品描述
    other_works = Column(Text, nullable=True)
    models_id = Column(Integer, ForeignKey('woman_models.id'))
    job_price = relationship('JobPrice', lazy='dynamic')

    def __repr__(self):
        return "< table_name: %s Model_property: %s>" % (
            self.__tablename__, self.__dict__)


# 接单价格
class JobPrice(Base):
    __tablename__ = 'job_price'
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_name = Column(String(128))
    price_lower = Column(Integer, nullable=True, index=True)
    price_up = Column(Integer, nullable=True, index=True)
    job_id = Column(Integer, ForeignKey('job.id'))

    def __repr__(self):
        return "< table_name: %s Model_property: %s>" % (
            self.__tablename__, self.__dict__)


class ModelInfo(Base):
    __tablename__ = 'model_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 生日
    birthday = Column(Date, nullable=True)
    # 星座
    constellation = Column(String(16), nullable=True, index=True)
    # 身高
    height = Column(Integer, nullable=True)
    # 体重
    weight = Column(Integer, nullable=True)
    # 三围
    shape = Column(String(16), nullable=True)
    # 发色
    hair_color = Column(String(8), nullable=True)
    # 眼睛颜色
    eye_color = Column(String(8), nullable=True)
    # 鞋码
    shoe_size = Column(Integer, nullable=True)
    # 血型
    blood_group = Column(String(8), nullable=True)
    model_id = Column(Integer, ForeignKey('woman_models.id'))
    hobby = relationship('Hobby', uselist=False)
    contact = relationship('Contact', uselist=False)

    def __repr__(self):
        return "< table_name: %s Model_property: %s>" % (
            self.__tablename__, self.__dict__)


# 联系方式
class Contact(Base):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 真实姓名，估计没有
    m_name = Column(String(128), nullable=True)
    email = Column(String(255), nullable=True)
    msn = Column(String(255), nullable=True)
    phone = Column(String(16), nullable=True)
    phone_b = Column(String(16), nullable=True)
    wechat = Column(String(64), nullable=True)
    qq = Column(String(16), nullable=True)
    model_info_id = Column(Integer, ForeignKey('model_info.id'))

    def __repr__(self):
        return "< table_name: %s Model_property: %s>" % (
            self.__tablename__, self.__dict__)


# 爱好
class Hobby(Base):
    __tablename__ = 'hobby'
    id = Column(Integer, primary_key=True, autoincrement=True)
    music = Column(Text, nullable=True)
    star = Column(Text, nullable=True)
    movies = Column(Text, nullable=True)
    tv = Column(Text, nullable=True)
    sport = Column(Text, nullable=True)
    book = Column(Text, nullable=True)
    other = Column(Text, nullable=True)
    model_info_id = Column(Integer, ForeignKey('model_info.id'))

    def __repr__(self):
        return "< table_name: %s Model_property: %s>" % (
            self.__tablename__, self.__dict__)


class School(Base):
    __tablename__ = 'school'
    id = Column(Integer, primary_key=True, autoincrement=True)
    school_name = Column(String(128), nullable=True)
    # 毕业年份
    finish_school = Column(Date, nullable=True)
    # 学历
    education = Column(String(16), nullable=True)
    # 院系
    factions = Column(String(16), nullable=True)
    model_id = Column(Integer, ForeignKey('woman_models.id'))

    def __repr__(self):
        return "< table_name: %s Model_property: %s>" % (
            self.__tablename__, self.__dict__)
