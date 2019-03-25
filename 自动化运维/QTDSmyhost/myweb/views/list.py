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

#获取产品类别索引
def typelist(request):
	try:
		context={}
		utype=Types.objects.filter(pid=0)
		context['utype']=utype
		return context
	except Exception as info:
		context={'info':info}
		return render(request,"myweb/info.html",context)

#获取单品			
def list(request,uid):
	try:
		context=typelist(request)
		ulist=Goods.objects.get(id=uid)
		utype=Types.objects.get(id=ulist.typeid)
		context['list']=ulist
		context['typename']=utype.name
		return render(request,"myweb/vipuser/list.html",context)
	except Exception as info:
		context={'info':info}
		return render(request,"myweb/info.html",context)	
#喜欢点赞
def love(request,uid):
	try:
		context=typelist(request)
		ulist=Goods.objects.get(id=uid)
		ulist.clicknum+=1
		ulist.save()
		utype=Types.objects.get(id=ulist.typeid)
		context['list']=ulist
		context['typename']=utype.name
		return render(request,"myweb/vipuser/list.html",context)
	except Exception as info:
		context={'info':info}
		return render(request,"myweb/info.html",context)