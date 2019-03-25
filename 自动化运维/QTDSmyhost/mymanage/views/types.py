from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from common.models import Types,Goods
from django.core.paginator import Paginator

from django.db.models import Q
# Create your views here.

def index(request,pIndex):
	#显示会员信息列表
	ulist=Types.objects.extra(select={'_has':'concat(path,id)'}).order_by('_has') #获取所有的记录，并且排序
	for i in ulist:
		i.parm='. . . .'*(i.path.count(',')-1)
	p = Paginator(ulist, 10) #分页显示，一页10条
	if pIndex == '':
		pIndex = '1'
	pIndex = int(pIndex)
	list = p.page(pIndex) #获取索引页对应的数据对象
	plist = p.page_range #获取分页索引所有对象
	context={'typelist': list, 'plist': plist, 'pIndex': pIndex,'plist_len':len(plist)}
	return render(request,"mymanage/types/index.html",context)

def add(request,tid):
	#加载商品类别增加表单
	if tid == '0':
		context={'pid':0,'path':'0,','name':'顶级目录'}
	else:
		ulist=Types.objects.get(id=tid)
		context={'pid':ulist.id,'path':ulist.path,'name':ulist.name}
	return render(request,"mymanage/types/add.html",context)

def insert(request):
	try:
		#新增商品类别信息
		list=Types()
		list.name=request.POST['txt_name']
		list.pid=request.POST['txt_pid']
		list.path=request.POST['txt_path']+request.POST['txt_pid']+','
		list.save()
		info="保存成功！"
		context={"info":info}
		return render(request,"mymanage/info.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"mymanage/info.html",context)

def edit(request,tid):
	try:
		#加载修改商品类别的表单
		ulist=Types.objects.get(id=tid)
		context={"list":ulist}
		return render(request,"mymanage/types/edit.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"mymanage/info.html",context)

def update(request):
	try:
		#修改商品类别信息
		list=Types.objects.get(id=request.POST['txt_id'])
		list.name=request.POST['txt_name']
		list.save()
		info="修改成功！"
		context={"info":info}
		return render(request,"mymanage/info.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"mymanage/info.html",context)

def delete(request,tid):
	try:
		#删除商品类别信息
		ulist=Types.objects.get(id=tid)
		#检查是否存在子类
		clist=Types.objects.filter(path__contains=tid).count()
		if clist>0:
			context={'info':'不能删除，存在子类别！'}
			return render(request,"mymanage/info.html",context)
		typelist=[]
		utylist=Types.objects.filter(Q(id=int(tid))|Q(path__contains=int(tid)))
		for i in utylist:
			typelist.append(i.id)
		plist=Goods.objects.filter(typeid__in=typelist).count()
		if plist>0:
			context={'info':'不能删除，类别下存在商品信息！'}
			return render(request,"mymanage/info.html",context)
		ulist.delete()
		context={"info":"删除成功！"}
	except Exception as info:
		context={"info":info}
	return render(request,"mymanage/info.html",context)

def checkdata(request):
	pass
