# -*- coding: utf-8 -*-
# -*- coding: euc-kr -*-

# login app 정리 부분적으로 완료(2/22)

from django.views.generic import TemplateView
from django.views.generic import RedirectView,ListView
from django.views.generic import View

from lecture.models import *#강의 목록

from django.contrib.auth.decorators import login_required#로그인 허용기능
from django.contrib.auth import logout #로그아웃 기능
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q #데이터 베이스 OR 기능 구현
from index.models import * #아직 시험중

from index.views import MajorSelect#전공 선택 및 페이지 메인 페이지 보여주는 함수를 불러옴
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist

# from selenium import webdriver	# 히스넷 체크를 위한 크롤링 모듈
from login.models import Profile	# 회원 추가 정보 model
from django.contrib.auth.models import User	# user model 등록
from functionhelper.views import *
import mechanicalsoup
from bs4 import BeautifulSoup
# django encoding
from django.utils.encoding import smart_str, smart_text
from .forms import LoginForm
from django.contrib import messages
#로그인 페이지	
class LoginView(ListView):
	template_name = 'html/login.html'
	m_template_name = "m_skins/m_html/login.html"
	context_object_name = "PageBoard"
	model=Total_Evaluation

	def get_context_data(self,**kwargs):
		if self.request.user.is_authenticated():
			self.paginate_by=10
		context=super(LoginView,self).get_context_data(**kwargs)
		if self.request.user.is_authenticated():
			block_size = 10 # 하단의 페이지 목록 수
			start_index = int((context['page_obj'].number - 1) / block_size) * block_size
			end_index = min(start_index + block_size, len(context['paginator'].page_range))
			context['page_range'] = context['paginator'].page_range[start_index:end_index]
		else:
			context['form']=LoginForm()
		return context
	def get_template_names(self):
		if self.request.user.is_authenticated():
			
			template_name="html/index.html"
		else:
			template_name="html/login.html"
		return 	[template_name]	
	def get_queryset(self):
		if self.request.user.is_authenticated():
			CourseCode=MajorSelect(self.request.user)
			return Total_Evaluation.objects.filter(Q(Course__Code__contains =CourseCode[0]) |Q(Course__Code__contains=CourseCode[1]))
	def post(self,request,*args, **kwargs):
		form =LoginForm(request.POST)
		if form.is_valid():			
			if request.POST.get('username', 'None') == 'admin_seal':
				username = request.POST['username']
				password = request.POST['password']
				user = authenticate(username=username, password=password)
			elif 'stu_num' in request.POST:	# 학번 값이 들어올 경우 해당 학번으로 로그인 제공.
				username = request.POST['stu_num']
				user = User.objects.filter(username=username)[0]
			elif 'stuNum' in request.POST:	# 학번 값이 들어올 경우 해당 학번으로 로그인 제공.
				if request.user.is_authenticated():	# 로그인 중일 때는 로그아웃 후에 재 로그인
					logout(request)
				username = request.POST['stuNum']
				if not username:
					LoginError(request)	# igo에서 받아온 값이 비어있을 경우 로그인 에러 발생
				try:
					user = User.objects.filter(username=username)[0]
				except IndexError:
					return HisnetCheck(request)
			elif request.POST.get('username', 'None'):
				username = request.POST['username']		# 여기서 username은 학번이 아닌 입력받은 히스넷 아이디
				password = request.POST['password']
			
				# 크롤링 Configuration
				browser = mechanicalsoup.Browser()
				
				
				page=browser.get("https://hisnet.handong.edu/login/login.php", verify=False)  

				form=page.soup.find("form",{"name":"login"}) 
				form.find("input",{"name":"id"})["value"]= smart_text(username).encode('euc-kr')
				form.find("input",{"name":"password"})["value"] = password  
				
				response=browser.submit(form,page.url)
				contents=browser.get("https://hisnet.handong.edu/haksa/hakjuk/HHAK110M.php")
				
				soup = contents.soup
				titles = soup.find_all(class_='tblcationTitlecls')
				# Save the informationn
				try:
					stu_num = titles[2].next_sibling.next_sibling.text[-8:]
					temp_major = titles[11].next_sibling.next_sibling.text.split('.')
					first_major = temp_major[0]
				except IndexError as e:
					return LoginError(request)	# 학번 혹은 전공 확인되지 않으면 로그인 에러
				try:
					second_major = temp_major[1]
				except IndexError as e:
					second_major = None

				try:
					user = User.objects.get(username=stu_num)
				except ObjectDoesNotExist:
					information=HisnetCheck(request)					
					newuser=RegisterInformation(information)
					request.session['stu_num']=information['stu_num']
					auth_login(request,newuser)
					return HttpResponseRedirect("/RegisterInfo")
				# user = None
			if user is not None:
				user.backend = 'django.contrib.auth.backends.ModelBackend'	# To login without password
				auth_login(request, user)
				#메인페이지 보여줄 함수 호출
				return HttpResponseRedirect("/")				
			else:
				return LoginError(request)

#로그아웃
class LogoutView(RedirectView):
	permanent =False
	query_string=True
	pattern_name='logout'
	def get_redirect_url(self,*args,**kwargs):
		if self.request.user.is_authenticated():
			logout(self.request)
		self.url='/'
		return super(LogoutView,self).get_redirect_url(*args,**kwargs)


def LoginError(request):
	
	return render(request,'html/login_error.html')

