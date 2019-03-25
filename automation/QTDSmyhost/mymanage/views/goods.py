from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from common.models import Goods,Types
from django.core.paginator import Paginator

from PIL import Image
from datetime import datetime
import time,os,json
import random
from django.db.models import Q

# Create your views here.

def index(request,pIndex):
	#显示会员信息列表
	tlist=Types.objects.extra(select={'_has':'concat(path,id)'}).order_by('_has')
	for i in tlist:
		i.pram='. . . .'*(i.path.count(',')-1)

	mywhere=[] #定义一个用于存放搜索条件列表
	txtname=request.GET.get("txt_fname",None)
	if txtname==None:
		ulist=Goods.objects.all() #获取所有的记录
	else:
		ulist=Goods.objects.filter(goods__contains=txtname) #获取所有的记录
		mywhere.append("txt_fname="+txtname)

	txtstate=request.GET.get("mysel2",None)

	if txtstate=='1':
		ulist=ulist.filter(state=1)
		mywhere.append("mysel2="+txtstate)
	elif txtstate=='2':
		ulist=ulist.filter(state=2)
		mywhere.append("mysel2="+txtstate)
	elif txtstate==3:
		ulist=ulist.filter(state=3)
		mywhere.append("mysel2="+txtstate)

	txttype=request.GET.get("mysel1",'0')
	if txttype!='0':
		mywhere.append("mysel1="+txttype)
		typelist=[]
		utylist=Types.objects.filter(Q(id=int(txttype))|Q(path__contains=int(txttype)))
		for i in utylist:
			typelist.append(i.id)
		ulist=ulist.filter(typeid__in=typelist)

	for i in ulist:
		tyname=Types.objects.get(id=i.typeid)
		i.tyname=tyname.name
		i.pram='. . . .'*(tyname.path.count(',')-1)
	p = Paginator(ulist, 10) #分页显示，一页10条
	if pIndex == '':
		pIndex = '1'
	pIndex = int(pIndex)
	list = p.page(pIndex) #获取索引页对应的数据对象
	plist = p.page_range #获取分页索引所有对象
	print(mywhere)
	context={'goodslist': list, 'plist': plist, 'pIndex': pIndex,'plist_len':len(plist),'tlist':tlist,'mywhere':mywhere,'mysel1':int(txttype)}
	return render(request,"mymanage/Goods/index.html",context)

def add(request):
	#加载会员增加表单
	tlist=Types.objects.extra(select={'_has':'concat(path,id)'}).order_by('_has')
	for i in tlist:
		i.pram='. . . .'*(i.path.count(',')-1)
	context={'tlist':tlist}
	return render(request,"mymanage/Goods/add.html",context)

