import datetime
import logging
import re
import time
from multiprocessing import Queue, Process
from multiprocessing.pool import Pool

import requests
from lxml import etree
from sqlalchemy import and_

from setting import db_session, HEADERS_DEFAULT, COOKIES, URL_DEFAULT
from .models import *


# 首页spider
def list_spider(url):
	new_resp = requests.get(url = URL_DEFAULT + url, headers = HEADERS_DEFAULT, cookies = COOKIES)
	new_html = etree.HTML(new_resp.text)
	"""
	1) Xpath模糊查找后用python处理
		/descendant::* 所有后代元素，等同于//*
	Elements = new_html.xpath('//*[@class="post small-post"]/descendant::*')
		| 管道符号，可以同时匹配前后两个条件，而且貌似是节点延伸匹配，可以用来自动排序
	elements_a_label = new_html.xpath(
			'//*[@class="post small-post"]//a|//*[@class="post small-post"]//img|//*[@class="post small-post"]//li//*')
		一步步分析需要的东西，减少匹配元素，提高效率，
		elements_a_label = new_html.xpath('//*[@class="post small-post"]//a|//*[@class="post small-post"]//li//*')
			==>Elements_a_img = new_html.xpath('//*[@class="post small-post"]//img')
				==>Elements_a_li = new_html.xpath('//*[@class="post small-post"]//li//*')
					==>获得包含全部元素的ElementList处理成pythonList，进一步过滤
	2) 直接用Xpath语法
		xpath_time = time.time()
		Elements_nickname = new_html.xpath('//*[@class="post small-post"]//a[@class="nickname"]')
		Elements_job = new_html.xpath(
				'//*[@class="post small-post"]//label[contains(text(),"职业")]/following::span[1]/text()')
		Elements_hits = new_html.xpath(
				'//*[@class="post small-post"]//label[contains(text(),"点击量")]/following::span[1]/text()')
		xpath_time = time.time() - xpath_time
	第二种方法，每多一条xpath语法，就比第一种慢一倍
	
	1) 实际情况发现不需要在首页获得点击量，但下面这种过于繁琐，不符合zen of python
		elements_a_label = new_html.xpath('//*[@class="post small-post"]//li//*')
		p = []
		element_list = []
		for i in range(len(elements_a_label)):
			if not i % 6 and elements_a_label[i + 1].attrib['title'] not in p:
				if db_session.query(WomanModels).filter(
						WomanModels.publisher == elements_a_label[i + 1].attrib['title']):
					p.append(elements_a_label[i + 1].attrib['title'])
					element_list.append(
							{
								y.text: elements_a_label[i + x + 1].text  if not elements_a_label[i + x +
								1].attrib else
								{
									'href': elements_a_label[i + x + 1].attrib['href'],
									'title': elements_a_label[i + x + 1].attrib['title']
								} for x, y in enumerate(elements_a_label[i:i + 4]) if not x % 2
							}
					)
		logging.debug(elements_a_label, element_list)
		# 进一步过滤掉男模
		elements_filter = [e for e in element_list if '男' not in e['发布人/']['title']]
	"""
	
	elements_nickname = new_html.xpath('//ul[@class="post small-post"]//a[@class="nickname"]')
	elements_job = new_html.xpath(
			'//ul[@class="post small-post"]//label[contains(text(),"职业")]/following::span[1]/text()')
	p = []
	model_list = []
	elements_nickname = [
		e for e in elements_nickname if '男' not in e.attrib['title']
		                                and '先生' not in e.attrib['title']
		                                and '绅士' not in e.attrib['title']
	]
	for i, e in enumerate(elements_nickname):
		if e.attrib['title'] not in p and not db_session.query(
				WomanModels).filter(WomanModels.publisher == e.attrib['title']).first():
			p.append(e.attrib['title'])
			model_list.append(
					{
						'publisher': e.attrib['title'],
						'href': e.attrib['href'],
						'job': elements_job[i]
					}
			)
	if model_list:
		model_list = [
			WomanModels(
					model_home = model['href'], publisher = model['publisher'],
					job = [Job(position = model['job'])]) for model in model_list
		]
		db_session.add_all(model_list)
		db_session.commit()
	next_url = new_html.xpath('//p[@class="page"]/a[@class="mBC wC"]/following::a[1]/@href')[0]
	print(next_url)
	if next_url.startswith('/'):
		return next_url
	else:
		return None


