# __author__="suhu"
# -*- coding:utf-8 -*-

#思路、通过同一个标签的不同属性区分在文章中的作用和位置
from bs4 import BeautifulSoup as bs
import re
import pymysql
conn = pymysql.connect(host='10.10.128.116', user='root', password='111111', database='pdb', charset='utf8')
cursor=conn.cursor()


def jiangchao8848(html):
	soup = bs(html, 'lxml')
	div = soup.find('div', attrs={'id': 'js_content'})
	tag = 'strong'
	strong = div.find_all(tag)
	str1 = ''  # 初始化记录特殊的数字字母字样
	result=''
	for item in strong:
		if len(item.find_all(tag)) == 0:  # 去除同一tag里面包tag情况
			count = len(item.text)
			if count <= 5:
				str1 = item.text
			else:
				str = str1 + item.text
				str1 = ''
				result+=str+'\n'
	return result
def qqzqlt(html):
	regex1=re.compile(r'[【\[]\d\d:\d\d[】\]]')
	regex2= re.compile(r'([(（][一二三四][)）])(上午|下午|隔夜市场|市场小结):?')
	soup=bs(html,'lxml')
	div=soup.find('div',attrs={'id':'js_content'})
	str=''
	for item in div.find_all('strong'):
		txt=item.text
		if len(regex1.findall(txt)) ==0 and  len(regex2.findall(txt))==0 and len(txt)!=0:
			str+=txt+'\n'
	return str
def GXZQ_BOND(html):
	regex_gxgs = re.compile(r'(我们)?(更?倾向于|建议|认为|估计|继续?推荐|意图很?明显|预计)')
	soup=bs(html,'lxml')
	div = soup.find('div', attrs={'id': 'js_content'})
	str=div.text
	s=''
	for x in [x for x in re.split(r'[；;。]', str) if len(x) != 0]:
		if len(regex_gxgs.findall(x))!=0:
			    s+=x+'\n'
	return s
def ficcquakeqin(html):
	soup=bs(html,'lxml')
	str=''
	div = soup.find('div', attrs={'id': 'js_content'})
	for item in soup.find_all('span',attrs={'style':"font-size: 15px;font-family: 楷体_GB2312;color: rgb(10, 0, 138);"}):
		s=item.text.replace('【','').replace('】','')
		str+=s+'\n'
	return str

def select(publicname):
	cursor.execute("""select f5,f6,f7 from wechat_info 
			where f2 =  %s and f5 like "%%国君固收 | 每日市场回顾%%" 	
		""",publicname)
	result=cursor.fetchall()
	with open('info.txt', 'a', encoding='utf-8') as f:
		for x in result:
			d = {}
			d['title'] = x[0]
			d['url'] = x[1]
			d['content'] = eval(publicname)(x[2])
			if d['content']==None:
				d['content']='none'
			f.write('title----'+d['title']+'\n')
			f.write('url----'+d['url']+'\n')
			f.write('content----'+d['content']+'\n')
			f.write('---------------------------------------------------------\n\n\n\n\n')


select('ficcquakeqin')
#jiangchao8848(html)