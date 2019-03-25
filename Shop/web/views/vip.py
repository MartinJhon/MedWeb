from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from common.models import Goods,Types,Orders,Detail,Users
from datetime import datetime


def loadinfo(request):
    '''公共信息加载，主要是为了显示页头的商品类别信息'''
    context = {}
    lists = Types.objects.filter(pid=0)
    context['typelist'] = lists
    return context

def viporders(request):
	'''个人中心，浏览订单信息'''
	context=loadinfo(request)
	#获取当前登陆者的订单信息,可能是多条订单,此处获取的odlist，是一个对象
	odlist=Orders.objects.filter(uid=request.session['vipuser']['id'])
	#遍历订单信息，查询对应的详情信息，订单详情中orderid对应订单id,一个订单可能有多条购买详情
	for od in odlist:
		delist=Detail.objects.filter(orderid=od.id)
		#遍历订单详情，获取对应的商品信息,并且把对应商品信息的图片放入
		for og in delist:
			ov=Goods.objects.only('picname').get(id=og.goodsid)
			og.picname=ov.picname
		od.detaillist=delist
	context['orderslist']=odlist
	return render(request,'web/viporders.html',context)


def odstate(request):
    ''' 修改订单状态 '''
    try:
        oid = request.GET.get("oid",'0')
        ob = Orders.objects.get(id=oid)
        ob.state = request.GET['state']
        ob.save()
        return redirect(reverse('vip_orders'))
    except Exception as err:
        print(err)
        return HttpResponse("订单处理失败！")

def register(request):
    ''' 跳转注册界面 '''
    return render(request,'web/vip/register.html')

def vipadd(request):
    ''' 写入注册信息界面 '''
    try:
        ob=Users()
        ob.username=request.POST['username']
        ob.password=request.POST['password']
        ob.repassword=request.POST['repassword']
        if ob.password !=ob.repassword:
            context={"info":"两次密码不符"}
        else:
            #获取密码并md5
            import hashlib
            m = hashlib.md5()
            m.update(bytes(ob.password,encoding="utf8"))
            ob.password=m.hexdigest()  #调用hexdigest方法对密码进行加密
            ob.save()
            context={'info':'注册成功,请登陆！'}
            return render(request,'web/login.html',context)
    except Exception as err:
        context={"info":'注册失败,该账户已存在！'}
    return render(request,'web/vip/register.html',context)


def vipindex(request,vid):
    '''会员中心信息浏览'''
    vipuser=Users.objects.get(id=vid)
    context={'vipuser':vipuser}
    return render(request,'web/vip/vipindex.html',context)

def vipedit(request,vid):
    '''加载编辑界面'''
    try:
        vipedit = Users.objects.get(id=vid)
        context={"vipedit":vipedit}
        return render(request,'web/vip/vipedit.html',context)
    except Exception as err:
        context={"info":'删除失败'}
    return render(request,'web/vip/info.html',context)


def vipupdate(request,vid):
    '''会员中心信息浏览'''
    try:
        ob=Users.objects.get(id=vid)
        ob.name = request.POST['name']
        ob.sex = request.POST['sex']
        ob.address = request.POST['address']
        ob.code = request.POST['code']
        ob.phone = request.POST['phone']
        ob.email = request.POST['email']
        ob.state = request.POST['state']
        ob.save()
        context = {'info': '修改成功'}
    except Exception as err:
        context={"info":'修改失败'}
    return render(request,'web/vip/info.html',context)


def vipreset(request,vid):
	'''加载重置密码界面'''
	try:
		ob = Users.objects.get(id=vid)
		context={"user":ob}
		return render(request,'web/vip/vipreset.html',context)
	except Exception as err:
		context={"info":'没有找到要修改的信息'}
	return render(request,'web/vip/info.html',context)

def vippassword(request,vid):
	ob=Users.objects.get(id=vid)
	ob.password=request.POST['password']
	ob.password=request.POST['password']
	ob.repassword=request.POST['repassword']
	if ob.password !=ob.repassword:
		context={"info":"两次密码不符"}
	else:
		import hashlib
		m = hashlib.md5()
		m.update(bytes(ob.password,encoding="utf8"))
		ob.password=m.hexdigest()  #调用hexdigest方法对密码进行加密
		ob.save()
		context={"info":'重置密码成功'}
	return render(request,'myadmin/info.html',context)
