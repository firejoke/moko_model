# main
import logging
import os
import sys

from importlib import import_module

from setting import migrate, URL_DEFAULT, COOKIES

if __name__ == '__main__':
    # [print(dir_name) for dir_name in os.listdir('./')]
    """
    Terminal
            $ python3 moko_spider.py model_name
    """
    try:
        # sys.argv[1].title()
        model_name = sys.argv[1].title()
        COOKIES["LAST_LOGIN_EMAIL"] = sys.argv[2]
        # 模型表映射
        migrate(model_name)
        model_path = os.path.join(
            os.path.dirname(__file__), model_name, 'config')
        with open(model_path, 'r') as md:
            index_url = md.read()
        print(URL_DEFAULT + index_url)
        # 动态导入对应模块的spider
        module = import_module(model_name + "." + "spider")
        module.spider(index_url)
    # logging.debug(db_session)
    except Exception as e:
        print(e, '\n', '没有该模块')
