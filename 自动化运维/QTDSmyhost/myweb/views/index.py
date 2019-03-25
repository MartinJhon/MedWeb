from django.shortcuts import render
from django.http import HttpResponse
from common.models import Users,Goods,Types
from django.core.paginator import Paginator
from PIL import Image
from datetime import datetime
import time,os
from django.db.models import Q
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
# Create your views here.
def index(request,pIndex=0):
	#主页显示
	try:
		utype=Types.objects.filter(pid=0)
		mywhere=[] #定义一个用于存放搜索条件列表
		txtname=request.GET.get("txt_fname",None)
		if txtname==None:
			txtname=request.GET.get("txt_name",None)
			
		if txtname==None:
			ulist=Goods.objects.filter().order_by("-addtime") #获取所有的记录
		else:
			ulist=Goods.objects.filter(goods__contains=txtname).order_by("-addtime") #获取所有的记录
			mywhere.append("txt_fname="+txtname)
		
		if pIndex == '':
			pIndex = '1'

		p = Paginator(ulist, 10) #分页显示，一页10条
		maxpages = p.num_pages #最大页数
		if pIndex<1:
			pIndex=1
		elif pIndex>maxpages:
			pIndex=maxpages
		pIndex = int(pIndex)
		list = p.page(pIndex) #获取索引页对应的数据对象
		plist = p.page_range #获取分页索引所有对象
		context={'goodslist': list, 'plist': plist, 'pIndex': pIndex,'plist_len':len(plist),'mywhere':mywhere,'maxpages':maxpages,'utype':utype}
		return render(request,"myweb/index.html",context)
	except Exception as info:
		context={'info':info}
		return render(request,"myweb/info.html",context)

def index_list(request,pIndex):
	#主页分页显示
	try:
		utype=Types.objects.filter(pid=0)
		mywhere=[] #定义一个用于存放搜索条件列表
		txtname=request.GET.get("txt_fname",None)
		if txtname==None:
			ulist=Goods.objects.filter().order_by("-addtime") #获取所有的记录
		else:
			ulist=Goods.objects.filter(goods__contains=txtname).order_by("-addtime") #获取所有的记录
			mywhere.append("txt_fname="+txtname)
		
		if pIndex == '':
			pIndex = '1'

		p = Paginator(ulist, 10) #分页显示，一页10条
		maxpages = p.num_pages #最大页数
		if int(pIndex)<1:
			pIndex=1
		elif int(pIndex)>maxpages:
			pIndex=maxpages
		pIndex = int(pIndex)
		list = p.page(pIndex) #获取索引页对应的数据对象
		plist = p.page_range #获取分页索引所有对象
		print(mywhere)
		context={'goodslist': list, 'plist': plist, 'pIndex': pIndex,'plist_len':len(plist),'mywhere':mywhere,'maxpages':maxpages,'utype':utype}
		return render(request,"myweb/index.html",context)
	except Exception as info:
		context={'info':info}
		return render(request,"myweb/info.html",context)

def Type_list(request,pIndex):
	#类别商品分页显示
	try:
		utype=Types.objects.filter(pid=0)
		mywhere=[] #定义一个用于存放搜索条件列表
		tyid=[]#顶一个类别id列表
		txtname=request.GET.get("txt_fname",None)
		Typeid=int(request.GET.get('tid',0))
		if txtname==None:
			if Typeid!=0:
				tlist=Types.objects.filter(Q(id=Typeid)|Q(path__contains=Typeid))
				for i in tlist:
					tyid.append(i.id)
				ulist=Goods.objects.filter(typeid__in=tyid).order_by("-addtime") #获取所有的记录
			else:
				ulist=Goods.objects.filter().order_by("-id") #获取所有的记录
		else:
			if Typeid!=0:
				tlist=Types.objects.filter(Q(id=Typeid)|Q(path__contains=Typeid))
				for i in tlist:
					tyid.append(i.id)
				ulist=Goods.objects.filter(goods__contains=txtname,typeid__in=tyid).order_by("-addtime") #获取所有的记录
				mywhere.append("txt_fname="+txtname)
			else:
				ulist=Goods.objects.filter(goods__contains=txtname).order_by("-addtime") #获取所有的记录
				mywhere.append("txt_fname="+txtname)
		
		if pIndex == '':
			pIndex = '1'

		p = Paginator(ulist, 10) #分页显示，一页10条
		maxpages = p.num_pages #最大页数
		if int(pIndex)<1:
			pIndex=1
		elif int(pIndex)>maxpages:
			pIndex=maxpages
		pIndex = int(pIndex)
		list = p.page(pIndex) #获取索引页对应的数据对象
		plist = p.page_range #获取分页索引所有对象
		print(mywhere)
		context={'goodslist': list, 'plist': plist, 'pIndex': pIndex,'plist_len':len(plist),'mywhere':mywhere,'maxpages':maxpages,'utype':utype}
		return render(request,"myweb/index.html",context)
	except Exception as info:
		context={'info':info}
		return render(request,"myweb/info.html",context)

