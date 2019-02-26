# __author__="suhu"
# -*- coding:utf-8 -*-

import requests
import re
import pymysql
import xlwt
import os

#-----------preaper----------------------------------------------
headers={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Host':'www.chinabond.com.cn',
'Referer':'http://www.chinabond.com.cn/jsp/include/EJB/queryResult.jsp?pageNumber=26&queryType=1&sType=0&zqdm=&zqjc=&zqxz=00&eYear2=&bigPageNumber=2&bigPageLines=500&zqdmOrder=1&fxrqOrder=1&hkrOrder=1&qxrOrder=1&dqrOrder=1&ssltrOrder=1&zqqxOrder=1&fxfsOrder=1&xOrder=12345678&qxStart=0&qxEnd=0&sWhere=1&wsYear=&weYear=&eWhere=1&sEnd=0&fxksr=1998-01-01&fxjsr=2017-10-12&fxStart=1998-01-01&fxEnd=2108-12-31&dfStart=1998-01-01&dfEnd=2108-10-12&start=0&zqfxr=00&fuxfs=32&faxfs=00&zqxs=00&bzbh=01&sYear=1998&sMonth=01&sDay=01&eYear=2017&eMonth=10&eDay=12&fxStartYear=1998&fxStartMonth=01&fxStartDay=01&fxEndYear=2108&fxEndMonth=12&fxEndDay=31&dfStartYear=1998&dfStartMonth=01&dfStartDay=01&dfEndYear=2108&dfEndMonth=10&dfEndDay=12&col=27',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
regex=re.compile(r"""tArray\[\d{1,3}\]\s{,2}=\s{,2}new Array\(\);\s*tArray\[\d{1,3}\]\[0\]\s{,2}=\s{,2}\'(.{1,50}?)\';\s*tArray\[\d{1,3}\]\[1\]\s{,2}=\s{,2}\'(\d{1,30}?)\';.*?tArray\[\d{1,3}\]\[27\]\s{,2}=\s{,2}\'(\S{1,50}?)\'""",re.DOTALL)
excel=xlwt.Workbook(encoding='utf-8')
sheet=excel.add_sheet('sheet1',cell_overwrite_ok=True)
excel_titel=['名字','f015_ths001','f001_ths001','f016_ths001','浮动利率基准']
for col in range(len(excel_titel)):
	sheet.write(0,col,excel_titel[col])
rownum=0
excel_path=os.path.join(os.getcwd(),'中债登数据.xls')
config={
	'host':'10.11.2.138',
	'user':'sunhf',
	'password':'sunhf@345',
	'database':'pljr',
	'use_unicode':True,
	'charset':'utf8'
}
cursor=pymysql.connect(**config).cursor()

#-----------begin------------------------------------------------
url=['http://www.chinabond.com.cn/jsp/include/EJB/queryResult.jsp?pageNumber=6&queryType=1&sType=0&zqdm=&zqjc=&zqxz=00&eYear2=&bigPageNumber=1&bigPageLines=500&zqdmOrder=1&fxrqOrder=1&hkrOrder=1&qxrOrder=1&dqrOrder=1&ssltrOrder=1&zqqxOrder=1&fxfsOrder=1&xOrder=12345678&qxStart=0&qxEnd=0&sWhere=1&wsYear=&weYear=&eWhere=1&sEnd=0&fxksr=1998-01-01&fxjsr=2017-10-12&fxStart=1998-01-01&fxEnd=2108-12-31&dfStart=1998-01-01&dfEnd=2108-10-12&start=0&zqfxr=00&fuxfs=32&faxfs=00&zqxs=00&bzbh=01&sYear=1998&sMonth=01&sDay=01&eYear=2017&eMonth=10&eDay=12&fxStartYear=1998&fxStartMonth=01&fxStartDay=01&fxEndYear=2108&fxEndMonth=12&fxEndDay=31&dfStartYear=1998&dfStartMonth=01&dfStartDay=01&dfEndYear=2108&dfEndMonth=10&dfEndDay=12&col=27',
	'http://www.chinabond.com.cn/jsp/include/EJB/queryResult.jsp?pageNumber=51&queryType=1&sType=0&zqdm=&zqjc=&zqxz=00&eYear2=&bigPageNumber=3&bigPageLines=500&zqdmOrder=1&fxrqOrder=1&hkrOrder=1&qxrOrder=1&dqrOrder=1&ssltrOrder=1&zqqxOrder=1&fxfsOrder=1&xOrder=12345678&qxStart=0&qxEnd=0&sWhere=1&wsYear=&weYear=&eWhere=1&sEnd=0&fxksr=1998-01-01&fxjsr=2017-10-12&fxStart=1998-01-01&fxEnd=2108-12-31&dfStart=1998-01-01&dfEnd=2108-10-12&start=0&zqfxr=00&fuxfs=32&faxfs=00&zqxs=00&bzbh=01&sYear=1998&sMonth=01&sDay=01&eYear=2017&eMonth=10&eDay=12&fxStartYear=1998&fxStartMonth=01&fxStartDay=01&fxEndYear=2108&fxEndMonth=12&fxEndDay=31&dfStartYear=1998&dfStartMonth=01&dfStartDay=01&dfEndYear=2108&dfEndMonth=10&dfEndDay=12&col=27',
	'http://www.chinabond.com.cn/jsp/include/EJB/queryResult.jsp?pageNumber=26&queryType=1&sType=0&zqdm=&zqjc=&zqxz=00&eYear2=&bigPageNumber=2&bigPageLines=500&zqdmOrder=1&fxrqOrder=1&hkrOrder=1&qxrOrder=1&dqrOrder=1&ssltrOrder=1&zqqxOrder=1&fxfsOrder=1&xOrder=12345678&qxStart=0&qxEnd=0&sWhere=1&wsYear=&weYear=&eWhere=1&sEnd=0&fxksr=1998-01-01&fxjsr=2017-10-12&fxStart=1998-01-01&fxEnd=2108-12-31&dfStart=1998-01-01&dfEnd=2108-10-12&start=0&zqfxr=00&fuxfs=32&faxfs=00&zqxs=00&bzbh=01&sYear=1998&sMonth=01&sDay=01&eYear=2017&eMonth=10&eDay=12&fxStartYear=1998&fxStartMonth=01&fxStartDay=01&fxEndYear=2108&fxEndMonth=12&fxEndDay=31&dfStartYear=1998&dfStartMonth=01&dfStartDay=01&dfEndYear=2108&dfEndMonth=10&dfEndDay=12&col=27']
bond_error=[]
for url in url:
	r=requests.get(url,headers=headers)
	r.encoding=r.apparent_encoding
	infor_list=regex.findall(r.text)
	for item in infor_list:
		bond=[]
		bond.append(item[0].replace('（','(').replace('）',')').replace(' ','').replace('０','0').replace('１','1').replace('２','2').replace('３','3').replace('４','4').replace('５','5').replace('６','6').replace('７','7').replace('８','8').replace('９','9'))
		bond.append(item[1]+'.IB')
		cursor.execute("""select f001_ths001,f016_ths001 from  ths001 where f015_ths001='%s'"""%(item[1]+'.IB'))
		result=cursor.fetchall()
		if len(result)!=0:
			bond.append(result[0][0])
			bond.append(result[0][1])
			bond.append(item[2].replace('（','(').replace('）',')').replace(' ',''))
			print(bond)
			rownum += 1
			for col in range(len(bond)):
				sheet.write(rownum,col,bond[col])
		else:
			bond_error.append(item)
print(bond_error)
excel.save(excel_path)


