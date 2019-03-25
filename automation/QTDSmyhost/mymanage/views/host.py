from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from common.models import Goods,Types,Host
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse

from PIL import Image
from datetime import datetime
import time,os,json
import random
from django.db.models import Q
import paramiko
import re
# Create your views here.

def index(request,pIndex):
	#显示会员信息列表
	mywhere=[] #定义一个用于存放搜索条件列表
	txtname=request.GET.get("txt_fname",None)
	if txtname==None:
		ulist=Host.objects.all() #获取所有的记录
	else:
		ulist=Host.objects.filter(name__contains=txtname) #获取所有的记录
		mywhere.append("txt_fname="+txtname)

	txtstate=request.GET.get("mysel2",None)

	if txtstate=='1':
		ulist=ulist.filter(state=1)
		mywhere.append("mysel2="+txtstate)
	elif txtstate=='2':
		ulist=ulist.filter(state=2)
		mywhere.append("mysel2="+txtstate)
	elif txtstate==3:
		ulist=ulist.filter(state=3)
		mywhere.append("mysel2="+txtstate)

	p = Paginator(ulist, 10) #分页显示，一页10条
	if pIndex == '':
		pIndex = '1'
	pIndex = int(pIndex)
	list = p.page(pIndex) #获取索引页对应的数据对象
	plist = p.page_range #获取分页索引所有对象
	print(mywhere)
	context={'hlist': list, 'plist': plist, 'pIndex': pIndex,'plist_len':len(plist),'mywhere':mywhere}
	return render(request,"mymanage/host/index.html",context)

def add(request):
	#加载主机增加信息窗口
	return render(request,"mymanage/host/host_add.html")

def insert(request):
	try:
		#新增主机信息
		list=Host()
		list.name=request.POST['txt_name']
		list.ip=request.POST['txt_ip']
		list.cpu=request.POST['txt_cpu']
		list.hard_disk=request.POST['txt_yp']
		list.memory=request.POST['txt_nc']
		list.state=request.POST['ra_rob']
		list.save()
		info="保存成功！"
		context={"info":info}
		return render(request,"mymanage/info.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"mymanage/info.html",context)

def edit(request,uid):
	try:
		#加载修改主机的表单
		ulist=Host.objects.get(id=uid)
		context={"list":ulist}
		return render(request,"mymanage/host/host_edit.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"mymanage/info.html",context)

def update(request):
	try:
		#修改主机信息
		list=Host.objects.get(id=request.POST['txt_id'])
		list.name=request.POST['txt_name']
		list.ip=request.POST['txt_ip']
		list.cpu=request.POST['txt_cpu']
		list.hard_disk=request.POST['txt_yp']
		list.memory=request.POST['txt_nc']
		list.state=request.POST['ra_rob']
		list.save()
		context={"info":"修改成功！"}
		return render(request,"mymanage/info.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"mymanage/info.html",context)

def delete(request,uid):
	try:
		list=Host.objects.get(id=uid)
		list.delete()
		context={"info":"删除成功"}
		return render(request,"mymanage/info.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"mymanage/info.html",context)

def monitor(request):
	#监控主机信息
	try:
		alist=Host.objects.all().first()
		context={"list":alist}
		return render(request,"mymanage/host/host_monitor.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"mymanage/info.html",context)

def monitor_find(request,uid):
	try:
		#选择要进行监控的主机
		ulist=Host.objects.get(id=uid)
		context={"list":ulist}
		return render(request,"mymanage/host/host_monitor_master.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"mymanage/info.html",context)

def monitor_update(request):
	try:
		#监控信息更新
		context={"id":request.POST['txt_id'],'ip':request.POST['txt_ip'],'user':request.POST['txt_root'],'pwd':request.POST['txt_pwd'],'sel':request.POST['ra_rob1']}
		return render(request,"mymanage/host/host_monitor.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"mymanage/info.html",context)

def monitor_list(request):
	try:
		#监控默认指定主机
		num=Host.objects.all().count()
		if num==0:
			context={"info":"没有任何主机信息"}
			return render(request,"mymanage/info.html",context)
		ulist=Host.objects.all().first()
		context={"list":ulist}
		return render(request,"mymanage/host/host_monitor_master.html",context)
	except Exception as info:
		context={"info":info}
		return render(request,"mymanage/info.html",context)

def monitor_data(request):
	#获取指定主机的CPU使用率
	try:
		txt=request.GET
		txt1=txt['txt_id']
		txt2=txt['txt_ip']
		txt3=txt['txt_user']
		txt4=txt['txt_pwd']
		txt5=txt['txt_sel']
		#定义一个远程客户端对象
		ssh=paramiko.SSHClient()
		#防止第一次连接陌生服务器的报错
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		#远程连接
		if txt5=="1":
			ssh.connect(hostname=txt2,username=txt3,password=txt4)
		elif txt5=="2":
			ssh.connect(hostname=txt2,username=txt3)
		else:
			context={"info":"用户名和密码开始输入的时候出错"}
			return render(request,"mymanage/info.html",context)
		#获取CPU核数
		command='cat /proc/cpuinfo | grep "cpu cores" | uniq'
		#标准输出
		stdin,stdout,stderr=ssh.exec_command(command)
		#获取执行状态码
		channel = stdout.channel
		status = channel.recv_exit_status()
		if status!=0:
			info="没有连接远程主机"
		command = stdout.read().decode()
		cpunum=re.findall("[0-9]+",command)

		#获取硬盘容量
		command='fdisk -l | grep Disk'
		#标准输出
		stdin,stdout,stderr=ssh.exec_command(command)
		command=stdout.readlines()
		hard=re.findall("[0-9]+",command[0])

		#获取内存容量
		command="cat /proc/meminfo | grep MemTotal"
		stdin,stdout,stderr=ssh.exec_command(command)

		command=stdout.read().decode()
		nc=re.findall("[0-9]+",command)

		#定义执行的命令 free -m 内存 iptraf -g 网络流量 iostat -d -x 磁盘使用
		command="vmstat 1 3|sed  '1d'|sed  '1d'|awk '{print $15}'"
		#标准输出
		stdin,stdout,stderr=ssh.exec_command(command)
		command = stdout.readlines()
		cpu_usage = str(round((100 - (int(command[0]) + int(command[1]) + int(command[2])) / 3), 2))
		time1=str(time.strftime("%H:%M:%S"))
		ssh.close()
		list={'time1':time1,'value1':cpu_usage,'cpu':cpunum[0],'hard':hard[0],'nc':nc[0],'info':status}
		return JsonResponse({'data':list})
	except Exception as info:
		status=2
		time1=""
		cpu_usage=0
		cpunum=0
		hard=0
		hard=0
		list={'time1':time1,'value1':cpu_usage,'cpu':cpunum,'hard':hard,'nc':hard,'info':status}
		return JsonResponse({'data':list})
