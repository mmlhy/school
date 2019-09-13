from PIL import Image, ImageDraw, ImageFont,ImageFilter
from io import BytesIO
import random
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
import simplejson
import time,datetime
import json
from . import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
# Create your views here.

def index(req):
	try:
		if req.session['is_login'] == 's':
			username = req.session['user_name']
			userid = req.session['user_id']
			user = models.STUDENT.objects.get(studentid=userid)
			t = {'male': '男', 'female': '女'}
			sex = t[user.sex]
			perid = user.perid
			xib = models.XI.objects.get(xiid=user.xiid)
			xiname = xib.name
			xg = models.XCLASS.objects.get(xclassid=user.xclassid)
			classname = xg.name
			return render(req,'index.html',locals())
		elif req.session['is_login'] == 't':
			username = req.session['user_name']
			userid = req.session['user_id']
			user = models.TEACHER.objects.get(teacherid=userid)
			t = {'male': '男', 'female': '女'}
			sex = t[user.sex]
			perid = user.perid
			xib = models.XI.objects.get(xiid=user.xiid)
			xiname = xib.name
			zhicheng = user.zhicheng
			return render(req, 'indext.html', locals())
	except:
		return redirect("/login/1/")

def login(req,type):
	message = ''
	if req.method =='POST':
		username = req.POST['username']
		password = req.POST['password']
		if type == 1:
			try:
				user = models.STUDENT.objects.get(studentid=username)
				if user.password != password:
					message = '密码不正确'
					return render(req, 'login.html',locals())
				if req.session['check_code'] != req.POST['code']:
					message = '验证码不正确'
					return render(req, 'login.html', locals())
				if user.password == password:
					req.session['is_login'] = 's'
					req.session['user_id'] = username
					req.session['user_name'] = user.name
					return redirect('/index/')
			except:
				message = '用户不存在'
				print(locals())
				return render(req, 'login.html', locals())
		if type == 2:
			try:
				user = models.TEACHER.objects.get(teacherid=username)
				if user.password != password:
					message = '密码不正确'
					return render(req, 'login.html', locals())
				if req.session['check_code'] != req.POST['code']:
					message = '验证码不正确'
					return render(req, 'login.html', locals())
				if user.password == password:
					req.session['is_login'] = 't'
					req.session['user_id'] = username
					req.session['user_name'] = user.name
					return redirect('/index/')
			except:
				message = '用户不存在'
				print(locals())
				return render(req, 'login.html', locals())

	return render(req,'login.html',locals())


def get_valiCode_img(req):
	width = 120
	height = 30
	char_length = 4
	#font_file = 'static/font/kumo.ttf'
	font_file = '/home/ubuntu/school/student/kumo.ttf'
	font_size = 28
	code = []
	img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
	draw = ImageDraw.Draw(img, mode='RGB')

	def rndChar():
		"""
        生成随机字母或数字
        :return:
        """
		if random.randint(0,1) == 0:
			return chr(random.randint(65, 90))
		else:
			return str(random.randint(0,9))

	def rndColor():
		"""
        生成随机颜色
        :return:
        """
		return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))

	# 写文字
	font = ImageFont.truetype(font_file, font_size)
	for i in range(char_length):
		char = rndChar()
		code.append(char)
		h = random.randint(0, 4)
		draw.text([i * width / char_length, h], char, font=font, fill=rndColor())

	# 写干扰点
	for i in range(40):
		draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

	# 写干扰圆圈
	for i in range(40):
		draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
		x = random.randint(0, width)
		y = random.randint(0, height)
		draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

	# 画干扰线
	for i in range(5):
		x1 = random.randint(0, width)
		y1 = random.randint(0, height)
		x2 = random.randint(0, width)
		y2 = random.randint(0, height)

		draw.line((x1, y1, x2, y2), fill=rndColor())

	img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
	stream = BytesIO()
	img.save(stream, 'png')
	print(code)
	co = ''.join(code)
	req.session['check_code'] = co
	data = stream.getvalue()
	return HttpResponse(data)

def schengji(req):
	username = req.session['user_name']
	chengji_list=[]
	try:
		xuan = models.XUANKE.objects.filter(studentid=req.session['user_id'])
	except:
		return render(req, 'chengji.html', locals())
	for i in xuan:
		chengji = {}
		chengji['id'] = i.lessonid
		chengji['grade'] = i.grade
		paike = models.PAIKE.objects.get(lessionid=i.lessonid)
		teacher = models.TEACHER.objects.filter(teacherid=paike.teacherid)
		tea = []
		for j in teacher:
			tea.append(j.name)
		chengji['t_name'] = co = ','.join(tea)
		lession = models.LESSONS.objects.get(lessionid=i.lessonid)
		chengji['l_name'] = lession.name
		chengji_list.append(chengji)
	print(chengji_list)
	return render(req,'chengji.html',locals())

