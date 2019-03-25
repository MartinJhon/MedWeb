from django.shortcuts import render
from django.http import HttpResponse
from common.models import Users
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from django.core.paginator import Paginator

from PIL import Image
from datetime import datetime
import time,os
from django.db.models import Q
# Create your views here.
#会员登录
def register(request):
	return render(request,"myweb/vipuser/register.html")

#会员注册
def reguser(request):
	return render(request,"myweb/vipuser/reguser.html")

def logon(request):
	try:
		#VIP登录验证
		if request.POST['txt_name']=='':
			context={'info':'用户名不正确'}
			return render(request,"myweb/vipuser/register.html",context)

		if request.POST['txt_pwd']=='':
			context={'info':'密码不正确'}
			return render(request,"myweb/vipuser/register.html",context)

		ucount=Users.objects.filter(username=request.POST['txt_name']).count()
		if ucount==0:
			context={'info':'用户名和密码不正确'}
			return render(request,"myweb/vipuser/register.html",context)
		ulist=Users.objects.get(username=request.POST['txt_name'])
		if ulist.state==0 or ulist.state==1:
			#获取密码并md5
			import hashlib
			m = hashlib.md5() 
			m.update(bytes(request.POST['txt_pwd'],encoding="utf8"))
			if ulist.password == m.hexdigest():
				photo=str(ulist.username)
				if os.path.exists("./static/mymanage/tempimg/"+photo+".jpg"):
					request.session['photo_eix_vip']={'photo':'1'}
				else:
					if os.path.exists("./static/mymanage/tempimg/"+photo+".gif"):
						request.session['photo_eix_vip']={'photo':'3'}
					else:
						request.session['photo_eix_vip']={'photo':'2'}
				request.session['vipuser'] = ulist.toDict()
				return redirect(reverse('index'))
			else:
				context={'info':'用户名和密码不正确'}
				return render(request,"myweb/vipuser/register.html",context)
		else:
			context={'info':'用户名和密码不正确'}
			return render(request,"myweb/vipuser/register.html",context)
	except Exception as info:
		context={'info':info}
		return render(request,"myweb/vipuser/register.html",context)

#注册信息插入
def insereguser(request):
	try:
		ulist=Users()
		ulist.username=request.POST['txt_name']
		#获取密码并md5
		import hashlib
		m = hashlib.md5() 
		m.update(bytes(request.POST['txt_pwd1'],encoding="utf8"))
		ulist.password = m.hexdigest()
		ulist.save()
		context={'info':"注册成功,请重新登录!"}
		return render(request,"myweb/vipuser/reguser.html",context)
	except Exception as info:
		context={'info':"注册成功,请重新登录!"}
		return render(request,"myweb/vipuser/reguser.html",context)	

#退出系统
def exitweb(request):
	del request.session['vipuser']
	return redirect(reverse('index'))

#编辑个人信息
def editvip(request,uid):
	try:
		#加载修改会员的表单
		ulist=Users.objects.get(id=uid)
		photo=str(ulist.username)
		context={"list":ulist}
		if os.path.exists("./static/mymanage/tempimg/"+photo+".jpg"):
			context["uphoto"]=photo+".jpg"
		elif os.path.exists("./static/mymanage/tempimg/"+photo+".png"):
			context["uphoto"]=photo+".png"
		elif os.path.exists("./static/mymanage/tempimg/"+photo+".gif"):
			context["uphoto"]=photo+".gif"
		else:
			context["uphoto"]=""
		return render(request,"myweb/vipuser/edit.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"myweb/info1.html",context)

def updatevip(request):
	try:
		#修改会员信息
		list=Users.objects.get(id=request.POST['txt_id'])
		list.name=request.POST['txt_name']
		list.sex=request.POST['ra_sex']
		list.state=request.POST['ra_rob']
		list.address=request.POST['txt_addr']
		list.code=request.POST['txt_map']
		list.phone=request.POST['txt_phone']
		list.email=request.POST['txt_mail']
		list.save()
		info="修改成功！"
		mypic=request.FILES.get('txt_photo',None)
		if not mypic:
			info+="照片不更新。"
		else:
			#判断是否已经存在图片，存在先删除
			photo=str(request.POST['txt_user_hidden'])
			if os.path.exists("./static/mymanage/tempimg/"+photo+".jpg"):
				os.remove("./static/mymanage/tempimg/"+photo+".jpg")
			elif os.path.exists("./static/mymanage/tempimg/"+photo+".png"):
				os.remove("./static/mymanage/tempimg/"+photo+".png")
			elif os.path.exists("./static/mymanage/tempimg/"+photo+".gif"):
				os.remove("./static/mymanage/tempimg/"+photo+".gif")
			if mypic.name.split(".").pop() == 'png':
				img = Image.open(mypic)
				filename=str(request.POST['txt_user_hidden'])+'.jpg'
				if len(img.split()) == 4:
					#将图片png格式统一成jpg
					r, g, b, a = img.split()
					img = Image.merge("RGB",(r, g, b))
					img.save("./static/mymanage/tempimg/"+filename)
			else:
				filename=str(request.POST['txt_user_hidden'])+'.'+mypic.name.split(".").pop() #time.time()
				destination = open("./static/mymanage/tempimg/"+filename,"wb+") #图片多用wb+代表二进制操作,其他的可以使用W或者w+
				for chunk in mypic.chunks():      # 分块写入文件  
					destination.write(chunk)  
				destination.close()
			info+="并更新个人照片。"
		context={"info":info}
		return render(request,"myweb/info1.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"myweb/info1.html",context)

def editvpawd(request,uid):
	#编辑密码
	ulist=Users.objects.get(id=uid)
	context={"list":ulist}
	return render(request,"myweb/vipuser/editpwd.html",context)

def updatevpawd(request):
	try:
		#新增会员信息
		list=Users.objects.get(id=request.POST['txt_id'])
		#获取密码并md5
		import hashlib
		m = hashlib.md5()
		m.update(bytes(request.POST['oldpassword'],encoding="utf8"))
		if list.password == m.hexdigest():
			m = hashlib.md5()
			m.update(bytes(request.POST['password'],encoding="utf8"))
			list.password = m.hexdigest()
			list.save()
			info="密码重置成功！"
		else:
			info="原密码不正确，密码重置失败！"
		context={"info":info}
		return render(request,"myweb/info1.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"myweb/info1.html",context)