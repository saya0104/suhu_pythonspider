import requests
import bs4
import re
import datetime
from selenium import webdriver
import time
import os

user_name="***"
user_password="***"
chromepath=os.path.join(os.getcwd(),"chromedriver.exe")
driver = webdriver.Chrome(executable_path=chromepath)
driver.get("https://www.tongyeyun.com/japi/loginPage")
verifycode=input("please enter the verifycode :")
driver.find_element_by_id("userName").clear()
driver.find_element_by_id("userName").send_keys(user_name)
driver.find_element_by_id("pwd").clear()
driver.find_element_by_id("pwd").send_keys(user_password)
driver.find_element_by_id("verifyCode").clear()
driver.find_element_by_id("verifyCode").send_keys(verifycode)
driver.find_element_by_id("loginCommit").click()
cookies=driver.get_cookies()
jsession_id=cookies[0].get('value')
driver.close()

headers={
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
"Host":"www.tongyeyun.com",
"Accept":"text/html, */*; q=0.01",
"Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
"Accept-Encoding":"gzip, deflate, br",
"Referer":"https://www.tongyeyun.com/tongyeyunweb/ncdPrimary/showNcd",
"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
"X-Requested-With":"XMLHttpRequest",
"Content-Length":"61",
"Connection":"keep-alive"
}

headers={
"Host":"www.tongyeyun.com",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
"Accept-Encoding":"gzip, deflate, br",
"Referer":"https://www.tongyeyun.com/tongyeyunweb/ncdPrimary/showNcd"
}
url="https://www.tongyeyun.com/tongyeyunweb/ncdPrimary/dataList?addTime=%s"%datetime.datetime.now().strftime("%Y-%m-%d")

cookies={
"JSESSIONID":jsession_id
}

def getinfo():
	resp=requests.get(url,headers=headers,cookies=cookies)
	print("execute time:"+str(datetime.datetime.now()))
	print("http statue_code :"+str(resp.status_code))
	html="""<body>"""+resp.text+"</body>"
	soup=bs4.BeautifulSoup(html,"lxml")
	pingji_list=[tag for tag in soup.find("body").contents if re.findall(r"^<div",str(tag))]
	for pingji_tag in pingji_list:
		dengji=pingji_tag.find("div",attrs={"class":"quot-td wp13 tcenter"}).find("span",attrs={"class":"fb"}).string
		for bankrow in pingji_tag.find_all("div",attrs={"class":"quot-tr"}):
			i=0
			qixian_l = ["1m", "3m", "6m", "9m", "1y", "2y", "3y"]
			for tag in bankrow.find_all("div",attrs={"class":"quot-td wp10 tcenter"}):
				item=tag.find_all("span")[0]
				bankinfo_dict = {}
				bankinfo_dict["grade"] = dengji
				bankinfo_dict["duration"] = qixian_l[i]
				bankinfo_dict["issueorg"] = item.attrs["issueorg"]
				for x in list(tag.find_all("span")[0].stripped_strings):
					if len(x) != 1:
						bankinfo_dict["rate"]=x
				bankinfo_dict["remark"] = item.attrs["remark"]
				bankinfo_dict["issuetime"] = item.attrs["issuetime"]
				bankinfo_dict["source"] = item.attrs["source"]
				bankinfo_dict["amount"] = item.attrs["amount"]
				if tag.find("span",attrs={"class":"quot-rise"}):
					bankinfo_dict["arrow"]="red_up"
				else:
					bankinfo_dict["arrow"]=""
				if tag.find("span",attrs={"class":"3"}):
					bankinfo_dict["line"]="1"
				else:
					bankinfo_dict["line"]="0"
				if tag.find("span",attrs={"class":"board-icon4"}):
					bankinfo_dict["star"]="1"
				else:
					bankinfo_dict["star"]="0"
				i += 1;
				print(bankinfo_dict)
			i = 0
while 1:
	getinfo()
	time.sleep(20)