"""===model个人信息spider==="""


def model_post(url):
	print("===model个人信息spider===", '\n', url)
	# 直接拼的URL，其实应该模仿自然操作，先打开个人首页再进展示和个人信息，偷了个懒～
	url = URL_DEFAULT + '/profile' + url[:-1] + '.html'
	new_resp = requests.get(url = url, headers = HEADERS_DEFAULT, cookies = COOKIES)
	new_html = etree.HTML(new_resp.text)
	publisher = new_html.xpath('//a[@id="workNickName"]/text()')[0]
	w_model = db_session.query(WomanModels).filter_by(publisher = publisher).first()
	info_list = new_html.xpath('//div[@class="profile-module-box profile-line-module"]//*')
	job_list = new_html.xpath('//div[@class="profile-module-box"]//*')
	contact_list = new_html.xpath('//div[@class="only-firend"]//*')
	job_price_list = new_html.xpath('//div[@class="profile-module-box gC"]//li//*/text()')
	user_broker = UserBroker(woman_models = [w_model])
	job = Job(models = w_model)
	school = School(model_id = w_model.id)
	model_info = ModelInfo(model_id = w_model.id)
	hobby = Hobby()
	contact = Contact()
	# 防止对方把字段对应的值设成和字段一样
	try:
		if info_list:
			for i, e in enumerate(info_list[::2]):
				# 基础信息
				if e.text == '出生日期':
					birthday = [int(e) for e in re.split(r'-', info_list[2 * i + 1].text)]
					if len(birthday) == 2:
						model_info.birthday = datetime.date(1, birthday[0], birthday[1])
					elif len(birthday) == 3:
						model_info.birthday = datetime.date(birthday[0], birthday[1], birthday[2])
				elif e.text == '星座':
					model_info.constellation = info_list[2 * i + 1].text
				elif e.text == '血型':
					model_info.blood_group = info_list[2 * i + 1].text
				elif e.text == '身高(cm)':
					model_info.height = info_list[2 * i + 1].text
				elif e.text == '体重(kg)':
					model_info.weight = info_list[2 * i + 1].text
				elif e.text == '三围(cm)':
					model_info.shape = info_list[2 * i + 1].text
				elif e.text == '头发颜色':
					model_info.hair_color = info_list[2 * i + 1].text
				elif e.text == '眼睛颜色':
					model_info.eye_color = info_list[2 * i + 1].text
				elif e.text == '鞋码':
					model_info.shoe_size = info_list[2 * i + 1].text
				# 学校
				elif e.text == '大学':
					school.school_name = info_list[2 * i + 1].text
				elif e.text == '毕业年份':
					school.finish_school = datetime.date(int(info_list[2 * i + 1].text), 6, 6)
				elif e.text == '学历':
					school.education = info_list[2 * i + 1].text
				elif e.text == '院系':
					school.factions = info_list[2 * i + 1].text
				# 经纪公司
				elif e.text == '签约公司':
					user_broker.company = info_list[2 * i + 1].text
				elif e.text == '经纪人':
					user_broker.broker = info_list[2 * i + 1].text
				elif e.text == '手机':
					user_broker.broker_phone = info_list[2 * i + 1].text
				elif e.text == 'E-mail':
					user_broker.broker_email = info_list[2 * i + 1].text
				# 爱好
				elif e.text == '喜欢的音乐':
					hobby.music = info_list[2 * i + 1].text
				elif e.text == '喜欢的明星':
					hobby.star = info_list[2 * i + 1].text
				elif e.text == '喜欢的电影':
					hobby.movies = info_list[2 * i + 1].text
				elif e.text == '喜欢的电视':
					hobby.tv = info_list[2 * i + 1].text
				elif e.text == '喜欢的运动':
					hobby.sport = info_list[2 * i + 1].text
				elif e.text == '喜欢的书':
					hobby.book = info_list[2 * i + 1].text
				elif e.text == '其他':
					hobby.other = info_list[2 * i + 1].text
	except IndexError as info_error:
		print(URL_DEFAULT + url + ' info==>有陷阱', '\n', info_error)
	try:
		if job_list:
			for i, e in enumerate(job_list[::2]):
				if e.text == '所在公司':
					job.now_company = job_list[2 * i + 1].text
				elif e.text == '头衔':
					job.title = job_list[2 * i + 1].text
				elif e.text == '经历':
					job.experience = job_list[2 * i + 1].text
				# 作品
				elif e.text == '展览作品':
					job.show_works = job_list[2 * i + 1].text
				elif e.text == '其他作品':
					job.other_works = job_list[2 * i + 1].text
				# 奖项
				elif e.text == '最高奖项':
					job.top_trophies = job_list[2 * i + 1].text
				elif e.text == '其他奖项':
					job.trophies = job_list[2 * i + 1].text
	except IndexError as job_error:
		print(URL_DEFAULT + 'profile/lijiaji.html' + ' job==>有陷阱', '\n', job_error)
	try:
		# 因为没找到有联系方式的页面，不知道她页面上会怎么写，所以用的in
		if contact_list:
			for i, e in enumerate(contact_list[::2]):
				if '名字' in e.text:
					contact.m_name = contact_list[2 * i + 1].text
				elif 'mail' in e.text.lower():
					contact.email = contact_list[2 * i + 1].text
				elif '手机' in e.text:
					contact.phone = contact_list[2 * i + 1].text
				elif '电话' in e.text:
					contact.phone_b = contact_list[2 * i + 1].text
				elif '微信' in e.text:
					contact.wechat = contact_list[2 * i + 1].text
				elif 'QQ' in e.text.lower():
					contact.qq = contact_list[2 * i + 1].text
	except IndexError as contact_error:
		print(URL_DEFAULT + url + 'contact==>有陷阱', '\n', contact_error)
	try:
		job_price_list = [re.search(r"\d{3,6},\d{3,6},", e).group().split(',') if e.startswith('j') else e for e in
			job_price_list]
		job_price_list = [
			JobPrice(job_name = e, price_lower = job_price_list[2 * i + 1][0], price_up = job_price_list[2 * i + 1][1])
			for i, e in
			enumerate(job_price_list[::2])
		]
	except IndexError as price_error:
		print(URL_DEFAULT + url + ' job_price==>有陷阱', '\n', price_error)
	# 一切就绪，开始创建模型对象
	try:
		model_info.hobby = hobby
		model_info.contact = contact
		job.job_price = job_price_list
		db_session.bulk_save_objects([model_info, job, school])
		db_session.commit()
		print('======model_post end======')
	except Exception as error:
		db_session.rollback()
		print(error)


