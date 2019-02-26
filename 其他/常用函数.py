
bank=td_list[0].text.replace('&nbsp;','')
		value_list.append(bank)

		buyin_ex=td_list[1].text.replace('&nbsp;','')
		value_list.append(buyin_ex)

		buyin_cur=td_list[2].text.replace('&nbsp;','')
		value_list.append(buyin_cur)

		sell_ex=td_list[3].text.replace('&nbsp;','')
		value_list.append(sell_ex)

		sell_cur=td_list[4].text.replace('&nbsp;', '')
		value_list.append(sell_cur)

		middle=td_list[5].text.replace('&nbsp;', '')
		value_list.append(middle)

		print('正在抓取%s...'%row_num)
		for x in range(1,7):
			sheet1.write(row_num,x,value_list[x])


excel.save(r'd:\te1.xls')