def skebiao(req):
	today = str(time.strftime("%Y-%m-%d"))
	try:
		zhou = int(req.GET['z'])
	except:
		zhou = days(today, '2019-08-26')
	if zhou <=0:
		zhou = 1
	elif zhou >= 25:
		zhou = 25
	if req.session['is_login'] == 's':
		xuan = models.XUANKE.objects.filter(studentid=req.session['user_id'])
		for i in xuan:
			paike = models.PAIKE.objects.filter(lessionid=i.lessonid)
			for j in paike:
				jclass = models.JCLASS.objects.get(jclassid=j.jclassid)
				s = int(jclass.startweek)
				e = int(jclass.endweek)
				if zhou >= s and zhou <= e:
					t_name = models.TEACHER.objects.get(teacherid=j.teacherid).name
					class_wei = models.CLASSROOM.objects.get(classroomid=jclass.classroomid).weizhi
					lesson_name = models.LESSONS.objects.get(lessionid=j.jclassid).name
					k = str(jclass.week) + '_' + str(jclass.jieci)
					locals()[k + '_lesson_name'] = lesson_name
					locals()[k + '_teacher_name'] = t_name
					locals()[k + '_class_wei'] = class_wei
				else:
					continue
		return render(req,'kebiao.html',locals())
	else:
		paike = models.PAIKE.objects.filter(teacherid=req.session['user_id'])
		for j in paike:
			jclass = models.JCLASS.objects.get(jclassid=j.jclassid)
			s = int(jclass.startweek)
			e = int(jclass.endweek)
			if zhou >= s and zhou <= e:
				t_name = models.TEACHER.objects.get(teacherid=j.teacherid).name
				class_wei = models.CLASSROOM.objects.get(classroomid=jclass.classroomid).weizhi
				lesson_name = models.LESSONS.objects.get(lessionid=j.jclassid).name
				k = str(jclass.week) + '_' + str(jclass.jieci)
				locals()[k + '_lesson_name'] = lesson_name
				locals()[k + '_teacher_name'] = t_name
				locals()[k + '_class_wei'] = class_wei
			else:
				continue
		return render(req,'tkebiao.html',locals())

def days(str1,str2):
	date1=datetime.datetime.strptime(str1[0:10],"%Y-%m-%d")
	date2=datetime.datetime.strptime(str2[0:10],"%Y-%m-%d")
	num=int((date1-date2).days)
	if num / 7 !=0:
		num = int(num / 7) + 1
	else:
		num = int(num / 7)
	return num

def test(req):
	xclass = models.XCLASS.objects.filter(teacherid=req.session['user_id'])
	c = []
	for i in xclass:
		c.append(i.xclassid)
	qing = models.QINGJIA.objects.all()
	jl = [{'name': models.STUDENT.objects.get(studentid=x.studentid).name,
		   'xclass': models.XCLASS.objects.get(xclassid=models.STUDENT.objects.get(studentid=x.studentid).xclassid).name,
		   'studentid': x.studentid, 'starttime': x.starttime, 'endtime': x.endtime, 'cause': x.cause,
		   'zhuangtai': x.zhuangtai, 'is_xiao': x.is_xiao} for x in qing if
		  models.STUDENT.objects.get(studentid=x.studentid).xclassid in c and x.is_xiao == '否']
	return render(req,'test.html',locals())

def qingjia(req):
	if req.method == 'POST':
		stime = req.POST['startdate']+' '+req.POST['starttime']
		stime = time.strptime(stime,"%Y-%m-%d %H:%M")
		stime = time.strftime("%Y-%m-%d %H:%M:%S", stime)
		etime = req.POST['enddate']+' '+req.POST['endtime']
		etime = time.strptime(etime,"%Y-%m-%d %H:%M")
		etime = time.strftime("%Y-%m-%d %H:%M:%S", etime)
		new_c = models.QINGJIA(
			studentid=int(req.session['user_id']),
			starttime=stime,
			endtime=etime,
			cause=req.POST['cause'],
		)
		new_c.save()
	return render(req,'qingjia.html',locals())