def insert(request):
	try:
		#新增会员信息
		mypic=request.FILES.get('txt_photo',None)
		if not mypic:
			info="照片不能为空！"
			context={"info":info}
			return render(request,"mymanage/info.html",context)
		if mypic.name.split(".").pop() == 'png':
			img = Image.open(mypic)
			filename=str(time.strftime("%Y%m%d%H%M%S"))+'-'+str(random.choice(range(10000)))+'.jpg'
			if len(img.split()) == 4:
				#将图片png格式统一成jpg
				r, g, b, a = img.split()
				img = Image.merge("RGB",(r, g, b))
				img.save("./static/mymanage/goods/"+filename)
				# 执行图片缩放
				im = Image.open("./static/mymanage/goods/"+filename)
				# 缩放到375*375:
				im.thumbnail((375, 375))
				# 把缩放后的图像用jpeg格式保存:
				im.save("./static/mymanage/goods/"+filename, 'jpeg')
				# 缩放到220*220:
				im.thumbnail((220, 220))
				# 把缩放后的图像用jpeg格式保存:
				im.save("./static/mymanage/goods/m_"+filename, 'jpeg')
				# 缩放到75*75:
				im.thumbnail((75, 75))
				# 把缩放后的图像用jpeg格式保存:
				im.save("./static/mymanage/goods/s_"+filename, 'jpeg')
		else:
			if mypic.name.split(".").pop() == 'gif':
				filename=str(time.strftime("%Y%m%d%H%M%S"))+'-'+str(random.choice(range(10000)))+'.'+ mypic.name.split(".").pop() #time.time()
				destination = open("./static/mymanage/goods/"+filename,"wb+") #图片多用wb+代表二进制操作,其他的可以使用W或者w+
				for chunk in mypic.chunks():      # 分块写入文件  
					destination.write(chunk)  
				destination.close()

				destination = open("./static/mymanage/goods/m_"+filename,"wb+") #图片多用wb+代表二进制操作,其他的可以使用W或者w+
				for chunk in mypic.chunks():      # 分块写入文件  
					destination.write(chunk)  
				destination.close()

				destination = open("./static/mymanage/goods/s_"+filename,"wb+") #图片多用wb+代表二进制操作,其他的可以使用W或者w+
				for chunk in mypic.chunks():      # 分块写入文件  
					destination.write(chunk)  
				destination.close()
			else:
				filename=str(time.strftime("%Y%m%d%H%M%S"))+'-'+str(random.choice(range(10000)))+'.'+ mypic.name.split(".").pop() #time.time()
				destination = open("./static/mymanage/goods/"+filename,"wb+") #图片多用wb+代表二进制操作,其他的可以使用W或者w+
				for chunk in mypic.chunks():      # 分块写入文件  
					destination.write(chunk)  
				destination.close()

				# 执行图片缩放
				im = Image.open("./static/mymanage/goods/"+filename)
				# 缩放到375*375:
				im.thumbnail((375, 375))
				# 把缩放后的图像用jpeg格式保存:
				im.save("./static/mymanage/goods/"+filename, 'jpeg')
				# 缩放到220*220:
				im.thumbnail((220, 220))
				# 把缩放后的图像用jpeg格式保存:
				im.save("./static/mymanage/goods/m_"+filename, 'jpeg')
				# 缩放到75*75:
				im.thumbnail((75, 75))
				# 把缩放后的图像用jpeg格式保存:
				im.save("./static/mymanage/goods/s_"+filename, 'jpeg')

		list=Goods()
		list.goods=request.POST['txt_name']
		list.typeid=request.POST['txt_type']
		list.company=request.POST['txt_pro']
		list.state=request.POST['ra_rob']
		list.content=request.POST['txt_text']
		list.price=request.POST['txt_price']
		list.picname=filename
		list.save()
		info="保存成功！"
		context={"info":info}
		return render(request,"mymanage/info.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"mymanage/info.html",context)

def edit(request,uid):
	try:
		#加载修改会员的表单
		ulist=Goods.objects.get(id=uid)
		tlist=Types.objects.extra(select={'_has':'concat(path,id)'}).order_by('_has')
		for i in tlist:
			i.pram='. . . .'*(i.path.count(',')-1)
		context={"list":ulist,"tlist":tlist}
		return render(request,"mymanage/Goods/edit.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"mymanage/info.html",context)

def update(request):
	try:
		#修改会员信息
		list=Goods.objects.get(id=request.POST['txt_id'])
		list.goods=request.POST['txt_name']
		list.typeid=request.POST['txt_type']
		list.company=request.POST['txt_pro']
		list.state=request.POST['ra_rob']
		list.content=request.POST['txt_text']
		list.price=request.POST['txt_price']

		mypic=request.FILES.get('txt_photo',None)
		if not mypic:
			list.picname=list.picname
		else:
			if mypic.name.split(".").pop() == 'png':
				img = Image.open(mypic)
				print(len(img.split()))
				filename=str(time.strftime("%Y%m%d%H%M%S"))+'-'+str(random.choice(range(10000)))+'.jpg'
				if len(img.split()) == 4:
					#将图片png格式统一成jpg
					r, g, b, a = img.split()
					img = Image.merge("RGB",(r, g, b))
					img.save("./static/mymanage/goods/"+filename)
					# 执行图片缩放
					im = Image.open("./static/mymanage/goods/"+filename)
					# 缩放到375*375:
					im.thumbnail((375, 375))
					# 把缩放后的图像用jpeg格式保存:
					im.save("./static/mymanage/goods/"+filename, 'jpeg')
					# 缩放到220*220:
					im.thumbnail((220, 220))
					# 把缩放后的图像用jpeg格式保存:
					im.save("./static/mymanage/goods/m_"+filename, 'jpeg')
					# 缩放到75*75:
					im.thumbnail((75, 75))
					# 把缩放后的图像用jpeg格式保存:
					im.save("./static/mymanage/goods/s_"+filename, 'jpeg')

					photoname_big=list.picname #获取图片的名称
					photoname_small='s_'+photoname_big #获取图片的名称
					photoname_Min='m_'+photoname_big
					#执行图片删除旧的图片
					os.remove("./static/mymanage/goods/"+photoname_small)
					os.remove("./static/mymanage/goods/"+photoname_big)
					os.remove("./static/mymanage/goods/"+photoname_Min)
			else:
				if mypic.name.split(".").pop() == 'gif':
					filename=str(time.strftime("%Y%m%d%H%M%S"))+'-'+str(random.choice(range(10000)))+'.'+mypic.name.split(".").pop() #time.time()
					destination = open("./static/mymanage/goods/"+filename,"wb+") #图片多用wb+代表二进制操作,其他的可以使用W或者w+
					for chunk in mypic.chunks():      # 分块写入文件  
						destination.write(chunk)  
					destination.close()

					destination = open("./static/mymanage/goods/m_"+filename,"wb+") #图片多用wb+代表二进制操作,其他的可以使用W或者w+
					for chunk in mypic.chunks():      # 分块写入文件  
						destination.write(chunk)  
					destination.close()

					destination = open("./static/mymanage/goods/s_"+filename,"wb+") #图片多用wb+代表二进制操作,其他的可以使用W或者w+
					for chunk in mypic.chunks():      # 分块写入文件  
						destination.write(chunk)
					destination.close()
					
					photoname_big=list.picname #获取图片的名称
					photoname_small='s_'+photoname_big #获取图片的名称
					photoname_Min='m_'+photoname_big
					#执行图片删除，旧的图片
					os.remove("./static/mymanage/goods/"+photoname_small)
					os.remove("./static/mymanage/goods/"+photoname_big)
					os.remove("./static/mymanage/goods/"+photoname_Min)
				else:
					filename=str(time.strftime("%Y%m%d%H%M%S"))+'-'+str(random.choice(range(10000)))+'.'+mypic.name.split(".").pop() #time.time()
					destination = open("./static/mymanage/goods/"+filename,"wb+") #图片多用wb+代表二进制操作,其他的可以使用W或者w+
					for chunk in mypic.chunks():      # 分块写入文件  
						destination.write(chunk)  
					destination.close()
					# 执行图片缩放
					im = Image.open("./static/mymanage/goods/"+filename)
					# 缩放到375*375:
					im.thumbnail((375, 375))
					# 把缩放后的图像用jpeg格式保存:
					im.save("./static/mymanage/goods/"+filename, 'jpeg')
					# 缩放到220*220:
					im.thumbnail((220, 220))
					# 把缩放后的图像用jpeg格式保存:
					im.save("./static/mymanage/goods/m_"+filename, 'jpeg')
					# 缩放到75*75:
					im.thumbnail((75, 75))
					# 把缩放后的图像用jpeg格式保存:
					im.save("./static/mymanage/goods/s_"+filename, 'jpeg')
					photoname_big=list.picname #获取图片的名称
					photoname_small='s_'+photoname_big #获取图片的名称
					photoname_Min='m_'+photoname_big
					#执行图片删除，旧的图片
					os.remove("./static/mymanage/goods/"+photoname_small)
					os.remove("./static/mymanage/goods/"+photoname_big)
					os.remove("./static/mymanage/goods/"+photoname_Min)
			list.picname=filename
		list.save()
		context={"info":"修改成功！"}
		return render(request,"mymanage/info.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"mymanage/info.html",context)

def delete(request,uid):
	try:
		list=Goods.objects.get(id=uid)
		photoname_big=list.picname #获取图片的名称
		photoname_small='s_'+photoname_big #获取图片的名称
		photoname_Min='m_'+photoname_big
		list.delete()
		#执行图片删除
		os.remove("./static/mymanage/goods/"+photoname_small)
		os.remove("./static/mymanage/goods/"+photoname_big)
		os.remove("./static/mymanage/goods/"+photoname_Min)
		context={"info":"删除成功"}
		return render(request,"mymanage/info.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"mymanage/info.html",context)