from django.shortcuts import render
from django.http import HttpResponse
from common.models import Users,Goods,Types,Orders,Detail
from datetime import datetime
import time
import random
from django.db.models import Q
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator

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

def add(request):
	#进行订单确认
	context=typelist(request)
	if 'shoplist' not in request.session:
		request.session['shoplist']={}
		context={'info':'没有购物信息'}
		return render(request,'myweb/goodslist/info2.html',context)
	getidlist=request.GET.get('ids','')
	if len(getidlist):
		getidlist=getidlist.split(',')
	else:
		context={'info':'没有购物信息'}
		return render(request,'myweb/goodslist/info2.html',context)

	shoplist=request.session['shoplist']	
	orderlist={}
	total = 0.0 #必须赋值，否则系统无法判断类型
	for i in getidlist:
		orderlist[i]=shoplist[i]
		total+=shoplist[i]['m']*shoplist[i]['price']
	request.session['total']= total
	request.session['orderlist']=orderlist
	return render(request,'myweb/goodslist/order.html',context)

def confirm(request):
	#进行二次确认
	context=typelist(request)
	return render(request,'myweb/goodslist/orderok.html',context)

def insert(request):
	#完全增加信息,增加订单信息
	context=typelist(request)
	try:
		stime=str(time.strftime("%y"))+str(time.strftime("%m"))+str(time.strftime("%d"))+"0000"
		stime=int(stime)
		count=Orders.objects.filter().count()
		stime+=count
		olist=Orders()
		vip=request.session['vipuser']
		#olist.id=int(stime)
		olist.uid=vip['id']
		olist.id=stime
		olist.linkman=request.POST.get('txt_name')
		olist.address=request.POST.get('txt_adrr')
		olist.code=request.POST.get('txt_po')
		olist.phone=request.POST.get('txt_phont')
		olist.addtime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		olist.total = request.session['total']
		olist.state = 0
		olist.save()
		#增加订单信息
		orderlist=request.session['orderlist']
		shoplist=request.session['shoplist']
		
		for i in orderlist.values():
			del shoplist[str(i['id'])]
			ulist=Detail()
			ulist.orderid=stime
			ulist.goodsid=i['id']
			ulist.name=i['goods']
			ulist.price=i['price']
			ulist.num=i['m']
			ulist.save()
		del request.session['orderlist']
		del request.session['total']
		request.session['shoplist']=shoplist
		context["info"]="订单添加成功！订单号："+str(olist.id)
		return render(request,'myweb/goodslist/orderS.html',context)
	except Exception as info:
		context["info"]="订单添加失败！"
		return render(request,'myweb/goodslist/orderS.html',context)

def showlist(request,pIndex=1):
	'''浏览信息'''
	#获取订单信息
	mod = Orders.objects
	mywhere=[]

	# 获取、判断并封装关keyword键搜索
	kw = request.session['vipuser']['name']
	kid = request.session['vipuser']['id']
	if kw:
		# 查询收件人和地址中只要含有关键字的都可以
		list = mod.filter(linkman=kw,uid=int(kid))
		mywhere.append("keyword="+kw)
		mywhere.append("kid="+str(kid))
	else:
		list = mod.filter()

	# 获取、判断并封装订单状态state搜索条件
	state = request.GET.get('state','')
	if state != '':
		list = list.filter(state=state)
		mywhere.append("state="+state)

	#执行分页处理
	pIndex = int(pIndex)
	page = Paginator(list,5) #以5条每页创建分页对象
	maxpages = page.num_pages #最大页数
	#判断页数是否越界
	if pIndex > maxpages:
		pIndex = maxpages
	if pIndex < 1:
		pIndex = 1
	list2 = page.page(pIndex) #当前页数据
	plist = page.page_range   #页码数列表

	# 遍历订单信息并追加 下订单人姓名信息
	for od in list2:
		user = Users.objects.only('name').get(id=od.uid)
		od.name = user.name

	#封装信息加载模板输出
	context = {"orderslist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
	return render(request,"myweb/orders/index.html",context)

def lookdetail(request,oid):
	''' 订单详情信息 '''
	try:
		# 加载订单信息
		orders = Orders.objects.get(id=oid)
		if orders != None:
			user = Users.objects.only('name').get(id=orders.uid)
			orders.name = user.name

		# 加载订单详情
		dlist = Detail.objects.filter(orderid=oid)
		# 遍历每个商品详情，从Goods中获取对应的图片
		for og in dlist:
			og.picname = Goods.objects.only('picname').get(id=og.goodsid).picname

		# 放置模板变量，加载模板并输出
		context = {'orders':orders,'detaillist':dlist}
		return render(request,"myweb/orders/detail.html",context)
	except Exception as err:
		print(err)
		context = {'info':'没有找到要修改的信息！'}
	return render(request,"myweb/info1.html",context)


def updatestate(request):
	''' 修改订单状态 '''
	try:
		oid = request.GET.get("oid",'0')
		ob = Orders.objects.get(id=oid)
		ob.state = request.GET['state']
		ob.save()
		context = {'info':'修改成功！'}
	except Exception as err:
		print(err)
		context = {'info':'修改失败！'}
	return render(request,"myweb/info1.html",context)