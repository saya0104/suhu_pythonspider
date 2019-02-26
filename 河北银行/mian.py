from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import random
import json
import os
webdriver.I
driver = webdriver.Chrome(executable_path=os.path.join(os.getcwd(),'chromedriver.exe'))
driver.get("https://www.hebbank.com/corporbank/otherBankQueryWeb.do")

with open("record.txt",'r',encoding='utf-8') as f:
	record_d=json.load(f)

bank_r = record_d["bank_r"]
province_r = record_d["province_r"]
city_r = record_d["city_r"]
with open("bank_info.txt",'a',encoding='utf-8') as file:
	try:
		while True:
			banks = driver.find_element_by_id("bankTypeSelect").find_elements_by_tag_name("option")
			bank_count = len(banks) - 1
			if bank_r <= bank_count:
				banks[bank_r].click()

				time.sleep(1)
				provinces = driver.find_element_by_id("provinceSelect").find_elements_by_tag_name("option")
				province_count = len(provinces) - 1
				if province_r <= province_count:
					provinces[province_r].click()

					time.sleep(1)
					citys = driver.find_element_by_id("citySelect").find_elements_by_tag_name("option")
					city_count = len(citys) - 1
					# print(city_count)
					# print(citys)
					# print(driver.page_source)
					if city_r <= city_count:
						citys[city_r].click()
						print("抓取至[%s-%s-%s]..." % (banks[bank_r].text, provinces[province_r].text, citys[city_r].text))




						checkcode = input("请输入验证码:")
						driver.find_element_by_id("checkCodeText").clear()
						driver.find_element_by_id("checkCodeText").send_keys(checkcode)
						driver.find_element_by_id("queryButton").click()
						time.sleep(2)
						html = driver.page_source
						if '验证码输入错误' not in html:
							soup = bs(html, 'lxml')
							tbody = soup.find('tbody', attrs={"id": 'resultTableBody'})
							for tr in tbody.find_all('tr'):
								info = []
								for td in tr.find_all('td'):
									info.append(td.string.replace(' ', '').replace('\t', ''))
								info_str = "%-60s\t\t\t%-s\n" % (info[0], info[1])
								file.write(info_str)
							city_r += 1
							driver.refresh()
						else:
							print("验证码输入有误,重新输入...")
							driver.refresh()
					else:
						province_r += 1
						city_r = 0
				else:
					bank_r += 1
					province_r = 0
			else:
				break
				print("i will be always fuck you ")
	except:
		record_d["bank_r"]=bank_r
		record_d["province_r"]=province_r
		record_d["city_r"]=	city_r
		with open("record.txt", 'w', encoding='utf-8') as f:
			f.write(json.dumps(record_d))
