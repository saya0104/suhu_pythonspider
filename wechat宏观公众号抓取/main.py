# __author__="suhu"
# -*- coding:utf-8 -*-

from selenium import webdriver
import json
import requests
import random
import time
import re
import pymysql
from bs4 import BeautifulSoup as bs
import jieba
import pandas as pd
import os

def wechatLogin():
	post = {}
	with open("account.txt",'r') as f:
		account_list=list(json.load(f).values())
	for account in account_list:
		print("本次用于生成cookies和token的是:%s"%account)
	try:
		for account in account_list:
			user = account[0]
			password = account[1]
			post[user] = {}
			post[user]['cookies'] = {}
			driver = webdriver.Chrome(os.path.join(os.getcwd(),"chromedriver.exe"))
			driver.get("https://mp.weixin.qq.com/")
			time.sleep(3)
			print("模拟登陆开始...")
			print("准备扫描二维码...")
			time.sleep(random.randint(1, 3) + random.random())
			driver.find_element_by_name("account").clear()
			driver.find_element_by_name("account").send_keys(user)
			time.sleep(random.random())
			driver.find_element_by_name("password").clear()
			driver.find_element_by_name("password").send_keys(password)
			time.sleep(random.random())

			driver.find_element_by_class_name("btn_login").click()
			time.sleep(random.randint(8, 12) + random.random())
			driver.get("https://mp.weixin.qq.com/")
			time.sleep(5)
			url = str(driver.current_url)
			cookies = driver.get_cookies()
			token = re.findall(r'token=(\d+)', url)[0]
			for item in cookies:
				post[user]['cookies'][item["name"]] = item["value"]
			post[user]['token'] = token
			print("%s登陆成功..."%user)
			time.sleep(random.randint(10,20)+random.random())
	except:
		print("使用%s登录时发生错误..."%account)
	finally:
		with open('cookies.txt','w') as f:
			f.write(json.dumps(post))
	print("cookies及token已保存...")
def div2tags(div_input):
	with open(r'userdict1.txt', 'r', encoding='utf-8') as d_file:
		d_file_list = d_file.readlines()
	jieba.load_userdict(r'userdict1.txt')
	div_str_list = []
	div_cont = bs(div_input, 'lxml')
	div_p_cont = div_cont.find_all('p')
	d = {}
	for p in div_p_cont:
		if ''.join(p.strings).strip().upper() != '':
			div_str_list.append(''.join(p.strings).strip().upper().replace(' ', ''))
			p_words_list = jieba.cut(''.join(p.strings).strip().upper().replace(' ', ''))
			for word in p_words_list:
				if word in d.keys() and word in [w.replace('\n', '') for w in d_file_list]:
					d[word] += 1
				elif word not in d.keys() and word in [w.replace('\n', '') for w in d_file_list]:
					d[word] = 1
				else:
					continue
	df = pd.DataFrame({'name': list(d.keys()), 'count': list(d.values())})
	tags = ','.join(df.sort_values(by='count', ascending='False')[0:5]['name'])
	return tags
