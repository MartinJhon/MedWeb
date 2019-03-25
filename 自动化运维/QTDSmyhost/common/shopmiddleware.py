import re
from django.shortcuts import redirect
from django.urls import reverse

class SimpleMiddleware(object):
    #中间件安全函数
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # 定义网站后台不用登录也可访问的路由url
        urllist = ['/login','/dologin','/logout']
        # 获取当前请求路径
        path = request.path
        #print("Hello World!"+path)
        # 判断当前请求是否是访问网站后台,并且path不在urllist中
        if re.match("/",path) and (path not in urllist):
            # 判断当前用户是否没有登录

            if "adminuser" not in request.session:
                # 执行登录界面跳转
                return redirect(reverse('mymanage_login'))

        response = self.get_response(request)

        print(path)
        # Code to be executed for each request/response after
        # the view is called.

        return response
