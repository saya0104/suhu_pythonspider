# __author__="suhu"
# -*- coding:utf-8 -*-
import requests
import time
import json
import random
from bs4 import BeautifulSoup as bs
headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
url="http://i.gasgoo.com/supplier/"
resp=requests.get(url,headers=headers)
resp.encoding=resp.apparent_encoding
soup=bs(resp.text,'lxml')
div_zc=soup.find('div',attrs={'class':'proCat'})
"""#整车企业
zhengche_link=[]
for item in div_zc.find('ul').find_all('a'):
	l=['整车企业','none']
	l.append(item.text.replace('\n','').replace('\r','').replace(' ',''))
	l.append(item.attrs.get("href"))
	zhengche_link.append(l)"""

#零部件企业
lingandshe=[]  #第一层
for item in div_zc.find_all('dl'):
	l=['零部件企业']
	dt=item.find('dt').text
	l.append(dt)
	for x in item.find_all('a')[1:]:
		l1=l.copy()
		l1.append(x.text.replace('\n','').replace('\r','').replace(' ',''))
		l1.append(x.attrs['href'])
		lingandshe.append(l1)
#设备类企业
for item in div_zc.find_all('ul')[9].find_all('a'):
	l=['设备类企业','none']
	l.append(item.text.replace('\n', '').replace('\r', '').replace(' ', ''))
	l.append(item.attrs.get("href"))
	lingandshe.append(l)

for url_i in lingandshe:#等下取消
	page_count=1
	url=url_i[3].replace('.html','')+'/index-%s'+'.html'
	while True:
		url_inner=url%page_count
		resp_inner=requests.get(url_inner,headers=headers)
		resp_inner.encoding=resp_inner.apparent_encoding
		soup=bs(resp_inner.text,'lxml')
		l_inner=soup.find_all('dl',attrs={'class':'companyDl '}) #l_inner第二层
		time.sleep(random.randint(2,5)+random.random())
		if len(l_inner)==0:
			print("%s%s错误"%(x,url_inner))
		else:
			for x in l_inner:
				info = []
				url_ii=x.find('a').attrs['href']
				resp_ii=requests.get(url_ii,headers=headers)
				resp_ii.encoding=resp_ii.apparent_encoding
				soup_ii=bs(resp_ii.text,'lxml')
				company_name=soup_ii.find('h1').text
				info.append(company_name)
				ul=soup_ii.find_all('ul',attrs={'name':'mk'})
				for x in ul:
					li=x.find_all('li')
					for x in li:
						info.append(x.text.replace('\n','')+'~')
				info_ii=url_i+info
				with open('info.txt','a',encoding='utf-8') as f:
					f.write(str(info_ii)+'\n')
				print(info_ii)
				time.sleep(random.randint(5,10)+random.random())
		#检测是否为下一页
		flag_nextpage='下一页' in soup.find('div',attrs={'id':'rpSearchResultList'}).text
		if not flag_nextpage:
			break
