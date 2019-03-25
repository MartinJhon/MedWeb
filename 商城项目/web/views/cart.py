from django.shortcuts import render
from django.http import HttpResponse
#导入用户类和重定向跳转
from django.shortcuts import redirect
from django.urls import reverse
from common.models import Types,Goods

# Create your views here.

#公共信息加载函数,加载商品信息一级类别
def loadinfo(request):
    lists=Types.objects.filter(pid=0) #此处需要使用filter，因为如果使用get准确判断，返回多个值是会报错
    context={'typelist':lists}
    return context


def index(request):
	'''浏览购物车'''
	context=loadinfo(request)
	#判断购物车里有没有商品，如果没有，添加一个空的字典
	if 'shoplist' not in request.session:
		request.sessoin['shoplist']={}
	return render(request,'web/cart.html',context)


def add(request,gid):
	'''添加购物车'''
	goods=Goods.objects.get(id=gid)
	shop=goods.toDict()
	#获取购物车内商品数量，默认是1,此时shop是一个字典，相当于在字典shop中增加了一对数据
	shop['m']=int(request.POST.get('m',1))
	#从状态保持中，获取之前的shoplist字典，没有默认一个空字典
	shoplist=request.session.get('shoplist',{})
	#判断购物车中是否已存在要购买的商品
	if gid in shoplist:
	#累加购买量，以gid为键获取一条商品信息，再以m为键获取此条数据中的购买数量，累加
		shoplist[gid]['m'] +=shop['m']
	else:
	#购物车没有该商品，作为新商品放入，即在shoplist字典中增加了一个键为gid，值为shop的一条字典数据
		shoplist[gid]=shop
	#将购物车中商品信息放入session
	request.session['shoplist']=shoplist
	#重定向查看购物车
	return redirect(reverse('cart_index'))


def delete(request,gid):
	'''删除购物车商品'''
	#取出购物车，也可以写为shoplist=request.session.get('shoplist')
	shoplist=request.session['shoplist']
	del shoplist[gid]
	#将购物车中商品信息放入session,删除后的再放回
	request.session['shoplist']=shoplist
	return redirect(reverse('cart_index'))


def clear(request):
	'''清空购物车'''
	#清空的原理就是给request.session['shoplist']赋值为空
	request.session['shoplist']={}
	return redirect(reverse('cart_index'))


def change(request):
	'''更改购物车信息'''
	shoplist=request.session['shoplist']
	#获取回传的商品id
	shopid=request.GET.get('gid',0)
	#获取回传的商品数量
	num = int(request.GET.get('num',1))
	if num<1:
		num=1
	#修改回传的商品数量
	shoplist[shopid]['m'] = num
	request.session['shoplist']=shoplist
	return redirect(reverse('cart_index'))