"""===model_show的spider==="""


def model_show_list(url_id):
	print("===model_show的spider===", '\n', url_id[0], url_id[1])
	url = URL_DEFAULT + '/post' + url_id[0] + 'new/1.html' if url_id[0].endswith('/') else URL_DEFAULT + url_id[0]
	new_resp = requests.get(url = url, headers = HEADERS_DEFAULT, cookies = COOKIES)
	new_html = etree.HTML(new_resp.text)
	show_list = new_html.xpath('//a[@class="coverBg wC"]/@href')
	next_url = new_html.xpath('//p[@class="page"]/a[@class="mBC wC"]/following::a[1]/@href')
	if next_url:
		print('======show_list nex url======', next_url)
		if next_url[0].startswith('/'):
			return next_url, (show_list, url_id[1])
		else:
			return None, (show_list, url_id[1])
	else:
		return None, (show_list, url_id[1])


"""===子相册的图片spider==="""


def photo_list(url_id):
	print("===子相册的图片spider===", '\n', url_id)
	url = URL_DEFAULT + url_id[0]
	new_resp = requests.get(url = url, headers = HEADERS_DEFAULT, cookies = COOKIES)
	new_html = etree.HTML(new_resp.text)
	photo_list = new_html.xpath('//p[@class="picBox"]//img/@src2')
	hits = int(new_html.xpath('//a[@class="sPoint gC"]/text()')[0][1:-1])
	create_time = new_html.xpath('//p[@class="date gC1"]/text()')[0]
	title = new_html.xpath('//h2[@class="text dBd_1"]/a/text()')[0]
	model_show_list = [
		ModelShow(href = photo_url, create_time = create_time, title = title, hits = hits, model_id = url_id[1])
		for photo_url in photo_list]
	try:
		db_session.bulk_save_objects(model_show_list)
		db_session.commit()
		print('======photo_list end======')
	except Exception as e:
		db_session.rollback()
		print(e)


