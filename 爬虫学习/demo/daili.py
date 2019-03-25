#在urllib中使用ip代理
from urllib.error import URLError
from urllib.request import ProxyHandler,build_opener


proxy = '119.101.116.41:9999'
#需要认证的代理
# proxy = 'username:password@127.0.0.1:8888'
#使用proxyHandler设置代理
proxy_handler = ProxyHandler({
    'http':'http://'+proxy,
    'http':'https://'+proxy
})

#传入参数创建Opener对象
opener = build_opener(proxy_handler)
try:
    response = opener.open('http://httpbin.org/get')
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)
#





#
# from selenium import webdriver
#
# service_args = [
#     '--proxy=127.0.0.1:9743',
#     '--proxy-type=http',
#     #'--proxy-auth=username:password' #带认证代理
# ]
#
# browser = webdriver.PhantomJS(service_args=service_args)
# browser.get('http://httpbin.org/get')
# print(browser.page_source)
