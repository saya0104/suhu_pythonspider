# __author__="suhu"
# -*- coding:utf-8 -*-
import requests
import json
import re
headers={
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
"Cache-Control":"no-cache",
"Pragma": "no-cache",
"Referer": "http://datainfo.fx168.com/calendar.shtml"
}
url='http://fx168api.fx168.com/InterfaceCollect/default.aspx'
params={
'succ_callback':'CallbackFinanceListDataByDate',
'Code':'fx168',
'bCode':'IFinancialCalendarData2017-11-12'
}


resp=requests.get(url=url,headers=headers,params=params)
print(resp.url)
print(resp.status_code)
content=resp.content.decode('utf-8')
regex=re.compile(r"CallbackFinanceListDataByDate\((.*)\)")
a=regex.findall(content)
print(a[0])
c=json.loads(a[0])


a="{'a':'1','b':'2','c':'3'}"
