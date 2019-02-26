"""
休市日抓取
主网站：http://www.cnyes.com/economy/indicator/GlobalRest/GlobalRest_Major.aspx
共77种市场，58种抓取到，19种内容为空
"""

import requests
from bs4 import BeautifulSoup as bs
import xlwt

headers={
'Connection':'keep-alive',
'Host':'www.cnyes.com',
'Referer':'http://www.cnyes.com/economy/indicator/GlobalRest/GlobalRest_Major.aspx',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
}
url='http://www.cnyes.com/economy/indicator/GlobalRest/GlobalRest_Major.aspx'
excel=xlwt.Workbook(encoding='utf-8')
sheet1=excel.add_sheet(sheetname='s1',cell_overwrite_ok=True)
row_num=0
empty=[]

r1=requests.get(url,headers=headers)
r1.encoding=r1.apparent_encoding
#print(r1.text)
soup_first=bs(r1.text,'lxml')
table=soup_first.find_all('table')[1]
url_list=table.find_all('a')
url_total=[]
for x in url_list:
	url_total.append([x.string,'http://www.cnyes.com/economy/indicator' + x['href'].replace('..','')])

##url_total总url列表
for url_single in url_total:
	r2=requests.get(url_single[1],headers=headers)
	r2.encoding=r2.apparent_encoding
	soup_second=bs(r2.text,'lxml')
	market_type=url_single[0]
	table=soup_second.find_all('table')[2]
	tr_list=table.find_all('tr')
	if len(tr_list)==1:
		empty.append(market_type)
	else:
		for x in tr_list[1:]:
			value_list=[]
			td=x.find_all('td')
			value_list.append(market_type)
			value_list.append(td[0].string)
			value_list.append(td[1].string)
			for col in range(len(value_list)):
				sheet1.write(row_num,col,value_list[col])
			row_num+=1
	print('正在抓取：%s...'%market_type)
excel.save(r'd:\休市日.xls')

print('有%s个市场内容为空:%s'%(len(empty),empty))