from django.shortcuts import redirect
from django.urls import reverse

import re #导入正则


#中间件代码
class ShopMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response
		# One-time configuration and initialization.


	def __call__(self, request):
	# Code to be executed for each request before
	# the view (and later middleware) are called.

		# 定义网站后台不用登录也可访问的路由url，这是为了把登录页放在密码验证的外面
		urllist = ['/myadmin/login','/myadmin/dologin','/myadmin/logout','/myadmin/verify']
		# 获取当前请求路径
		path = request.path
		#print("Hello World!"+path)
		# 判断当前请求是否是访问网站后台,并且path不在urllist中
		if re.match("/myadmin",path) and (path not in urllist):
			# 判断当前用户是否没有登录
			if "adminuser" not in request.session: #判断adminuser在不在session里，即判断以前有没有登陆过
				# 执行登录界面跳转
				return redirect(reverse('myadmin_login')) #重定向跳转

		#网站前台会员登陆判断,^以什么开头
		viplist = ['/vip/register','/vip/vipadd']
		if re.match("^/orders",path) or re.match("^/vip",path) and (path not in viplist):
			# 判断当前会员是否没有登录
			if "vipuser" not in request.session: #判断vipuser在不在session里，即判断以前有没有登陆过
				# 执行登录界面跳转
				return redirect(reverse('login')) #重定向跳转


		response = self.get_response(request)

		# Code to be executed for each request/response after
		# the view is called.
		return response
