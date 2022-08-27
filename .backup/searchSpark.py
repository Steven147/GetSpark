import json, os, getSpark.web as web

baseUrl = os.getenv('baseUrl')
query = "25478323990@chatroom"
url = baseUrl + 'user?keyword=' + query

result = web.get(url=url)
result.raise_for_status()
resp = result.text
userList = json.loads(resp)

for item in userList:
    title = item['title']
    subtitle = item['subTitle']
    icon = item['icon']
    userId = item['userId']
    copyText = item['copyText']
    qlurl = item['url']
    fout.write("{}:{}\n".format(userId,copyText))

fout.close()