def getUrl():
#-----------------------preaper-------------------------------------------------
	#获取待抓取公众号list
	with open("公众号list.txt",'r',encoding='utf-8') as f:
		public_list = list(json.load(f).values())

	#获取cookies/cookies_num用取模的方式控制每次用不同的cookies
	with open("cookies.txt",'r',encoding='utf-8') as f:
		cookies_list=list(json.load(f).values())
		cookies_num=0

	#链接数据库pdb:wechat_info
	conn = pymysql.connect(host='10.10.128.116', user='root', password='111111', database='pdb', charset='utf8')
	cursor=conn.cursor()

	headers = {
		'Host': 'mp.weixin.qq.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
	appmsg_url="https://mp.weixin.qq.com/cgi-bin/appmsg?"
	requests.packages.urllib3.disable_warnings()
#----------------------begin----------------------------------------------------
	#遍历public_list
	errorlist=[]
	count_public=0
	count_insert_essay=0
	start_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
	f=open("record.txt",'a',encoding='utf-8')
	f.write(start_time+"\n")
	for public_item in public_list:
		count_public+=1
		count_essay=0 #记录每次抓取中新增文章新增数量
		cookies_num = (cookies_num + 1) % 2 #控制cookieslist循环
		fakeid=public_item.get('fakeid')
		public_name=public_item.get("nickname")
		public_id=public_item.get("alias")
		appmsg_id = {
			'token': cookies_list[cookies_num].get('token'),
			'lang': 'zh_CN',
			'f': 'json',
			'ajax': '1',
			'random': random.random(),
			'action': 'list_ex',
			'begin': 0,
			'count': '5',
			'query': '',
			'fakeid': '%s=='%fakeid,
			'type': '9'}
		cookies=cookies_list[cookies_num].get('cookies')

		# 得到一个按确定公众号按时间排倒序的aid列表/用于检测插入数据是否重复
		sql="select F3 from wechat_info where F1='{0}' order by F4 desc limit 50".format(public_name)
		cursor.execute(sql)
		exist_list=[]
		for aid in cursor.fetchall():
			exist_list.append(aid[0])


		#遍历appmsglist
		try:
			resp_appmsg=requests.get(appmsg_url,headers=headers,cookies=cookies,params=appmsg_id,verify=False)
			time.sleep(random.randint(3,6)+random.random())
			list_account=len(resp_appmsg.json().get("app_msg_list"))
			for message_item in resp_appmsg.json().get("app_msg_list"):
				message_info=[public_name,public_id]
				aid=message_item.get("aid")
				if aid not in exist_list:
					message_info.append(aid)
					message_info.append(time.strftime('%Y%m%d%H%M%S', time.localtime(message_item.get("update_time"))))
					message_info.append(message_item.get("title").replace('\"',"“"))
					link=message_item.get("link")
					message_info.append(link)
					resp_url=requests.get(link,headers=headers)
					resp_url.encoding=resp_url.apparent_encoding
					div=str(bs(resp_url.text,'lxml').find('div',attrs={'id':'js_content'})).strip().replace('data-src', 'src')
					message_info.append(div)
					lable=div2tags(div)
					message_info.append(lable)
					sql="""insert into wechat_info values(UNIX_TIMESTAMP(CURRENT_TIMESTAMP)<<32 | RIGHT(UUID_SHORT(),8), UNIX_TIMESTAMP(CURRENT_TIMESTAMP)<<32 | RIGHT(UUID_SHORT(),8),
        	           %s,%s,%s,%s,%s,%s,%s,%s,0,0)"""
					cursor.execute(sql,message_info)
					count_insert_essay+=1
					count_essay+=1
		except Exception as e:
			print(e)
			if message_info[0] not in errorlist:
				errorlist.append(message_info[0])
				continue
		queto1="程序已经爬取至[第%s个],\"%s\",此次该公众号共有[%s]条消息,本次程序运行新增[%s]个..."%(count_public,public_name,list_account,count_essay)
		if len(errorlist)!=0:
			print(errorlist)
		print(queto1)
		f.write(queto1+"\n")
		conn.commit()


	cursor.execute("""update wechat_info set FP=DATE_FORMAT(SYSDATE(),'%Y%m%d%H%I%S'),FU=DATE_FORMAT(SYSDATE(),'%Y%m%d%H%I%S') WHERE FU=0 """)
	conn.commit()
	queto2="数据库内本次共新增%s条记录\n"%count_insert_essay
	print(queto2)
	f.write(queto2)
	conn.close()
	if len(errorlist)==0:
		print("本次运行爬取没有错误项...")
	else:
		queto3="本次运行错误项为%s"%str(errorlist)
		print(queto3)
		f.write(queto3 + "\n")
	f.write("-----------------------------------")
	f.close()


test=input("是否需要新生成cookies？")
if test=="Y":
	wechatLogin()
	getUrl()
else:
	getUrl()

