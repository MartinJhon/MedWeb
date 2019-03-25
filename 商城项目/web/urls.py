from django.conf.urls import url
from web.views import index,cart,orders,vip


urlpatterns = [
    #前台首页
    url(r'^$',index.index,name='index'), #首页
    url(r'^list$',index.lists,name='list'), #列表
    url(r'^list/(?P<pIndex>[0-9]+)$',index.lists,name='list'), #列表，回传页码参数
    url(r'^detail/(?P<gid>[0-9]+)$',index.detail,name='detail'), #详情

    #会员登陆修改路由
    url(r'^login$', index.login, name="login"),
    url(r'^dologin$', index.dologin, name="dologin"),
    url(r'^logout$', index.logout, name="logout"),

    # 购物车路由
    url(r'^cart$', cart.index,name='cart_index'),
    url(r'^cart/add/(?P<gid>[0-9]+)$', cart.add,name='cart_add'),
    url(r'^cart/del/(?P<gid>[0-9]+)$', cart.delete,name='cart_del'),
    #清空
    url(r'^cart/clear$', cart.clear,name='cart_clear'),
    #修改
    url(r'^cart/change$', cart.change,name='cart_change'),

    #订单处理
    url(r'^orders/add$', orders.add,name='orders_add'), #订单的表单页
    url(r'^orders/confirm$', orders.confirm,name='orders_confirm'), #订单确认页
    url(r'^orders/insert$', orders.insert,name='orders_insert'), #执行订单添加操作

    # 会员中心
    url(r'^vip/orders$', vip.viporders,name='vip_orders'), #会员中心我的订单
    url(r'^vip/odstate$', vip.odstate,name='vip_odstate'), #修改订单状态（确认收货）

    #会员注册
    url(r'^vip/register$', vip.register,name='vip_register'),
    url(r'^vip/vipadd$', vip.vipadd,name='vip_add'),

    #会员中心信息浏览
    url(r'^vip/vipindex/(?P<vid>[0-9]+)$', vip.vipindex,name='vip_index'),
    url(r'^vip/vipedit/(?P<vid>[0-9]+)$', vip.vipedit,name='vip_edit'),
    url(r'^vip/vipupdate/(?P<vid>[0-9]+)$',vip.vipupdate,name='vip_update'),
    url(r'^vip/vipreset/(?P<vid>[0-9]+)$',vip.vipreset,name='vip_reset'),
    url(r'^vip/vippassword/(?P<vid>[0-9]+)$',vip.vippassword,name='vip_password'),


]
