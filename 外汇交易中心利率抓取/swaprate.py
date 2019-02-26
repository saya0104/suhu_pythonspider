# __author__="suhu"
# -*- coding:utf-8 -*-
import datetime
import requests
import pymysql
import time
import random
from bs4 import BeautifulSoup
import re
a=re.compile(r".*=(.*)&")
#数据库配置***********************************
conn = pymysql.connect(host='10.10.128.116', user='root', password='111111', database='pdb', charset='utf8')
cursor=conn.cursor()

sql1="""insert into swaprate values(UNIX_TIMESTAMP(CURRENT_TIMESTAMP)<<32 | RIGHT(UUID_SHORT(),8), UNIX_TIMESTAMP(CURRENT_TIMESTAMP)<<32 | RIGHT(UUID_SHORT(),8),%s,%s,%s,%s,%s,0,0)"""
sql2="""update swaprate set FP=%s,FU=%s WHERE FU=0 """%(datetime.datetime.now().strftime("%Y%m%d%H%I%S"),datetime.datetime.now().strftime("%Y%m%d%H%I%S"))

#url配置**************************************
url_list=[
'http://www.chinamoney.com.cn/fe-c/interestRateSwapCurve3MHistoryAction.do?bigthType=Shibor3M&lan=cn',
'http://www.chinamoney.com.cn/fe-c/interestRateSwapCurve3MHistoryAction.do?bigthType=FR007&lan=cn',
'http://www.chinamoney.com.cn/fe-c/interestRateSwapCurve3MHistoryAction.do?bigthType=FDR007&lan=cn',
'http://www.chinamoney.com.cn/fe-c/interestRateSwapCurve3MHistoryAction.do?bigthType=ShiborON&lan=cn',
'http://www.chinamoney.com.cn/fe-c/interestRateSwapCurve3MHistoryAction.do?bigthType=Shibor1W&lan=cn',
'http://www.chinamoney.com.cn/fe-c/interestRateSwapCurve3MHistoryAction.do?bigthType=Deposit1Y&lan=cn'
]
headers={
	"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36",
	"Host": "www.chinamoney.com.cn"}

#---begin---------------------------------------------
name_dict=d={'Shibor3M':['6M','9M','1Y','2Y','3Y','4Y','5Y','7Y','10Y'],
'FR007':['1M','3M','6M','9M','1Y','2Y','3Y','4Y','5Y','7Y','10Y'],
'FDR007':['1M','3M','6M','9M','1Y','2Y','3Y','4Y','5Y','7Y','10Y'],
'ShiborON':['1M','3M','6M','9M','1Y','2Y','3Y',],
'Shibor1W':['1M','3M','6M','9M','1Y',],
'Deposit1Y':['2Y','3Y','4Y','5Y','7Y','10Y']}
count=0
for url in url_list:
	resp=requests.get(url,headers=headers)
	resp.encoding=resp.apparent_encoding
	soup=BeautifulSoup(resp.text,'lxml')
	table=soup.find_all("table")[5]

	for tr in table.find_all("tr")[1:]:

		record=[]
		date=str(tr.find_all("td")[0].text).replace('-','')
		name=str(tr.find_all("td")[1].text)
		type=str(tr.find_all("td")[2].text).replace('）','').replace('（','')
		i=0
		print("execute %s"%(str([date,name,type])))
		flag=a.findall(url)[0]
		qixian=name_dict.get(flag)
		for item in tr.find_all("td")[3:]:
			record=[date,name,type]
			record.append(qixian[i])
			record.append(item.text)

			i=i+1;
			try:
				cursor.execute(sql1,record)
			except pymysql.err.IntegrityError as err:
				continue
			count=count+1
	conn.commit()
cursor.execute(sql2)
conn.commit()
s="swap increase %s records on %s"%(count,datetime.datetime.now())
print(s)
with open("daliyrecords.txt",'a') as f:
	f.write("swap"+"***"*10+"\n")
	f.write(s)
	f.write("\n\n")