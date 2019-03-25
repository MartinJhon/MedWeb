from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from common.models import Users
from django.core.paginator import Paginator

from PIL import Image
from datetime import datetime
import time,os
from django.db.models import Q

# Create your views here.

def index(request,pIndex):
	#显示会员信息列表
	mywhere=[]
	txt1=request.GET.get("txt_find",'0')
	txt2=request.GET.get("txt_sex",'0')
	print(txt1)
	print(txt2)
	if txt1 !='0' and txt2!='0':
		if txt2 =='3':
			ulist=Users.objects.filter(Q(sex=0),Q(username__contains=txt1)|Q(name__contains=txt1)|Q(email__contains=txt1))
		elif txt2 == '1':
			ulist=Users.objects.filter(Q(sex=1),Q(username__contains=txt1)|Q(name__contains=txt1)|Q(email__contains=txt1))
		mywhere.append('txt_find='+txt1)
		mywhere.append('txt_sex='+txt2)
	elif txt1 !="0":
		ulist=Users.objects.filter(Q(username__contains=txt1)|Q(name__contains=txt1)|Q(email__contains=txt1))
		mywhere.append('txt_find='+txt1)
	elif txt2!='0':
		if txt2 =='3':
			ulist=Users.objects.filter(sex=0)
		elif txt2 == '1':
			ulist=Users.objects.filter(sex=1)
		mywhere.append('txt_sex='+txt2)
	else:
		ulist=Users.objects.all() #获取所有的记录
	p = Paginator(ulist, 10) #分页显示，一页10条
	if pIndex == '':
		pIndex = '1'
	pIndex = int(pIndex)
	list = p.page(pIndex) #获取索引页对应的数据对象
	plist = p.page_range #获取分页索引所有对象
	context={'userlist': list, 'plist': plist, 'pIndex': pIndex,'plist_len':len(plist),'mywhere':mywhere}
	return render(request,"mymanage/users/index.html",context)

def add(request):
	#加载会员增加表单
	return render(request,"mymanage/users/add.html")

