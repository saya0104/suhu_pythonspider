# __author__="suhu"
# -*- coding:utf-8 -*-
import requests
import pymysql
import datetime
conn = pymysql.connect(host='10.10.128.116', user='root', password='111111', database='pdb', charset='utf8')
cursor=conn.cursor()
date_end=datetime.datetime.now()
date_start=date_end-datetime.timedelta(days=15)
url="http://www.chinamoney.com.cn/dqs/rest/dqs-u-currency/FrrHis?lang=cn&startDate=%s&endDate=%s"%(date_start.strftime("%Y-%m-%d"),date_end.strftime("%Y-%m-%d"))
headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36",
"Host": "www.chinamoney.com.cn"}
requ=requests.get(url,headers=headers)
data=requ.json()
record=data.get('records')
count=0
for x in record:
	date=x.get("lfiProducDate").replace('-','')
	map=x.get("frValueMap")
	for y in map:
		type=str(y)
		rate=str(map.get(y))
		sql="""insert into reporate values(UNIX_TIMESTAMP(CURRENT_TIMESTAMP)<<32 | RIGHT(UUID_SHORT(),8), UNIX_TIMESTAMP(CURRENT_TIMESTAMP)<<32 | RIGHT(UUID_SHORT(),8),
        	           %s,%s,%s,0,0)"""
		try:
			cursor.execute(sql,[type,date,rate])
		except pymysql.err.IntegrityError as err:
			continue
		count=count+1
	conn.commit()
cursor.execute(
		"""update reporate set FP=%s,FU=%s WHERE FU=0 """%(datetime.datetime.now().strftime("%Y%m%d%H%I%S"),datetime.datetime.now().strftime("%Y%m%d%H%I%S")))
conn.commit()
conn.close()
s="reporate increase %s records on %s\n"%(count,str(datetime.datetime.now()))
print(s)
with open("daliyrecords.txt",'a') as f:
	f.write("repodate"+"***"*10+"\n")
	f.write(s)
	f.write("\n\n")