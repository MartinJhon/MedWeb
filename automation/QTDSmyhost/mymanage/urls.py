from django.conf.urls import url

from mymanage.views import index,users,types,goods,oders,host

urlpatterns = [
	#管理主页面
	url(r'^$', index.index,name='mymanage_index'),

	# 后台管理员路由
	url(r'^login$', index.login, name="mymanage_login"),
	url(r'^dologin$', index.dologin, name="mymanage_dologin"),
	url(r'^logout$', index.logout, name="mymanage_logout"),
	#检索相片
	url(r'^findphoto$', index.findphoto,name='mymanage_index_findphoto'),

	#会员数据显示
	url(r'^user/(?P<pIndex>[0-9]+)$', users.index,name='mymanage_user_index'),
	#会员数据添加加载
	url(r'^user/add/$', users.add,name='mymanage_user_add'),
	#会员数据增加
	url(r'^user/insert/$', users.insert,name='mymanage_user_insert'),
	#会员数据修改加载
	url(r'^user/edit/(?P<uid>[0-9]+)$', users.edit,name='mymanage_user_edit'),
	#会员数据更新
	url(r'^user/upate/$', users.update,name='mymanage_user_update'),
	#会员数据删除
	url(r'^user/del/(?P<uid>[0-9]+)$', users.delete,name='mymanage_user_delete'),
	#重置会员密码
	url(r'^user/editpwd/(?P<uid>[0-9]+)$', users.editpawd,name='mymanage_user_editpawd'),
	#更新会员密码
	url(r'^user/upatepwd/$', users.updatepawd,name='mymanage_user_updatepawd'),
	#检索全部
	url(r'^user/findall/(?P<pIndex>[0-9]+)$', users.findall,name='mymanage_user_findall'),
	#检索条件
	url(r'^user/selfind/(?P<pIndex>[0-9]+)$', users.selfind,name='mymanage_user_selfind'),


	#商品数据显示
	url(r'^type/(?P<pIndex>[0-9]+)$', types.index,name='mymanage_type_index'),
	#商品数据添加加载
	url(r'^type/add/(?P<tid>[0-9]+)$', types.add,name='mymanage_type_add'),
	#商品数据增加
	url(r'^type/insert/$', types.insert,name='mymanage_type_insert'),
	#商品数据修改加载
	url(r'^type/edit/(?P<tid>[0-9]+)$', types.edit,name='mymanage_type_edit'),
	#商品数据更新
	url(r'^type/upate/$', types.update,name='mymanage_type_update'),
	#商品数据删除
	url(r'^type/del/(?P<tid>[0-9]+)$', types.delete,name='mymanage_type_delete'),
	#数据查询校验
	url(r'^type/checkdata/$', types.checkdata,name='mymanage_type_checkdata'),

	#商品数据显示
	url(r'^goods/(?P<pIndex>[0-9]+)$', goods.index,name='mymanage_goods_index'),
	#商品数据添加加载
	url(r'^goods/add/$', goods.add,name='mymanage_goods_add'),
	#商品数据增加
	url(r'^goods/insert/$', goods.insert,name='mymanage_goods_insert'),
	#商品数据修改加载
	url(r'^goods/edit/(?P<uid>[0-9]+)$', goods.edit,name='mymanage_goods_edit'),
	#商品数据更新
	url(r'^goods/upate/$', goods.update,name='mymanage_goods_update'),
	#商品数据删除
	url(r'^goods/del/(?P<uid>[0-9]+)$', goods.delete,name='mymanage_goods_delete'),

	#会员后台订单管理
	url(r'^orders$', oders.index, name="mymanage_orders_index"),
	url(r'^orders/(?P<pIndex>[0-9]+)$', oders.index, name="mymanage_orders_index"),
	url(r'^orders/detail/(?P<oid>[0-9]+)$', oders.detail, name="mymanage_orders_detail"),
	url(r'^orders/state$',oders.state, name="mymanage_orders_state"),

	#主机数据显示
	url(r'^host/(?P<pIndex>[0-9]+)$', host.index,name='mymanage_host_index'),
	#主机的添加模版加载
	url(r'^host/add/$', host.add,name='mymanage_host_add'),
	#主机数据增加
	url(r'^host/insert/$', host.insert,name='mymanage_host_insert'),
	#主机数据修改加载
	url(r'^host/edit/(?P<uid>[0-9]+)$', host.edit,name='mymanage_host_edit'),
	#主机数据更新
	url(r'^host/upate/$', host.update,name='mymanage_host_update'),
	#主机数据删除
	url(r'^host/del/(?P<uid>[0-9]+)$', host.delete,name='mymanage_host_delete'),
	#监控主机信息
	url(r'^host/monitor/$', host.monitor_list,name='mymanage_host_monitor'),
	#监控主机信息传送
	url(r'^host/monitor_data/$', host.monitor_data,name='mymanage_host_monitor_data'),

	#选择要监控的主机
	url(r'^host/monitor_find/(?P<uid>[0-9]+)$', host.monitor_find,name='mymanage_host_monitor_find'),
	#监控主机更新
	url(r'^host/monitor_update/$', host.monitor_update,name='mymanage_host_monitor_update'),
]