def insert(request):
	try:
		#新增会员信息
		list=Users()
		list.username=request.POST['txt_user']
		#获取密码并md5
		import hashlib
		m = hashlib.md5() 
		m.update(bytes(request.POST['password'],encoding="utf8"))
		list.password = m.hexdigest()

		list.name=request.POST['txt_name']
		list.sex=request.POST['ra_sex']
		list.state=request.POST['ra_rob']
		list.address=request.POST['txt_addr']
		list.code=request.POST['txt_map']
		list.phone=request.POST['txt_phone']
		list.email=request.POST['txt_mail']
		list.save()
		info="保存成功！"
		mypic=request.FILES.get('txt_photo',None)
		if not mypic:
			info+="照片为空。"
		else:
			if mypic.name.split(".").pop() == 'png':
				img = Image.open(mypic)
				filename=str(request.POST['txt_user'])+'.jpg'
				if len(img.split()) == 4:
					#将图片png格式统一成jpg
					r, g, b, a = img.split()
					img = Image.merge("RGB",(r, g, b))
					img.save("./static/mymanage/tempimg/"+filename)
			else:
				filename=str(request.POST['txt_user'])+'.'+mypic.name.split(".").pop() #time.time()
				destination = open("./static/mymanage/tempimg/"+filename,"wb+") #图片多用wb+代表二进制操作,其他的可以使用W或者w+
				for chunk in mypic.chunks():      # 分块写入文件  
					destination.write(chunk)  
				destination.close()
			info+="并有个人照片。"
		context={"info":info}
		return render(request,"mymanage/info.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"mymanage/info.html",context)

def edit(request,uid):
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
		return render(request,"mymanage/users/edit.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"mymanage/info.html",context)

def update(request):
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
		return render(request,"mymanage/info.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"mymanage/info.html",context)

def delete(request,uid):
	try:
		#删除会员信息
		ulist=Users.objects.get(id=uid)
		photo=str(ulist.username)
		if os.path.exists("./static/mymanage/tempimg/"+photo+".jpg"):
			os.remove("./static/mymanage/tempimg/"+photo+".jpg")
		elif os.path.exists("./static/mymanage/tempimg/"+photo+".png"):
			os.remove("./static/mymanage/tempimg/"+photo+".png")
		elif os.path.exists("./static/mymanage/tempimg/"+photo+".gif"):
			os.remove("./static/mymanage/tempimg/"+photo+".gif")
		ulist.delete()
		context={"info":"删除成功！"}
	except Exception as info:
		context={"info":info}
	return render(request,"mymanage/info.html",context)

def editpawd(request,uid):
	#编辑密码
	ulist=Users.objects.get(id=uid)
	context={"list":ulist}
	return render(request,"mymanage/users/editpawd.html",context)

def updatepawd(request):
	try:
		#新增会员信息
		list=Users.objects.get(id=request.POST['txt_id'])
		#获取密码并md5
		import hashlib
		m = hashlib.md5() 
		m.update(bytes(request.POST['password'],encoding="utf8"))
		list.password = m.hexdigest()
		list.save()
		info="密码重置成功！"
		context={"info":info}
		return render(request,"mymanage/info.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"mymanage/info.html",context)

def findall(request,pIndex):
	#显示会员信息列表
	list=[]
	lplist=[]
	ulist=Users.objects.all() #获取所有的记录
	p = Paginator(ulist, 10) #分页显示，一页10条
	if pIndex == '':
		pIndex = '1'
	pIndex = int(pIndex)
	list1 = p.page(pIndex) #获取索引页对应的数据对象
	plist = p.page_range #获取分页索引所有对象
	for i in plist:
		lplist.append({'plist':i})
	for i in list1:
		list.append({'id':i.id,'username':i.username,'name':i.name,'sex':i.sex,'address':i.address,'code':i.code,'phone':i.phone,'email':i.email,'state':i.state,'addtime':i.addtime})
	list.append({'plist': lplist, 'pIndex': pIndex,'plist_len':len(plist)})
	print(list)
	return JsonResponse({'data':list})

def selfind(request,pIndex):
	#检索查询
	try:
		list=[]
		lplist=[]
		mywhere1=[] #定义一个用于存放搜索条件列表
		mywhere2=[]
		txt=request.GET
		txt1=txt['txt_info1']
		txt2=txt['txt_info2']
		print(txt1)
		print(txt2)
		if txt2!='' and txt1!='':
			if txt2 == '3':
				ulist=Users.objects.filter(Q(sex=0),Q(username__contains=txt1)|Q(name__contains=txt1)|Q(email__contains=txt1))
			else:
				ulist=Users.objects.filter(Q(sex=1),Q(username__contains=txt1)|Q(name__contains=txt1)|Q(email__contains=txt1))
			mywhere1.append('txt_find='+txt1)
			mywhere2.append('txt_sex='+txt2)
		elif txt2!='':
			if txt2 == '3':
				ulist=Users.objects.filter(sex=0)
			else:
				ulist=Users.objects.filter(sex=1)
			mywhere2.append('txt_sex='+txt2)
		elif txt1!='':
			ulist=Users.objects.filter(Q(username__contains=txt1)|Q(name__contains=txt1)|Q(email__contains=txt1))
			mywhere1.append('txt_find='+txt1)
		else:
			ulist=Users.objects.all()
		p = Paginator(ulist, 10) #分页显示，一页10条
		if pIndex == '':
			pIndex=1
		pIndex = int(pIndex)
		list1 = p.page(pIndex) #获取索引页对应的数据对象
		plist = p.page_range #获取分页索引所有对象
		for i in plist:
			lplist.append({'plist':i})
		for i in list1:
			list.append({'id':i.id,'username':i.username,'name':i.name,'sex':i.sex,'address':i.address,'code':i.code,'phone':i.phone,'email':i.email,'state':i.state,'addtime':i.addtime})
		list.append({'plist': lplist, 'pIndex': pIndex,'plist_len':len(plist),'mywhere1':mywhere1,'mywhere2':mywhere2})
		return JsonResponse({'data':list})
	except Exception as info:
		context={'info':info}
		return render(request,"mymanage/info.html",context)