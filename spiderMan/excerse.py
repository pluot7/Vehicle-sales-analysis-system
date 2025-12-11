import requests
import chardet


url='https://tipdm.com/'
rq =requests.get(url)
rq.status_code
rq.text
rq.headers

with open('spiderMan/web_data.txt','w',encoding='utf-8') as f:
    f.write(rq.text)

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0'
}
respose=requests.get(url,headers=headers,timeout=2)
respose.encoding=chardet.detect(respose.content)

