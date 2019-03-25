#导入webdriver驱动
from selenium import webdriver
'''
    声明浏览器对象
'''
# driver = webdriver.Chrome()  #声明谷歌浏览器
# driver = webdriver.FireFox() #火狐 需：GeckoDriver驱动
# driver = webdriver.Edge()
# driver = webdriver.Safari()
driver = webdriver.PhantomJS() #无界面浏览器
'''
    访问页面
'''
#访问一个url地址
driver.get("http://www.taobao.com")
#获取页面资源
print(driver.page_source)
##关闭浏览器
#driver.close()