"""===一切的开始==="""


def spider(url):
	"""
	4核cpu
	勉强把四个需求都实现了......
	先爬model首页pages获得所有的model个人页面的链接
	==> 等待有足够多的数据后，开始同时爬取信息页面和展示页面
		model_post==> 获取信息页面所需的信息，保存到对应的model的model_info表
		model_show_list==> 获取展示页面的所有子相册链接
			photo_list==> 获取每一个子相册内的图片链接
	"""
	profile_q = Queue()
	profile_p = Pool(processes = 1)
	show_q = Queue()
	show_p = Pool(processes = 1)
	photo_q = Queue()
	photo_p = Pool(processes = 2)
	try:
		# while 1:
		# 	url = list_spider(url)
		# 	if not url:
		# 		print('Finish')
		# 		break
		# 	time.sleep(2)
		# time.sleep(10)
		# 因为首页pages不多，就等它跑完再开其他spider，也就40second，而且也不用担心数据库冲突，偷懒:-)
		print('======首页爬完，开始model_info 和 show_list======')
		profile_new_id = 0
		show_new_id = 0
		while 1:
			model_post_url_list = []
			model_show_url_list = []
			if not profile_q.empty() or not show_q.empty():
				if not profile_q.empty():
					time.sleep(2)
					profile_p.apply(model_post, profile_q.get())
				
				if not show_q.empty():
					time.sleep(2)
					res = show_p.apply(model_show_list, args = (show_q.get(),))
					if res[0]:
						show_q.put(res[0])
					[photo_q.put((photo_url, res[1][1])) for photo_url in res[1][0]]
				if not photo_q.empty():
					time.sleep(2)
					photo_p.apply_async(func = photo_list, args = (photo_q.get(),))
			else:
				if profile_q.empty():
					model_post_url_list = db_session.query(WomanModels.model_home) \
						.filter(WomanModels.id.in_(range(profile_new_id, profile_new_id + 10)))
					model_post_url_list = list(model_post_url_list)
					if model_post_url_list:
						[profile_q.put(post_url) for post_url in model_post_url_list]
						profile_new_id += 10
					else:
						profile_q.close()
						profile_p.close()
						profile_p.terminate()
				if show_q.empty():
					# 有重复代码，但因为show页面可能有好几页，如果和profile用同一个Queue，
					# 当它把这几个页面爬完的时候，可能profile已经从Queue取走好几个URL，充满了不确定性
					model_show_url_list = db_session.query(WomanModels.model_home, WomanModels.id) \
						.filter(WomanModels.id.in_(range(show_new_id, show_new_id + 10)))
					model_show_url_list = list(model_show_url_list)
					if model_show_url_list:
						[show_q.put(show_url_and_id) for show_url_and_id in model_show_url_list]
						show_new_id += 10
					else:
						show_q.close()
						show_p.close()
						show_p.terminate()
				# 如果两个都拿不到URL了就等待子进程结束再退出循环
				if not model_post_url_list and not model_show_url_list:
					if photo_q.empty():
						photo_q.close()
						photo_p.close()
						photo_p.terminate()
						profile_p.join()
						show_p.join()
						photo_p.join()
						break
	except Exception as e:
		db_session.rollback()
		print(e)
