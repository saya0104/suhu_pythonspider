# -!- coding: utf-8 -!-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import datetime
import xlwt
import time
import random

###准备工作
excel = xlwt.Workbook(encoding='utf-8')
sheet1 = excel.add_sheet('财经日历', cell_overwrite_ok=True)
sheet2 = excel.add_sheet('财经事件', cell_overwrite_ok=True)
sheet3 = excel.add_sheet('央行动态', cell_overwrite_ok=True)
cjrl_row=0
cjsj_row=0
yhdt_row=0
sheet1_title=['时间','重要性','国家','指标内容','前值','前值(修正前)','预测值','公布值']
sheet3_title=['时间','重要性','国家地区','事件']
for x in range(len(sheet1_title)):
	sheet1.write(cjrl_row,x,sheet1_title[x])
for x in range(len(sheet3_title)):
	sheet3.write(yhdt_row,x,sheet3_title[x])
	sheet2.write(yhdt_row,x,sheet3_title[x])



###日期列表函数
def datelist(start, end):
    start_date = datetime.date(*start)
    end_date = datetime.date(*end)

    result = []
    curr_date = start_date
    while curr_date != end_date:
        result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
        curr_date += datetime.timedelta(1)
    result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
    return result
term=datelist((2015,9,7),(2017,9,17))


##模拟浏览器
driver=webdriver.Chrome(r'E:\chrome\chromedriver.exe')
driver.get('http://datainfo.fx168.com/calendar.shtml')
assert '财经日历-FX168外汇数据' in driver.title

for rq in ['2015-11-06']:
	dt_elem=driver.find_element_by_id('datetime')
	dt_elem.clear()
	dt_elem.send_keys('%s'%rq)
	dt_elem.send_keys(Keys.RETURN)
	#hb_elem=driver.find_element_by_id('guojia_9')
	#hb_elem.click()
	html=driver.page_source
	soup = bs(html, 'lxml')
	print(html)

	###整个源代码事件tag
	main_div = soup.find_all('div', attrs={'id': "datetime_box_time"})[0]

	###财经事件tag
	cjrl_tag = main_div.find_all('dl')[0]
	first=cjrl_tag.find_all('dd')[0]
	if len(first.find_all('span',attrs={'class': 'span2'}))==0 and len(first.find_all('span', attrs={'class': 'span3'}))==0:
		pass
	else:
		zhuangtai = []
		for dd in cjrl_tag.find_all('dd'):
			cjrl_list = []
			sj = '%s  '%rq+dd.find_all('span')[0].text
			zyx = len(dd.find_all('span', attrs={'class': 'span2'})[0].find_all('b', attrs={
				'class': 'yjl_caijingyueli_star'}))
			if dd.find_all('span')[0].text == '' and zyx == 0:
				cjrl_list.append(zhuangtai[0])
				cjrl_list.append(zhuangtai[1])
			else:
				cjrl_list.append(sj)
				cjrl_list.append(zyx)

			nr = dd.find_all('span', attrs={'class': 'span3'})[0]
			nr1 = nr.find_all('em')[0].string
			nr2 = nr.text
			cjrl_list.append(nr1)
			cjrl_list.append(nr2)

			qz = dd.find_all('span', attrs={'class': 'span4'})
			if len(qz) != 0:
				cjrl_list.append(qz[0].string)
			else:
				cjrl_list.append('')

			xzqz = dd.find_all('span', attrs={'class': 'span12'})
			if len(xzqz) != 0:
				cjrl_list.append(xzqz[0].string)
			else:
				cjrl_list.append('')

			ycz = dd.find_all('span', attrs={'class': 'span5'})
			if len(ycz) != 0:
				cjrl_list.append(ycz[0].string)
			else:
				cjrl_list.append('')

			gbz = dd.find_all('span', attrs={'class': 'span6'})
			if len(gbz) != 0:
				cjrl_list.append(gbz[0].string)
			else:
				cjrl_list.append('')
			zhuangtai = cjrl_list
			cjrl_row += 1
			for col in range(len(cjrl_list)):
				sheet1.write(cjrl_row, col, cjrl_list[col])

	###央行动态
	yhdt_tag = main_div.find_all('dl')[2]
	first = yhdt_tag.find_all('dd')[0].find_all('li')
	if len(first) == 0:
		pass
	else:
		for dd in yhdt_tag.find_all('dd'):
			yhdt_list = []
			sj=dd.find_all('span',attrs={'class':'span8'})
			if len(sj)!=0:
				yhdt_list.append('%s '%rq+sj[0].string)
			else:
				yhdt_list.append('')

			zyx = dd.find_all('span', attrs={'class': 'span9'})
			if len(zyx) != 0:
				yhdt_list.append(len(zyx[0].find_all('b', attrs={'class': 'yjl_caijingyueli_star'})))
			else:
				yhdt_list.append('')

			gjdq = dd.find_all('span', attrs={'class': 'span10'})
			if len(gjdq) != 0:
				yhdt_list.append(gjdq[0].string)
			else:
				yhdt_list.append('')

			nr = dd.find_all('span', attrs={'class': 'span11'})
			if len(nr) != 0:
				yhdt_list.append(nr[0].string)
			else:
				yhdt_list.append('')
			yhdt_row+=1
			for col in range(len(yhdt_list)):
				sheet3.write(yhdt_row,col,yhdt_list[col])

	###财经事件
		cjsj_tag = main_div.find_all('dl')[1]
		first = cjsj_tag.find_all('dd')[0].find_all('li')
		if len(first) == 0:
			pass
		else:
			for dd in cjsj_tag.find_all('dd'):
				cjsj_list = []
				sj = dd.find_all('span', attrs={'class': 'span8'})
				if len(sj) != 0:
					cjsj_list.append('%s '%rq+sj[0].string)
				else:
					cjsj_list.append('')

				zyx = dd.find_all('span', attrs={'class': 'span9'})
				if len(zyx) != 0:
					cjsj_list.append(len(zyx[0].find_all('b', attrs={'class': 'yjl_caijingyueli_star'})))
				else:
					cjsj_list.append('')

				gjdq = dd.find_all('span', attrs={'class': 'span10'})
				if len(gjdq) != 0:
					cjsj_list.append(gjdq[0].string)
				else:
					cjsj_list.append('')

				nr = dd.find_all('span', attrs={'class': 'span11'})
				if len(nr) != 0:
					cjsj_list.append(nr[0].string)
				else:
					cjsj_list.append('')
				cjsj_row += 1
				for col in range(len(cjsj_list)):
					sheet2.write(cjsj_row, col, cjsj_list[col])
	time.sleep(random.randint(0,2)+random.random())
	print('正在抓取[%s]日期页面...'%rq)

#excel.save(r'd:\wancban.xls')






