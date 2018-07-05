import logging

from apis import OrmSql
from models import WomanModels, ModelInfo
from setting import engine, Base, db_session

# 实例化的时候就会把表写进数据库

model_sql = OrmSql(engine = engine, base = Base, session = db_session, models = WomanModels)
# model_info_sql = OrmSql(engine = engine, base = Base, session = db_session, models = ModelInfo)

print(vars(model_sql.models).items())
