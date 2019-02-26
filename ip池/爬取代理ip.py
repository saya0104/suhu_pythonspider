import requests
from bs4 import BeautifulSoup as bs

headers={
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
'Connection':'keep-alive'
}

###返回html页面
def gethtml(url):
	r=requests.session().get(url,headers=headers)
	r.encoding=r.apparent_encoding
	return r.text

file=open(r'C:\Users\suhu\Desktop\code\python_spider\ip\ip.txt','w')

for i in range(1,10):
	url='http://www.xicidaili.com/nn/'+str(i)
	html=gethtml(url)

	soup=bs(html,'lxml')
	table=soup.find_all('table',attrs={'id':"ip_list"})[0]
	tr_list=table.find_all('tr')[1:]
	for tr in tr_list:
		td=tr.find_all('td')
		ip=td[1].text
		port=td[2].text
		httptype=td[5].text
		file.write(ip+'\t'+port+'\t'+httptype+'\n')
		print('正在抓取%s...'%(ip+'\t'+port+'\t'+httptype+'\n'))
file.close()






