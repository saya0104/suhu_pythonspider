# -*- coding:utf8 -*-

'''
# =============================================================================
#      FileName: bank_data.py
#      Desc: 股驿台数据抓取
#      url: http://www.guyitai.net/
# =============================================================================
'''

from urllib import request
from urllib import parse
from bs4 import BeautifulSoup as bs
import http.cookiejar
import xlwt
import re
import time

# 数据准备
header = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'Host': 'www.guyitai.net',
	'Referer': 'http://www.guyitai.net/',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
}

data = {
	'email': '15527991208',
	'user_pwd': 'qweasdzxc11'
}
postdata = parse.urlencode(data).encode('utf-8')

# request添加cookies信息
cj = http.cookiejar.LWPCookieJar()
request.install_opener(request.build_opener(request.HTTPCookieProcessor(cj)))


# def func post,get
def get(url, header):
	req = request.Request(url, None, header)
	resp = request.urlopen(req)
	return resp.read().decode('utf-8')


def post(url, postdata, header):
	req = request.Request(url, postdata, header)
	resp = request.urlopen(req)
	return resp.read().decode('utf-8')


def getregex(s):
	r = re.compile(r'>(\d.*?.\d.*?)<')
	result = r.findall(s)
	return result[0]


# 准备工作
excel = xlwt.Workbook(encoding='utf-8')
sheet2016 = excel.add_sheet('2016', cell_overwrite_ok=True)
sheet2015 = excel.add_sheet('2015', cell_overwrite_ok=True)
name_list = ['银行名', '总股本(万股)', '营业利润(万元)', '营业收入(万元)', '存款（万元）', '贷款（万元）', '总资产（万元）', '利润总额（万元）', '负债总额(万元)']
for col in range(len(name_list)):
	sheet2015.write(0, col, name_list[col])
	sheet2016.write(0, col, name_list[col])

print('[抓取文件将存在d盘根目录]')
begin_page = int(input('请输入抓取起始页面:'))
end_page = int(input('请输入抓取终止页面:'))

# post登录页面，保持登录状态
url = 'http://www.guyitai.net/member/login.html'
post(url, postdata, header)

# get抓取页面信息

row = 1
bank_lost = []
for page in range(begin_page, end_page + 1):
	url = 'http://www.guyitai.net/stock/bankdata/p/%s.html' % page
	resp = get(url, header)
	num = 0

	# beautifulsoup提取表格中每家银行对应数据
	# 提取每家银行对应里层页面url
	soup = bs(resp, 'lxml')
	table = soup.find_all('table')
	if len(table) == 0:
		print('error:get page%s 出错 ' % page)
	elif len(table) > 1:
		print('此页面有多个银行数据表格')
	else:
		for label_a in table[0].find_all('a'):
			inner_url = 'http://www.guyitai.net' + label_a['href']

			url_2015 = inner_url.replace('.html', '/years/2015.html')  # 银行inner页面url
			url_2016 = inner_url.replace('.html', '/years/2016.html')
			num += 1

			try:
				# 爬取内部页面数据2015
				inner_data = []
				resp_2015 = get(url_2015, header)
				soup_2015 = bs(resp_2015, 'lxml')

				# 抓取银行名字
				name = soup_2015.find_all('h1')
				inner_data.append('2015' + name[0].string)
				print('页面%s,%s 正在抓取...' % (page, '[' + name[0].string + ']'))

				# 抓取指标数据
				ul = soup_2015.find_all('ul')[3]
				span = ul.find_all('span')
				for x in span:
					inner_data.append(x.string)
				li = ul.find_all('li')[8]
				fzze = getregex(li.prettify())
				inner_data.append(fzze)
				for col in range(len(inner_data)):
					sheet2015.write(row, col, inner_data[col])

				# 爬取内部页面数据2016
				inner_data = []
				resp_2016 = get(url_2016, header)
				soup_2016 = bs(resp_2016, 'lxml')

				# 抓取银行名字
				name = soup_2016.find_all('h1')
				inner_data.append('2016' + name[0].string + 'page%s' % page)

				# 抓取指标数据
				ul = soup_2016.find_all('ul')[3]
				span = ul.find_all('span')
				for x in span:
					inner_data.append(x.string)
				li = ul.find_all('li')[8]
				fzze = getregex(li.prettify())
				inner_data.append(fzze)
				for col in range(len(inner_data)):
					sheet2016.write(row, col, inner_data[col])
				row += 1
			except:
				bank_lost.append('error [页面%s,第%s家银行抓取失败]' % (page, num))

filename = '股驿台数据' + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '抓取.xlsx'
path = 'd:/' + filename
excel.save(path)
for x in bank_lost:
	print(x)




