import requests
import socket
socket.setdefaulttimeout(3)
with open(r'C:\Users\suhu\Desktop\code\python_spider\ip\ip.txt','r') as file:
	proxys=[]
	ip_list=file.readlines()
	ipable=[]

	for x in ip_list:
		addres=x.strip('\n').split('\t')
		if addres[2]=='HTTP':
			ip=addres[0]
			port=ip[1]
			proxy_host='http://'+ip+':'+port
			proxy={'http':proxy_host}
			proxys.append(proxy)

for x in proxys:
	print(x)