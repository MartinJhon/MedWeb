from django.conf.urls import url
from myweb.views import index,register,list,car,order

urlpatterns = [
	#首页显示及索引
    url(r'^$', index.index,name='index'),
    url(r'^indexlist/(?P<pIndex>[0-9]+)$', index.index_list,name='myweb_index_list'),
    url(r'^Typelist/(?P<pIndex>[0-9]+)$', index.Type_list,name='myweb_Type_list'),

    #会员登录及注册
    url(r'^register/$', register.register,name='myweb_register'),
    url(r'^logon/$', register.logon,name='myweb_logon'),
    url(r'^reguser/$', register.reguser,name='myweb_reguser'),
    url(r'^insert/$', register.insereguser,name='myweb_insereguser'),
    url(r'^exitweb/$', register.exitweb,name='myweb_exitweb'),
    url(r'^editvip/(?P<uid>[0-9]+)$', register.editvip,name='myweb_editvip'),
    url(r'^updatevip/$', register.updatevip,name='myweb_updatevip'),
    url(r'^editvpawd/(?P<uid>[0-9]+)$', register.editvpawd,name='myweb_editvpawd'),
    url(r'^updatevpawd/$', register.updatevpawd,name='myweb_updatevpawd'),

    #产品显示
    url(r'^list/(?P<uid>[0-9]+)$', list.list,name='myweb_list'),
    url(r'^list/love(?P<uid>[0-9]+)$', list.love,name='myweb_love'),

    #购物车
    url(r'^car$', car.index,name='myweb_car_index'),
    url(r'^car/addcar/(?P<gid>[0-9]+)$', car.addcar,name='myweb_car_addcar'),
    url(r'^car/delcar/(?P<gid>[0-9]+)$', car.delcar,name='myweb_car_delcar'),
    url(r'^car/clearcar$', car.clearcar,name='myweb_car_clearcar'),
    url(r'^car/updatecar$', car.updatecar,name='myweb_car_updatecar'),

    #订单
    url(r'^order/add$', order.add,name='myweb_order_add'),
    url(r'^order/confirm$', order.confirm,name='myweb_order_confirm'),
    url(r'^order/insert$', order.insert,name='myweb_order_insert'),

    #个人中心
    url(r'^order/showlist$', order.showlist,name='myweb_order_showlist'),
    url(r'^order/showlist/(?P<pIndex>[0-9]+)$', order.showlist,name='myweb_order_showlist'),
    url(r'^order/lookdetail/(?P<oid>[0-9]+)$', order.lookdetail,name='myweb_order_lookdetail'),
    url(r'^order/updatestate$', order.updatestate,name='myweb_order_updatestate'),    
]