def jilu(req):
	if req.method =='POST':
		if req.session['is_login'] == 's':
			a = req.POST['qb']
			print(a)
			models.QINGJIA.objects.filter(qingid=a).update(is_xiao = '是')
			return HttpResponse("TRUE")
		else:
			id = req.POST['qb']
			is_tong = req.POST['tong']
			models.QINGJIA.objects.filter(qingid=id).update(zhuangtai = is_tong)
			return HttpResponse("TRUE")
	username = req.session['user_name']
	if req.session['is_login'] == 's':
		b = models.QINGJIA.objects.filter(studentid=req.session['user_id'])
		jl = [{'name':models.STUDENT.objects.get(studentid=x.studentid).name,'qingid':x.qingid,'studentid':x.studentid,'starttime':x.starttime,'endtime':x.endtime,'cause':x.cause,'zhuangtai':x.zhuangtai,'is_xiao':x.is_xiao} for x in b]
		paginator = Paginator(jl, 12)
		if req.method == "GET":
			# 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
			page = req.GET.get('page')
			try:
				jilu = paginator.page(page)
			except PageNotAnInteger:
				# 如果请求的页数不是整数, 返回第一页。
				jilu = paginator.page(1)
			except InvalidPage:
				# 如果请求的页数不存在, 重定向页面
				message = "页面不存在"
			except EmptyPage:
				# 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
				jilu = paginator.page(paginator.num_pages)
		return render(req,'jilu.html',locals())
	else:
		xclass = models.XCLASS.objects.filter(teacherid=req.session['user_id'])
		c = []
		for i in xclass:
			c.append(i.xclassid)
		qing = models.QINGJIA.objects.all()
		jl = [{'name': models.STUDENT.objects.get(studentid=x.studentid).name,'qingid':x.qingid,
			   'xclass': models.XCLASS.objects.get(
				   xclassid=models.STUDENT.objects.get(studentid=x.studentid).xclassid).name,
			   'studentid': x.studentid, 'starttime': x.starttime, 'endtime': x.endtime, 'cause': x.cause,
			   'zhuangtai': x.zhuangtai, 'is_xiao': x.is_xiao} for x in qing if
			  models.STUDENT.objects.get(studentid=x.studentid).xclassid in c]
		paginator = Paginator(jl, 12)
		if req.method == "GET":
			# 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
			page = req.GET.get('page')
			try:
				jilu = paginator.page(page)
			except PageNotAnInteger:
				# 如果请求的页数不是整数, 返回第一页。
				jilu = paginator.page(1)
			except InvalidPage:
				# 如果请求的页数不存在, 重定向页面
				message = "页面不存在"
			except EmptyPage:
				# 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
				jilu = paginator.page(paginator.num_pages)
		return render(req, 'jilut.html', locals())

def kezhuang(req):
	today = str(time.strftime("%Y-%m-%d"))
	zhou = days(today, '2019-03-01')
	paike = models.PAIKE.objects.filter(teacherid=req.session['user_id'])
	jclass = [x.jclassid for x in paike]
	d = time.localtime()
	day = time.strftime("%w",d)
	t = time.localtime(time.time())
	ti = int('%d' % (t.tm_hour * 60 + t.tm_min))
	if  480 < ti <= 500:
		ci = 1
	elif 500 < ti <= 720:
		ci = 2
	elif 820 < ti <= 940:
		ci = 3
	elif 940 < ti <= 1060:
		ci = 4
	elif 1150 < ti <= 1270:
		ci =5
	try:
		for x in jclass:
			j = models.JCLASS.objects.get(jclassid=x)
			if j.week == day and j.jieci == int(ci) :
				jclassid = x
				break
		biao = [{'studentid':x.studentid,'name':models.STUDENT.objects.get(studentid=x.studentid).name,
			'xclass':models.XCLASS.objects.get(xclassid=models.STUDENT.objects.get(studentid=x.studentid).xclassid).name,
					 'zhuangtai':x.zhuangtai}for x in models.QIANDAO.objects.filter(jclassid=jclassid)]
	except:
		biaoji = "暂时没课"
	return render(req,'kezhuang.html',locals())

def dchengji(req):
	wrong = False
	message = "课程目录"
	try:
		class_list = [{'lesson_id':x.lessionid,'lesson_name':models.LESSONS.objects.get(lessionid=x.lessionid).name,'jclass_id':x.jclassid} for x in models.PAIKE.objects.filter(teacherid=req.session['user_id'])]
		if len(class_list) == 0:
			wrong = True
			return render(req, 'tchengji.html', locals())
		for i in class_list:
			if len(models.XUANKE.objects.filter(lessonid=i['lesson_id'])) != len (models.XUANKE.objects.filter(lessonid=i['lesson_id'],grade = None)):
				i['c'] = True
				print(class_list)
			else:
				i['c'] = False
				print(class_list)
		paginator = Paginator(class_list, 12)
		if req.method == "GET":
			# 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
			page = req.GET.get('page')
			try:
				jilu = paginator.page(page)
			except PageNotAnInteger:
				# 如果请求的页数不是整数, 返回第一页。
				jilu = paginator.page(1)
			except InvalidPage:
				# 如果请求的页数不存在, 重定向页面
				message = "页面不存在"
			except EmptyPage:
				# 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
				jilu = paginator.page(paginator.num_pages)
	except:
		wrong = True
	return render(req, 'tchengji.html', locals())

def ddchengji(req):
	if req.method == "GET":
		print(req.GET.get('id'))
	return render(req, 'ddchengji.html', locals())