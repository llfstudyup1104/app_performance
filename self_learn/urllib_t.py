import http.cookiejar
import urllib.request
import os


parent_path = os.path.dirname(__file__)
filename = os.path.join(parent_path, 'cookie.txt')
cookie=http.cookiejar.MozillaCookieJar(filename=filename) #创建保存cookie的实例，保存浏览器类型的Mozilla的cookie格式
handler=urllib.request.HTTPCookieProcessor(cookie) #构建一个handler
opener=urllib.request.build_opener(handler) #构建Opener
response=opener.open('http://www.baidu.com') #请求
cookie.save(ignore_discard=True, ignore_expires=True) #保存cookie