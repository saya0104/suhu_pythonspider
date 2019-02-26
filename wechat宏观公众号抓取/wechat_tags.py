import json
with open("公众号list.txt",'r',encoding='utf-8') as f:
    d=json.load(f)
with open("公众号list.txt",'w',encoding='utf-8',) as f:
    f.write(str(json.dumps(d,ensure_ascii=False)))
