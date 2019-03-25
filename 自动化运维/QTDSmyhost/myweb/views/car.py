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

def index(request):
	#购物车浏览
	context=typelist(request)
	if 'shoplist' not in request.session:
		request.session['shoplist']={}
	return render(request,"myweb/goodslist/car.html",context)

def addcar(request,gid):
	#购物车增加
	'''在购物车中放入商品信息'''
	#获取要放入购物车中的商品信息
	goods = Goods.objects.get(id=gid)
	shop = goods.toDict();
	shop['m'] = 1  #添加一个购买量属性m,每次加一个
	#从session获取购物车信息，没有默认空字典
	shoplist = request.session.get('shoplist',{})
	#判断此商品是否在购物车中
	if gid in shoplist:
		#商品数量加
		shoplist[gid]['m']+=shop['m']
	else:
		#新商品添加
		shoplist[gid]=shop

	#将购物车信息放回到session
	request.session['shoplist'] = shoplist

	#重定向到浏览购物车页
	return redirect(reverse('myweb_car_index'))

def delcar(request,gid):
	#购物车删除
	'''删除一个商品'''
	shoplist = request.session['shoplist']
	del shoplist[gid]
	request.session['shoplist'] = shoplist
	return redirect(reverse('myweb_car_index'))

def clearcar(request):
	#清除购物车
	'''清空购物车'''
	context = typelist(request)
	request.session['shoplist'] = {}
	return render(request,"myweb/goodslist/car.html",context)

def updatecar(request):
	#更改购物车
	'''更改购物车中的商品信息'''
	shoplist = request.session['shoplist']
	#获取信息
	shopid = request.GET.get('gid','0')
	num = int(request.GET['num'])
	if num<1:
		num = 1
	shoplist[shopid]['m'] = num #更改商品数量
	request.session['shoplist'] = shoplist
	return redirect(reverse('myweb_car_index'))