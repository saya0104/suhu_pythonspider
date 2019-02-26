# __author__="suhu"
# -*- coding:utf-8 -*-
import requests
import bs4
import re
import xlwt
import os
from datetime import datetime
import time
import random
regex_penalty=re.compile(r"\D(\d{1,7}|[一二三四五六七八九十]{1,3})万")
regex_shenfen=re.compile(r"会?(.{2,3})银监局")
regex_shi=re.compile(r"会?(.{2,5})银监分局")
regex_shi_1=re.compile(r"(?<=会)(.{2,5})监管分局")
import pymysql
headers={"Host":"www.cbrc.gov.cn",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"}
excel=xlwt.Workbook(encoding="utf-8")


def yjh(yjh_page):
	row_count = 0
	error_list=["银监会遗漏项"] #错误项
	#yjh sheet
	sheet1 = excel.add_sheet("银监会", cell_overwrite_ok=True)
	yjh_biaotou=["信息发布日","行政处罚决定书文号", "个人姓名", "名称", "法定代表人姓名", "主要违法违规事实", "行政处罚依据", "行政处罚决定", "作出处罚决定的机关名称", "作出处罚决定的日期","处罚金额","区域","网页链接"]
	for i in range(len(yjh_biaotou)):
		sheet1.write(row_count, i, yjh_biaotou[i])
	if yjh_page == 0:
		return []

	#制造页面url list
	yjh_url = []
	url_str = """http://www.cbrc.gov.cn/chinese/home/docViewPage/110002&current="""
	for page_count in range(yjh_page):
		yjh_url.append(url_str + str(page_count + 1))

	#遍历url_list
	for url in yjh_url:
		resp = requests.get(url, headers=headers)
		resp.encoding = resp.apparent_encoding
		soup = bs4.BeautifulSoup(resp.text, 'lxml')
		urltable = soup.find("table", attrs={"id": "testUI"})
		info_sum = len(urltable.find_all("a", attrs={"class": "STYLE8"})) #页面信息总数

		#遍历页面所有a_href
		info_count=0 #记录每一页的正在抓取数量
		for a_href in  urltable.find_all("a",attrs={"class":"STYLE8"}):
			row_count += 1  #excel表格行数
			info_count += 1 #页面url位序,print用
			title = a_href.attrs["title"]

			#展示信息
			page_count=re.findall(r"current=(\d{1,2})",url)[0]



			#对内部url请求
			url_inner = """http://www.cbrc.gov.cn""" + str(a_href.attrs["href"])
			show_str = """第%s页，第%s条,%s""" % (page_count, info_count, title)
			print(show_str)
			resp_inner = requests.get(url_inner, headers=headers)
			resp_inner.encoding = resp_inner.apparent_encoding
			soup_inner = bs4.BeautifulSoup(resp_inner.text, 'lxml')
			time.sleep(random.randint(1,2)+random.random())

			#最终信息列表
			info=[]

			#处理发布时间
			fabu_str = soup_inner.find("div", attrs={'height': '10', 'valign': 'top', 'width': '750'}).string
			fabu_time = re.findall(r"\d{4}-\d{2}-\d{2}", fabu_str)
			info.append(fabu_time)

			table_inner = soup_inner.find("table", attrs={"class": "MsoNormalTable"})
			if not table_inner :
				error_list.append(show_str +"       " + url_inner)
				row_count -= 1
				continue

			tr_list = table_inner.find_all("tr")
			if len(tr_list) != 9:
				error_list.append(show_str + "       " + url_inner)
				row_count -= 1
				continue

			tr_count =  0
			for tr in tr_list:
				tr_count += 1
				if tr_count == 2 or tr_count == 3:
					info.append("".join(tr.find_all("td")[2].stripped_strings))
				else:
					info.append("".join(tr.find_all("td")[1].stripped_strings))
			if(len(regex_penalty.findall(info[7]))) == 1:
				info.append(regex_penalty.findall(info[7])[0])
			else:
				info.append("")
			info.append("")
			info.append(url_inner)

			#写入表格
			for x in range(len(info)):
				sheet1.write(row_count, x, info[x])
	return error_list
def yjj(yjj_page):
	row_count = 0
	error_list = ["银监局遗漏项"]  # 错误项
	# yjj sheet
	sheet2 = excel.add_sheet("银监局", cell_overwrite_ok=True)
	yjj_biaotou = ["信息发布日", "行政处罚决定书文号", "个人姓名", "名称", "法定代表人姓名", "主要违法违规事实", "行政处罚依据", "行政处罚决定", "作出处罚决定的机关名称",
	               "作出处罚决定的日期", "金额", "地区", "网页链接"]
	for i in range(len(yjj_biaotou)):
		sheet2.write(row_count, i, yjj_biaotou[i])
	if yjj_page == 0:
		return []
	# 制造页面url list
	yjj_url = []
	url_str = """http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//1.html?current="""
	for page_count in range(yjj_page):
		yjj_url.append(url_str + str(page_count + 1))

	# 遍历url_list
	for url in yjj_url:
		resp = requests.get(url, headers=headers)
		resp.encoding = resp.apparent_encoding
		soup = bs4.BeautifulSoup(resp.text, 'lxml')
		urltable = soup.find("table", attrs={"id": "testUI"})
		info_sum = len(urltable.find_all("a", attrs={"class": "STYLE8"}))  # 页面信息总数

		# 遍历页面所有a_href
		info_count = 0  # 记录每一页的正在抓取数量
		for a_href in urltable.find_all("a", attrs={"class": "STYLE8"}):
			row_count += 1  # excel表格行数
			info_count += 1  # 页面url位序,print用
			title = a_href.attrs["title"]

			# 展示信息
			page_count = re.findall(r"current=(\d{1,2})", url)[0]
			show_str = """第%s页，第%s条,%s""" % (page_count, info_count, title)
			print(show_str)

			# 对内部url请求
			url_inner = """http://www.cbrc.gov.cn""" + str(a_href.attrs["href"])
			resp_inner = requests.get(url_inner, headers=headers)
			resp_inner.encoding = resp_inner.apparent_encoding
			soup_inner = bs4.BeautifulSoup(resp_inner.text, 'lxml')
			time.sleep(random.randint(1, 2) + random.random())
			# 最终信息列表
			info = []

			# 处理发布时间
			fabu_str = soup_inner.find("div", attrs={'height': '10', 'valign': 'top', 'width': '750'}).string
			fabu_time = re.findall(r"\d{4}-\d{2}-\d{2}", fabu_str)
			info.append(fabu_time)

			table_inner = soup_inner.find("table", attrs={"class": "MsoNormalTable"})
			if not table_inner:
				error_list.append(show_str + "       " + url_inner)
				row_count -= 1
				continue

			tr_list = table_inner.find_all("tr")
			if len(tr_list) != 9:
				error_list.append(show_str + "       " + url_inner)
				row_count -= 1
				continue

			tr_count = 0
			for tr in tr_list:
				tr_count += 1
				if tr_count == 2 or tr_count == 3:
					info.append("".join(tr.find_all("td")[2].stripped_strings))
				else:
					info.append("".join(tr.find_all("td")[1].stripped_strings))

			if (len(regex_penalty.findall(info[7]))) == 1:
				info.append(regex_penalty.findall(info[7])[0])
			else:
				info.append("")

			if (len(regex_shenfen.findall(title)) == 1):
				info.append(regex_shenfen.findall(title)[0])
			else:
				info.append("")

			info.append(url_inner)

			# 写入表格
			for x in range(len(info)):
				sheet2.write(row_count, x, info[x])
	return error_list
def yjfj(yjfj_page):
	row_count = 0
	error_list = ["银监分局遗漏项"]  # 错误项
	# yjfj sheet
	sheet3 = excel.add_sheet("银监分局", cell_overwrite_ok=True)
	yjfj_biaotou = ["信息发布日", "行政处罚决定书文号", "个人姓名", "名称", "法定代表人姓名", "主要违法违规事实", "行政处罚依据", "行政处罚决定", "作出处罚决定的机关名称",
	                "作出处罚决定的日期", "处罚金额", "地区", "网页链接"]
	for i in range(len(yjfj_biaotou)):
		sheet3.write(row_count, i, yjfj_biaotou[i])
	if yjfj_page == 0:
		return []
	# 制造页面url list
	yjfj_url = []
	url_str = """http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//2.html?current="""
	for page_count in range(yjfj_page):
		yjfj_url.append(url_str + str(page_count + 1))

	# 遍历url_list
	for url in yjfj_url:
		resp = requests.get(url, headers=headers)
		resp.encoding = resp.apparent_encoding
		soup = bs4.BeautifulSoup(resp.text, 'lxml')
		urltable = soup.find("table", attrs={"id": "testUI"})
		info_sum = len(urltable.find_all("a", attrs={"class": "STYLE8"}))  # 页面信息总数

		# 遍历页面所有a_href
		info_count = 0  # 记录每一页的正在抓取数量
		for a_href in urltable.find_all("a", attrs={"class": "STYLE8"}):
			row_count += 1  # excel表格行数
			info_count += 1  # 页面url位序,print用
			title = a_href.attrs["title"]

			# 展示信息
			page_count = re.findall(r"current=(\d{1,2})", url)[0]
			show_str = """第%s页，第%s条,%s""" % (page_count, info_count, title)
			print(show_str)

			# 对内部url请求
			url_inner = """http://www.cbrc.gov.cn""" + str(a_href.attrs["href"])
			resp_inner = requests.get(url_inner, headers=headers)
			resp_inner.encoding = resp_inner.apparent_encoding
			soup_inner = bs4.BeautifulSoup(resp_inner.text, 'lxml')
			time.sleep(random.randint(1, 2) + random.random())

			# 最终信息列表
			info = []

			# 处理发布时间
			fabu_str = soup_inner.find("div", attrs={'height': '10', 'valign': 'top', 'width': '750'}).string
			fabu_time = re.findall(r"\d{4}-\d{2}-\d{2}", fabu_str)
			info.append(fabu_time)

			table_inner = soup_inner.find("table", attrs={"class": "MsoNormalTable"})
			if not table_inner:
				error_list.append(show_str + "       " + url_inner)
				row_count -= 1
				continue

			tr_list = table_inner.find_all("tr")
			if len(tr_list) != 9:
				error_list.append(show_str + "       " + url_inner)
				row_count -= 1
				continue

			tr_count = 0
			for tr in tr_list:
				tr_count += 1
				if tr_count == 2 or tr_count == 3:
					info.append("".join(tr.find_all("td")[2].stripped_strings))
				else:
					info.append("".join(tr.find_all("td")[1].stripped_strings))

			if (len(regex_penalty.findall(info[7]))) == 1:
				info.append(regex_penalty.findall(info[7])[0])
			else:
				info.append("")

			if regex_shi.findall(title) or regex_shi_1.findall(title):
				if "中国" in title:
					if len(regex_shi_1.findall(title)) == 1:
						info.append(regex_shi_1.findall(title)[0])
					else:
						info.append("")
				else:
					if (len(regex_shi.findall(title)) == 1):
						info.append(regex_shi.findall(title)[0])
					else:
						info.append("")
			else:
				info.append("")

			info.append(url_inner)

			# 写入表格
			for x in range(len(info)):
				sheet3.write(row_count, x, info[x])
	return error_list

print("***银监处罚信息抓取***")
print("author: suhu")
print("请依次输入3个页码(0表示对应项不抓取)")
print("")


page1=int(input("请输入银监会抓取页码:"))
page2=int(input("请输入银监局抓取页码:"))
page3=int(input("请输入银监分局抓取页码:"))

resp_list1 = yjh(page1)
resp_list2 = yjj(page2)
resp_list3 = yjfj(page3)
resp_sum = resp_list1 + resp_list2 + resp_list3
excute_time=datetime.now().strftime("%Y_%m_%d_%H%M%S")

excel.save(os.path.join(os.getcwd(),"处罚信息_%s.xls"%excute_time))
with open(os.path.join(os.getcwd(),"record_%s.txt"%excute_time),'w',encoding="utf-8") as f:
	for x in resp_sum:
		f.write(x+"\n")
for x in resp_sum:
	print(x)

























