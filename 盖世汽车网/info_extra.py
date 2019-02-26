# __author__="suhu"
# -*- coding:utf-8 -*-
import xlwt
excel=xlwt.Workbook(encoding='utf-8')
sheet=excel.add_sheet('s',cell_overwrite_ok=True)
row_count=0
example=['一级分类', '二级分类', '三级分类', 'url', 'page', '公司名称', '公司标识', '公司性质', '公司地区', '成立时间', '研发人数',
         '员工人数', '法人代表', '注册资金', '年产值', '总资产', '质量体系', '年销售额', '同步开发能力', '根据图纸/样品开发能力',
         '根据客户需求描述设计生成三维数模能力', '联系人', '联系方式', '邮编', '公司地址', '主营产品', '配套客户', '出口市场']
for x in range(len(example)):
	sheet.write(0,x,example[x])
with open("info.txt",'r',encoding='utf-8') as f:
	for secentence in f.readlines():
		row_count +=1
		l=eval(secentence)
		result=l[0:6]
		for x in example[6:]:
			flag=0
			for y in l[6:]:
				if x in y:
					flag=1
					result.append(y.replace('（',')').replace('）',')').replace('~',''))
					break
			if flag==1:
				pass
			else:
				result.append('')
		for x in range(len(result)):
			sheet.write(row_count,x,result[x])
excel.save('info.xls')


