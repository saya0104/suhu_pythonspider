import requests
import random
import json
cookies={"data_ticket": "kO/fzkfQOWgMeauZu0uWRoAJPhqQGwRp4B0oDMMQ3LVv9FP4SdeMXudq5obhNXfX", "xid": "2fce30afddffe8fd4af870a3114ffc66", "uuid": "ec21272d564ceab6e1c4af87ebc9dcc9", "ticket": "069f34c60ced6e0777f41752cb809f072bc77130", "remember_acct": "whfi_brcx9713%40163.com", "cert": "ogMgcoDcfLtNKcpAkTXyjgLSLn2TEty8", "ticket_id": "gh_7b318dff7b98", "noticeLoginFlag": "1", "data_bizuin": "3265662822", "openid2ticket_oZg-mwju6UwXJLEI2S7UkQgSAB3w": "IB77Rn25c2VsC1HJqNhWdwTtR+BtvYyrqFiMOtwdwUg=", "mm_lang": "zh_CN", "ua_id": "W3YtKcReIAZAi8yKAAAAAHcymIXiizdOV7kQmQDjbj8=", "slave_user": "gh_7b318dff7b98", "slave_sid": "Ymw1SUxGY2dUSFhYRzNRbE1UdjZHMzNDeTQ1MXRUblI4X2dYNDI0ejc1czRfS0xqOWtIM2ZLblVQMFlsRk9OUGxzakUxUHNiTGh2Zk1XOVI1ZWpmX3ppREhMUEp0R0pFOVRfWWJTemlVeXE2OWsyc3k2bnBXMGFTT1dZalFlS0hiUDVCYlhyWVNKZnZZSkVP", "bizuin": "3203806539"}


appmsg_id = {
			'token': 1053996541,
			'lang': 'zh_CN',
			'f': 'json',
			'ajax': '1',
			'random': random.random(),
			'action': 'list_ex',
			'begin': 0,
			'count': '5',
			'query': '',
			'fakeid': 'MzA3MDU4NjU4MA==',
			'type': '9'}

headers={
		'Host': 'mp.weixin.qq.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
	}
appmsg_url="https://mp.weixin.qq.com/cgi-bin/appmsg?"

resp_appmsg=requests.get(appmsg_url,params=appmsg_id,headers=headers,cookies=cookies,verify=False)
info_list = resp_appmsg.json().get("app_msg_list")
print(info_list)