from django.shortcuts import render
from django.http import HttpResponse
#导入用户类和重定向跳转
from django.shortcuts import redirect
from django.urls import reverse
from common.models import Users,Types,Goods,Orders
#导入分页对象
from django.core.paginator import Paginator

# Create your views here.

#公共信息加载函数,加载商品信息一级类别
def loadinfo(request):
    lists=Types.objects.filter(pid=0) #此处需要使用filter，因为如果使用get准确判断，返回多个值是会报错
    context={'typelist':lists}
    return context

def index(request):
    '''项目前台首页'''
    #调用函数，此处的context是自定义的变量，可任意命名，等于每个方法开头都获取了一下pid=0的数据进行封装，并赋值给context
    context=loadinfo(request)
    best_sellers=Goods.objects.order_by('-clicknum')[0:5]
    digital=Goods.objects.filter(typeid__in=Types.objects.only('id').filter(pid=2),state=1).order_by('-addtime')[0:4]
    clothes=Goods.objects.filter(typeid__in=Types.objects.only('id').filter(pid=1),state=1).order_by('-addtime')[0:4]
    context['best_sellers']=best_sellers
    context['digital']=digital
    context['clothes']=clothes
    return render(request,'web/index.html',context)


def lists(request,pIndex=1):
    #关于此处的查询，老师有其他的写法，运用?tid={{type.id}},用tid = int(request.GET.get("tid",0))接收
    '''项目列表页'''
    context=loadinfo(request)
    #查询商品信息
    mod=Goods.objects
    mywhere=[] #定义一个用于存放搜索条件列表，暂时这个功能暂时没写

    #获取请求查询的对象，即获取base中?tid={{type.id}}回传的数据
    tid = int(request.GET.get("tid",0))
    if tid > 0:
        #只查询表中一个字段（id），并且做过滤pid=tid，only（id）可不写
        list=mod.filter(typeid__in=Types.objects.only('id').filter(pid=tid))
        mywhere.append('tid='+str(tid))
    else:
        #查询Goods表的所有数据
        list=mod.filter()

    pIndex = int(pIndex)
    #将数据进行分页
    page=Paginator(list,4)
    maxpages = page.num_pages #最大页数
    #判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    #获取当前选择的某一页
    list2=page.page(pIndex)
    #获取数据一共被分了多数页
    plist=page.page_range

    #context在这是类似一个字典，向其增加值为list的键，原有的不变,等于向字典内新增,新增封装各自条件
    context['goodslist']=list2
    context['plist']=plist
    context['pIndex']=pIndex
    context['mywhere']=mywhere
    return render(request,'web/list.html',context)


def detail(request,gid):
    '''项目详情页'''
    context=loadinfo(request)
    #获取单个商品信息
    ob=Goods.objects.get(id=gid)
    #点击量加1,保存
    ob.clicknum += 1
    ob.save()
    context['goods']=ob
    return render(request,'web/detail.html',context)


def login(request):
    '''会员登录表单'''
    return render(request,'web/login.html')

def dologin(request):
    '''会员执行登录'''
    # 校验验证码，此处的验证码使用的是url地址为 'myadmin_verify'的，即后台视图中写的验证码，按理应单独写
    verifycode = request.session['verifycode']
    code = request.POST['code']
    if verifycode != code:
        context = {'info':'验证码错误！'}
        return render(request,"web/login.html",context)
    try:
        #根据账号获取登录者信息
        user = Users.objects.get(username=request.POST['username'])

        #判断当前用户是否是后台管理员用户
        if user.state == 0 or user.state == 1:
            # 验证密码
            import hashlib
            m = hashlib.md5()
            m.update(bytes(request.POST['password'],encoding="utf8"))
            if user.password == m.hexdigest():
                # 此处登录成功，user.toDict() 是一个字典形数据，将其放入到session中，此时获取一个vipuser的字典
                request.session['vipuser'] = user.toDict()

                return redirect(reverse('index'))
            else:
                context = {'info':'登录密码错误！'}
        else:
            context = {'info':'此用户为非法用户！'}
    except:
        context = {'info':'登录账号错误！'}
    return render(request,"web/login.html",context)



def logout(request):
    '''会员退出'''
    # 清除登录的session信息
    del request.session['vipuser']

    # 跳转登录页面（url地址改变）
    return redirect(reverse('login'))
