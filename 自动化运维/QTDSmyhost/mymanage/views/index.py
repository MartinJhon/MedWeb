from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from common.models import Users
from django.shortcuts import redirect
from django.urls import reverse
import os
# Create your views here.
def index(request):
	#主页
	return render(request,"mymanage/index.html")

def login(request):
	#登录页
	return render(request,"mymanage/login.html")

def dologin(request):
	#登录保存
	try:
		ulist=Users.objects.get(username=request.POST['txtname'])
		#获取密码并md5
		import hashlib
		m = hashlib.md5()
		m.update(bytes(request.POST['txtpwd'],encoding="utf8"))
		if ulist.password == m.hexdigest():
			if ulist.state == 0:
				request.session['adminuser']=ulist.toDict() #将值传到session保存，接收是按字段接收
				photo=str(ulist.username)
				if os.path.exists("./static/mymanage/tempimg/"+photo+".jpg"):
					request.session['photo_eix']={'photo':'1'}
				else:
					if os.path.exists("./static/mymanage/tempimg/"+photo+".gif"):
						request.session['photo_eix']={'photo':'3'}
					else:
						request.session['photo_eix']={'photo':'2'}
				return redirect(reverse('mymanage_index'))
			else:
				context={'info':"不是管理员账户！"}
				return render(request,"mymanage/login.html",context)
		else:
			context={'info':"用户或密码不正确！"}
			return render(request,"mymanage/login.html",context)
	except Exception as info:
		print(info)
		context={'info':"用户或密码不正确！"}
		return render(request,"mymanage/login.html",context)

def logout(request):
	#退出
	if "adminuser" in request.session:
		del request.session['adminuser']
	return redirect(reverse('mymanage_index'))

def findphoto(request):
	try:
		#加载修改会员的表单(作废，因为取消了ajax传值)
		import os
		context={'uphoto':''}
		txt=request.GET
		photo=txt['uname']
		if os.path.exists("./static/mymanage/tempimg/"+photo+".jpg"):
			context["uphoto"]=photo+".jpg"
		elif os.path.exists("./static/mymanage/tempimg/"+photo+".png"):
			context["uphoto"]=photo+".png"
		elif os.path.exists("./static/mymanage/tempimg/"+photo+".gif"):
			context["uphoto"]=photo+".gif"
		else:
			context={'uphoto':''}
		return JsonResponse({'data':context})
	except Exception as info:
		context={"info":info}
		print(info)
		return render(request,"mymanage/info.html",context)