def Confirm(request):
	if request.flavour =='full':
		return render(request,'html/confirm.html')
	else:
		return render(request,'m_skins/m_html/confirm.html')

@csrf_protect
def HisnetCheck(request):
	#hisnet_url = "http://hisnet.handong.edu/login/login.php"
	if request.method == 'POST':
		if 'stuNum' in request.POST:
			stu_num = request.POST['stuNum']
			stu_name = request.POST['usr_name']
			stu_major = request.POST['stuMajor'].split('.')
			first_major = stu_major[0].strip()
			try:
				second_major = stu_major[1].strip()
			except:
				second_major = None

			ctx = {
				'stu_num': stu_num,
				'stu_name': stu_name,
				'first_major': first_major,
				'second_major': second_major,
			}

			if request.flavour =='full':
				return render(request,'html/agree_reg.html', ctx)
			else:
				return render(request,'m_skins/m_html/agree_reg.html', ctx)

		else:
			hisnet_id = request.POST['username']
			hisnet_pw = request.POST['password']

			browser = mechanicalsoup.Browser()
				
				
			page=browser.get("https://hisnet.handong.edu/login/login.php", verify=False)  

			form=page.soup.find("form",{"name":"login"}) 
			form.find("input",{"name":"id"})["value"]= smart_text(hisnet_id).encode('euc-kr')
			form.find("input",{"name":"password"})["value"] = hisnet_pw  
			
			response=browser.submit(form,page.url)
			contents=browser.get("https://hisnet.handong.edu/haksa/hakjuk/HHAK110M.php")
			
			soup = contents.soup
			titles = soup.find_all(class_='tblcationTitlecls')
			# Save the informationn
			# Save the information
			try:
				stu_name = titles[0].next_sibling.next_sibling.text[:-1]
				stu_num = titles[2].next_sibling.next_sibling.text[-8:]
				temp_major = titles[11].next_sibling.next_sibling.text.split('.')
				first_major = temp_major[0]
			except IndexError as e:
				return LoginError(request)	# 학번 혹은 전공 확인되지 않으면 로그인 에러
			try:
				second_major = temp_major[1]
			except IndexError as e:
				second_major = None

			record_contents=browser.get("https://hisnet.handong.edu/haksa/record/HREC110M.php")
			record_soup = record_contents.soup

			tables = record_soup.find_all(id='att_list')	# navigate to lecture list table
			all_rec = ''	# 전체 수강목록 string 초기화

			for i, table in enumerate(tables):
				if i < 2:
					continue
				trs = table.find_all('tr')
				# rec_semester = trs[0].text.split()[0]	# 수강 학기
				for i, tr in enumerate(trs):
					if i < 2:
						continue
					rec_code = tr.find('td')
					rec_name = rec_code.next_sibling.next_sibling
					all_rec += rec_code.text + '->' + rec_name.text + '$$'		# 구분자 '$$' 나중에 split하기 위함.
			all_rec = all_rec[:-2]	# 마지막 구분자 '$$'' 제거

			ctx = {
				'stu_num': stu_num,
				'stu_name': stu_name,
				'first_major': first_major,
				'second_major': second_major,
				'all_rec': all_rec,
			}
			return ctx
			# if request.flavour =='full':
			# 	return render(request,'html/agree_reg.html', ctx)
			# else:
			# 	return render(request,'m_skins/m_html/agree_reg.html', ctx)
	else:
		if request.flavour =='full':
			return render(request,'html/login.html')
		else:
			return render(request,'m_skins/m_html/login.html')

class RegisterInfoView(TemplateView):
	template_name="html/agree_reg.html"
	def get_context_data(self,**kwargs):
		context=super(RegisterInfoView,self).get_context_data(**kwargs)
		return context
	
class RegisterView(RedirectView):
	permanent =False
	query_string=True
	pattern_name='logout'
	def get_redirect_url(self,*args,**kwargs):
		self.url='/'

		return super(RegisterView,self).get_redirect_url(*args,**kwargs)
class CancelView(RedirectView):
	permanent =False
	query_string=True
	pattern_name='cancel'
	def get_redirect_url(self,*args,**kwargs):
		if 'stu_num' in self.request.session:
			user=User.objects.get(username=self.request.session['stu_num'])
			user.delete()
		self.url='/'
		return super(CancelView,self).get_redirect_url(*args,**kwargs)

def RegisterInformation(information):
	stu_num = information['stu_num']
	stu_name = information['stu_name']
	first_major = information['first_major']
	second_major = information['second_major']
	all_rec = information['all_rec']
	# 신입생 전공 비어있는 경우 직접 할당
	if not first_major:
		first_major = '글로벌리더십'

	try:
		user = User.objects.create_user(username=stu_num)
		user.save()
		get_user = User.objects.get(username=stu_num)
		profile = Profile(User=get_user, FirstMajor=first_major, SecondMajor=second_major, UserName=stu_name, LectureRecord=all_rec)
		profile.save()
		return user
	except:
		# User를 만들었으나 Profile에서 실패할 경우 User만 등록되는 겨우가 발생함.
		# 예외처리로 User만 등록되었을 때를 위한 처리
		e_user = User.objects.filter(username=stu_num)
		if e_user:
			e_user.delete()

		if request.flavour =='full':
			return render(request,'html/stu_num_duplicate.html')
		else:
			return render(request,'m_skins/m_html/stu_num_duplicate.html')	# m_skin 없음

	
def static_forbidden(request):
	raise  PermissionDenied
