# moko_model
一个并行式小爬虫\
sql:\
    SQLAlchemy\
request:\
    requests\
并行式:\
    multiprocessing.pool Pool\
\
写着写着就变成了一个小框架......\
###7/10\
    又写了一天报错......
\
###7/12\
    终端里跑到\
    *
    ===model_show的spider===\
    /320771e8341a4efb97bf7f2e84b56d7a/ 352\
    ===子相册的图片spider===\
    ('/post/1302816.html', 51)\
    ======photo_list end======\
    ===子相册的图片spider===\
    ('/post/1302813.html', 51)\
    ======photo_list end======\
    2018-07-12 15:03:26,858 INFO sqlalchemy.engine.base.Engine \
        SELECT woman_models.model_home AS woman_models_model_home FROM woman_models\
        WHERE woman_models.id IN (%(id_1)s, %(id_2)s, %(id_3)s, %(id_4)s, %(id_5)s, %(id_6)s, %(id_7)s, %(id_8)s, \
            %(id_9)s, %(id_10)s)\
    2018-07-12 15:03:26,858 INFO sqlalchemy.engine.base.Engine \
        {'id_1': 360, 'id_2': 361, 'id_3': 362, 'id_4': 363, 'id_5': 364, 'id_6': 365, 'id_7': 366, 'id_8': 367, \
            'id_9': 368, 'id_10': 369}\
    2018-07-12 15:03:26,944 INFO sqlalchemy.engine.base.Engine \
        SELECT woman_models.model_home AS woman_models_model_home, woman_models.id AS woman_models_id\
        FROM woman_models\
        WHERE woman_models.id IN (%(id_1)s, %(id_2)s, %(id_3)s, %(id_4)s, %(id_5)s, %(id_6)s, %(id_7)s, %(id_8)s, \
            %(id_9)s, %(id_10)s)\
    2018-07-12 15:03:26,944 INFO sqlalchemy.engine.base.Engine \
        {'id_1': 360, 'id_2': 361, 'id_3': 362, 'id_4': 363, 'id_5': 364, 'id_6': 365, 'id_7': 366, 'id_8': 367, \
            'id_9': 368, 'id_10': 369}\
    2018-07-12 15:03:27,014 INFO sqlalchemy.engine.base.Engine ROLLBACK\
    handle is closed\
    *
\
    352是woman_models table最后一个id\
    应该是跟关闭进程池有关\
    spider逻辑已经证明没问题了\
    检查了一下数据库，还是有脏数据，给info spider的保存流程加几个状态码判断\
    \
    \
    原本是想把所有的photo URL都跑出来后，在主进程里统一写到数据库，\
    但发现这样要是有一个数据出了非数据保存问题，之前的所有数据就都没了......\
    就改成中途保存一部分算了，但还是放在主进程，还是把spider和sql分开为好 \
    把列表处理改成queue，可以不用考虑存和取的冲突 \
    原：\
    '
    model_photo_list = \
            [\
                [\
					ModelShow(href = model_photo['href'], create_time = model_photo['create_time'],\
							title = model_photo['title'], hits = model_photo['hits'],\
							model_id = model_photo['model_id'])\
					for model_photo in model_photo_generator\
				] for model_photo_generator in model_photo_list\
			]\
	'\
###7/13\
    一晚上起来，发现有的页面被删除了，在信息匹配那里引发了IndexError 加一个判断避雷\
    \
    \
    把之前用的multiprocessing.Queue 改成了multiprocessing.Manager().Queue()\
    但没想到，这个Manager().Queue()没有close方法\
    报了一个这个错误：\
    'AutoProxy[Queue]' object has no attribute 'close'\
##数据都拿到了，这个项目暂时告一段落，去攻克别的pro