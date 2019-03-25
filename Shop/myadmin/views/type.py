from django.shortcuts import render
from django.http import HttpResponse
from common.models import Types  # 导入models类
from django.core.paginator import Paginator  # 导入分页类
from django.db.models import Q  # 导入查询分类


# Create your views here.

def index(request, pIndex):
    '''浏览信息'''
    # list = Types.objects.all() #此处不能这么写，因为还需要做一个排序
    list = Types.objects.extra(select={'_has': 'concat(path,id)'}).order_by(
        '_has')  # '_has':'concat(path,id)',这的意思是给后者起别名再排序
    mywhere = []  # 定义一个用于存放搜索条件列表

    kw = request.GET.get("keyword", None)
    if kw:
        # 查询账号中只要含有关键字的都可以
        list2 = list.filter(Q(name__contains=kw))
        mywhere.append("keyword=" + kw)
    else:
        list2 = list.filter()

    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list2, 7)  # 以5条每页创建分页对象
    maxpages = page.num_pages  # 最大页数
    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list3 = page.page(pIndex)  # 当前页数据
    plist = page.page_range  # 页码数列表

    # 遍历查询结果，添加一个类别缩进效果属性,此处的效果是有一个‘，’输出四个‘.’
    for i in list3:
        i.pname = ' . . . .' * (i.path.count(',') - 1)  # pname是在此处的父类别名称,此处相当于每循环一次给list添加了一个pname的字段和属性值
    # 封装信息加载模板输出
    context = {"tlist": list3, 'plist': plist, 'pIndex': pIndex, 'mywhere': mywhere, }
    return render(request, "myadmin/type/index.html", context)


def add(request, tid):
    '''加载添加页面'''
    # 获取父类别信息
    if tid == '0':
        context = {'pid': 0, 'path': '0,', 'name': '跟类别'}
    else:
        ob = Types.objects.get(id=tid)
        context = {'pid': ob.id, 'path': ob.path + str(ob.id) + ',', 'name': ob.name}
    return render(request, 'myadmin/type/add.html', context)


def insert(request):
    '''添加数据'''
    try:
        ob = Types()
        ob.name = request.POST['name']
        ob.pid = request.POST['pid']
        ob.path = request.POST['path']
        ob.save()
        context = {'info': '添加成功'}
    except Exception as err:
        context = {"info": '添加失败'}
    return render(request, 'myadmin/info.html', context)


def delete(request, tid):
    '''删除数据'''
    try:
        ob = Types.objects.get(id=tid)
        ob.delete()
        context = {'info': '删除成功'}
    except Exception as err:
        context = {"info": '删除失败'}
    return render(request, 'myadmin/info.html', context)


def edit(request, tid):
    '''加载编辑页面'''
    try:
        type = Types.objects.get(id=tid)
        context = {"type": type}
        return render(request, 'myadmin/type/edit.html', context)
    except Exception as err:
        context = {"info": '删除失败'}
    return render(request, 'myadmin/info.html', context)


def update(request, tid):
    '''修改数据'''
    try:
        ob = Types.objects.get(id=tid)
        ob.name = request.POST['name']
        ob.save()
        context = {'info': '修改成功'}
    except Exception as err:
        context = {"info": '修改失败'}
    return render(request, 'myadmin/info.html', context)