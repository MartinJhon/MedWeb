from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

from common.models import Users  # 导入models类
from django.core.paginator import Paginator  # 导入分页类
from django.db.models import Q


# Create your views here.


def index(request, pIndex):
    '''浏览信息'''
    mod = Users.objects
    mywhere = []  # 定义一个用于存放搜索条件列表
    kw = request.GET.get("keyword", None)
    if kw:
        # 查询账号中只要含有关键字的都可以
        list = mod.filter(Q(username__contains=kw))
        mywhere.append("keyword=" + kw)
    else:
        list = mod.filter()

    # 获取、判断并封装用户状态state搜索条件
    state = request.GET.get('state', '')
    if state != '':
        list = list.filter(state=state)
        mywhere.append("state=" + state)

    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list, 5)  # 以5条每页创建分页对象
    maxpages = page.num_pages  # 最大页数
    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 当前页数据
    plist = page.page_range  # 页码数列表

    # 封装信息加载模板输出
    context = {"userslist": list2, 'plist': plist, 'pIndex': pIndex, 'mywhere': mywhere, }
    return render(request, "myadmin/users/index.html", context)


def add(request):
    '''加载添加页面'''
    return render(request, 'myadmin/users/add.html')


def insert(request):
    '''添加数据'''
    try:
        ob = Users()
        ob.username = request.POST['username']
        ob.name = request.POST['name']

        ob.password = request.POST['password']
        ob.repassword = request.POST['repassword']
        if ob.password != ob.repassword:
            context = {"info": "两次密码不符"}
        else:
            # 获取密码并md5
            import hashlib
            m = hashlib.md5()
            m.update(bytes(ob.password, encoding="utf8"))
            ob.password = m.hexdigest()  # 调用hexdigest方法对密码进行加密
            ob.sex = request.POST['sex']
            ob.address = request.POST['address']
            ob.code = request.POST['code']
            ob.phone = request.POST['phone']
            ob.email = request.POST['email']
            ob.state = 1
            ob.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间
            ob.save()
            context = {'info': '添加成功'}
    except Exception as err:
        context = {"info": '添加失败'}
    return render(request, 'myadmin/info.html', context)


def delete(request, uid):
    '''删除数据'''
    try:
        ob = Users.objects.get(id=uid)
        ob.delete()
        context = {'info': '删除成功'}
    except Exception as err:
        context = {"info": '删除失败'}
    return render(request, 'myadmin/info.html', context)


def edit(request, uid):
    '''加载编辑页面'''
    try:
        ob = Users.objects.get(id=uid)
        context = {"user": ob}
        return render(request, 'myadmin/users/edit.html', context)
    except Exception as err:
        context = {"info": '删除失败'}
    return render(request, 'myadmin/info.html', context)


def update(request, uid):
    '''修改数据'''
    try:
        ob = Users.objects.get(id=uid)
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
        context = {"info": '修改失败'}
    return render(request, 'myadmin/info.html', context)


def reset(request, uid):
    '''加载重置密码界面'''
    try:
        ob = Users.objects.get(id=uid)
        context = {"user": ob}
        return render(request, 'myadmin/users/reset.html', context)
    except Exception as err:
        context = {"info": '没有找到要修改的信息'}
    return render(request, 'myadmin/info.html', context)


def password(request, uid):
    ob = Users.objects.get(id=uid)
    ob.password = request.POST['password']
    ob.password = request.POST['password']
    ob.repassword = request.POST['repassword']
    if ob.password != ob.repassword:
        context = {"info": "两次密码不符"}
    else:
        import hashlib
        m = hashlib.md5()
        m.update(bytes(ob.password, encoding="utf8"))
        ob.password = m.hexdigest()  # 调用hexdigest方法对密码进行加密
        ob.save()
        context = {"info": '重置密码成功'}
    return render(request, 'myadmin/info.html', context)

