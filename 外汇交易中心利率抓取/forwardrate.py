# __author__="suhu"
# -*- coding:utf-8 -*-]
import datetime
import requests
import pymysql
import time
import random
import json
#数据库配置***********************************
conn = pymysql.connect(host='10.10.128.116', user='root', password='111111', database='pdb', charset='utf8')
cursor=conn.cursor()

sql1="""insert into forwardrate values(UNIX_TIMESTAMP(CURRENT_TIMESTAMP)<<32 | RIGHT(UUID_SHORT(),8), UNIX_TIMESTAMP(CURRENT_TIMESTAMP)<<32 | RIGHT(UUID_SHORT(),8),%s,%s,%s,%s,0,0)"""
sql2="""update forwardrate set FP=%s,FU=%s WHERE FU=0 """%(datetime.datetime.now().strftime("%Y%m%d%H%I%S"),datetime.datetime.now().strftime("%Y%m%d%H%I%S"))

#url配置**************************************
url1="http://www.chinamoney.com.cn/dqs/rest/cm-u-pt/IfccFwrBmarkHistory?pageSize=&lang=cn&pageNum=1&startDate=%s&floatRefName=all"
url2="http://www.chinamoney.com.cn/dqs/rest/cm-u-pt/IfccFwrBmarkHistory?pageSize=%s&lang=cn&pageNum=1&startDate=%s&floatRefName=all"
headers={
	"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36",
	"Host": "www.chinamoney.com.cn"}

#begin---------------------------------------------
date_now=datetime.datetime.now()
date=date_now-datetime.timedelta(days=7)
count=0
while date<date_now:
	datestr=date.strftime("%Y-%m-%d")
	r=requests.get(url1%datestr,headers=headers)
	try:
		datacount=r.json().get("data").get("total")
	except json.decoder.JSONDecodeError:
		print("error here %s."%datestr)
		
		continue
	if(not datacount):
		print("execute %s,records=%s." % (datestr, datacount))
		date = date + datetime.timedelta(days=1)
		
		continue  #休息日
	
	rsp=requests.get(url2%(str(datacount),datestr),headers=headers)
	try:
		records=rsp.json().get("records")
	except json.decoder.JSONDecodeError :
		print("error here %s." % datestr)
		
		continue
	for item in records:
		calcdate = str(item.get("calcDate").replace("-", ''))
		floatrefname = str(item.get("floatrefName"))
		fradate = str(item.get("fraDate").replace("-", ''))
		frarate = str(item.get("fraRate"))
		try:
			cursor.execute(sql1,[floatrefname,calcdate,fradate,frarate])
		except pymysql.err.IntegrityError as err:
			continue
		count=count+1
	conn.commit()
	
	print("execute %s,records=%s."%(datestr,datacount))
	date = date + datetime.timedelta(days=1)
cursor.execute(sql2)
conn.commit()
conn.close()
s="forward increase %s records on %s\n"%(count,str(datetime.datetime.now()))
print(s)
with open("daliyrecords.txt",'a') as f:
	f.write("forward"+"***"*10+"\n")
	f.write(s)
	f.write("\n\n")