#导入相应模块
from selenium import webdriver
from selenium.webdriver.common.keys import Keys   #导入键盘键入的值
#创建浏览器并赋值
driver = webdriver.Chrome()
#访问一个网址,连接浏览器
driver.get("http://www.baidu.com")
#获取当前网页当中id属性为kw 的值
input = driver.find_element_by_id("kw")
#执行一个操作,输入键值
input.send_keys("python")
#执行回车，达到一个执行效果
input.send_keys(Keys.ENTER)
#获取页面的资源
print(driver.page_source)
# #关闭打开的网址
# driver.close()
