import requests

url = 'http://127.0.0.1:5000/politeness'
text = 'Hey, great job. Could you perhaps write down the steps you took?'
header = {"Content-Type":"application/x-www-form-urlencoded"}
values = {'sentence':text}

resp = requests.post(url,data=values,headers = header)

print resp.content
