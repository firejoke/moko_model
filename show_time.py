import logging

from setting import migrate

# 实例化的时候就会把表写进数据库


logging.debug(migrate('Model'))
