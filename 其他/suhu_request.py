"""
参数为网址和headers
返回可以处理的html
"""

import requests

def suhu_request_get(url,headers):
	r=requests.get(url=url,headers=headers)
	r.encoding=r.apparent_encoding
	return r.text