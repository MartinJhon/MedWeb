from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from common.models import Goods,Types,Orders,Detail
from datetime import datetime

# 公共信息加载
def loadinfo(request):
    '''公共信息加载'''
    context = {}
    lists = Types.objects.filter(pid=0)
    context['typelist'] = lists
    return context

def add(request):
    '''下订单第一步：订单表单'''
    context = loadinfo(request)
    # 获取要结算商品的id号
    ids = request.GET.get("ids",'')
	#判断长度是不是0，即有没有商品
    if len(ids) == 0:
        context = {"info":"请选择要结算的商品！"}
        return render(request,"web/ordersinfo.html",context)
	#如果有商品，获取id号，用把id号用，隔开，即把商品id隔开变为一个列表
    gidlist = ids.split(',')

    # 从购物车获取要结算所有商品，并放入到orderslist中，并且累计总金额
	#获取购物车信息
    shoplist = request.session['shoplist']
    orderslist = {}
    total = 0.0
	#遍历选择的商品id，将购物车中对应的商品id的值以gid为键放入orderslist字典中，并且累加对应id的商品价格
    for gid in gidlist:
        orderslist[gid] = shoplist[gid]
        total += shoplist[gid]['price']*shoplist[gid]['m']
    # 将这些信息放入到session中
    request.session['orderslist'] = orderslist
    request.session['total'] = total
    return render(request,"web/ordersadd.html",context)


#过渡，跳到确认页
def confirm(request):
    context = loadinfo(request)
    return render(request,"web/ordersconfirm.html",context)


def insert(request):
    context = loadinfo(request)
    try:
        # 执行订单信息添加操作
        od = Orders()
        od.uid = request.session['vipuser']['id'] #当前登录者的id号
        od.linkman = request.POST.get('linkman')
        od.address = request.POST.get('address')
        od.code = request.POST.get('code')
        od.phone = request.POST.get('phone')
        od.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.total = request.session['total']
        od.state = 0
        od.save()

        # 执行订单详情添加
        orderslist = request.session['orderslist']
        shoplist = request.session['shoplist']
		#orderslist是一个大字典，以商品id为键对应很多值，这些值是一条条字典形式的商品信息
        for shop in orderslist.values():
			#删除购物车里已购买的数据，shop本身是个字典包含商品信息，取出商品的id，删除购物车里对应商品id的数据
            del shoplist[str(shop['id'])]
            ov = Detail()
            ov.orderid = od.id #od.id是订单号
            ov.goodsid = shop['id']
            ov.name = shop['goods']
            ov.price = shop['price']
            ov.num = shop['m']
            ov.save()
        del request.session['orderslist']
        del request.session['total']
        request.session['shoplist'] = shoplist
        context = {"info":"订单添加成功！订单号："+str(od.id)}
        return render(request,"web/ordersinfo.html",context)
    except Exception as err:
        print(err)
        context = {"info":"订单添加失败，请稍后再试！"}
        return render(request,"web/ordersinfo.html",context)
