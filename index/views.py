# -*- coding: utf-8 -*-
# -*- coding: euc-kr -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.views.generic import View,ListView
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404,JsonResponse
from base.views import *
from index.models import * 
from lecture.models import *
from login.models import *
from index.serializers import Total_Evaluation_Serializer
from django.views.decorators.csrf import csrf_protect
import datetime
from django.db.models import Q
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import mechanicalsoup
import logging
from bs4 import BeautifulSoup
from rest_framework.response import Response


class MyPageView(LoginRequiredMixin,TemplateView):
	login_url="/"
	template_name = 'html/sealmypage.html'
	m_template_name = "m_skins/m_html/sealmypage.html"

	def get_context_data(self,**kwargs):
		context=super(MyPageView,self).get_context_data(**kwargs)
		return context
class MainPageView(LoginRequiredMixin,PageView):
	login_url="/"
	template_name = "html/page.html"
	context_object_name = "PageBoard"
	paginate_by=10
	logger = logging.getLogger(__name__) 
	class Meta:
		ordering = ['id']
	def get_template_names(self):
		if 'page' in self.kwargs:
			template_name = "html/page.html"
			m_template_name = "m_html/page.html"
		else:
			template_name = "html/page.html"
			m_template_name = "m_html/page.html"
		if self.request.flavour == 'mobile':
			return [m_template_name]
		else:
			return [template_name]
	def get_queryset(self):
		CourseCode=MajorSelect(self.request.user)
		return Total_Evaluation.objects.filter(Q(Course__Code__contains =CourseCode[0]) |Q(Course__Code__contains=CourseCode[1])).order_by("id")
	def get_context_data(self,**kwargs):
		context=super(MainPageView,self).get_context_data(**kwargs)
		return context
class AutoSearchView(LoginRequiredMixin,PageView):
	def get(self,request):
		CourseName=request.GET['phrase']		
		data=Lecture.objects.filter(Q(CourseName__icontains=CourseName) | Q(Professor__icontains=CourseName)).annotate(total=Count('Code')).values("CourseName").distinct()[0:10]
		CourseList=[]
		for item in data:
			newCourse=dict()
			newCourse['CourseName']=item['CourseName']
			CourseList.append(newCourse)
		return JsonResponse(CourseList,safe=False)
class AutoSearchResultView(LoginRequiredMixin,View):
	def get(self,request):
		CourseName=request.GET['phrase']		
		data=Lecture.objects.filter(Q(CourseName__icontains=CourseName) | Q(Professor__icontains=CourseName)).annotate(total=Count('Code')).values("CourseName").distinct()[0:10]
		CourseList=[]
		for item in data:
			newCourse=dict()
			newCourse['CourseName']=item['CourseName']
			CourseList.append(newCourse)
		return JsonResponse(CourseList,safe=False)
class SearchView(LoginRequiredMixin,PageView):
	login_url="/"
	context_object_name="PageBoard"
	paginate_by=10
	class Meta:
		ordering = ['id']
	def get_template_names(self):
		if 'page' in self.kwargs:
			template_name = "html/searchpage.html"
			m_template_name = "m_html/searchpage.html"
		else:
			template_name = "html/search.html"
			m_template_name = "m_html/search.html"
		if self.request.flavour == 'mobile':
			return [m_template_name]
		else:
			return [template_name]

	def get_context_data(self,**kwargs):
		context=super(SearchView,self).get_context_data(**kwargs)
		context['search']=self.request.GET['search'].upper()
		return context
	def get_queryset(self):
		search_data = self.request.GET['search'].upper()
		return Total_Evaluation.objects.filter(Q(Course__CourseName__icontains=search_data) | Q(Course__Professor__icontains=search_data)).distinct().order_by("Course__CourseName")
class StudentInformationChangeView(LoginRequiredMixin,TemplateView):
	def get_context_data(self,**kwargs):
		context=super(StudentInformationChangeView,self).get_context_data(**kwargs)
		return context
	def post(self,request):
			myprofile = Profile.objects.get(User= request.user)
			username = request.POST['username']		# 여기서 username은 학번이 아닌 입력받은 히스넷 아이디
			password = request.POST['password']
			browser = mechanicalsoup.Browser()
			page=browser.get("https://hisnet.handong.edu/login/login.php")  

			form=page.soup.find("form",{"name":"login"}) 
			form.find("input",{"name":"id"})["value"]= smart_text(username).encode('euc-kr')
			form.find("input",{"name":"password"})["value"] = password  
			
			response=browser.submit(form,page.url)
			contents=browser.get("https://hisnet.handong.edu/haksa/hakjuk/HHAK110M.php")
			
			soup = contents.soup
			titles = soup.find_all(class_='tblcationTitlecls')
			# Save the information
			stu_name = titles[0].next_sibling.next_sibling.text[:-1]
			stu_num = titles[2].next_sibling.next_sibling.text[-8:]
			temp_major = titles[11].next_sibling.next_sibling.text.split('. ')
			first_major = temp_major[0]

			try:
				second_major = temp_major[1]
			except IndexError as e:
				second_major = None

			contents = browser.get("https://hisnet.handong.edu/haksa/lecture/HLEC110M.php")
			record_soup = contents.soup
			h_years=record_soup.find_all(attrs={"name":"hak_year"})[0].find_all("option")
			h_semesters = record_soup.find_all(attrs={"name":"hak_term"})[0].find_all("option")
			all_rec = ''	# 전체 수강목록 string 초기화
			for year in h_years[1:]:
				for semester in h_semesters[1:]:
					form2=record_soup.find("form",{"name":"form1"}) 
					form2.find("select",{"name":"hak_year"}).find("option",{"selected":""})["value"]= year['value']
					form2.find("select",{"name":"hak_term"}).find("option",{"selected":""})["value"] = semester['value']  

					try:
						lecture_contents = browser.submit(form2,contents.url)
					except:
						raise Exception
					lecture_record_soup = lecture_contents.soup
					tables = lecture_record_soup.find_all(id='att_list')	# navigate to lecture list table
						
					for i, table in enumerate(tables):
						
						trs = table.find_all('tr')
						# rec_semester = trs[0].text.split()[0]	# 수강 학기
						for i, tr in enumerate(trs):
							if i < 1:
								continue
							element= tr.find_all('td')
							rec_code = element[1].text
							rec_name =element[2].text
							rec_professor = element[6].text[1:]
							all_rec += rec_code + '->' + rec_name + '->' +rec_professor+ '$$'		# 구분자 '$$' 나중에 split하기 위함.
			all_rec = all_rec[:-2]	# 마지막 구분자 '$$'' 제거

			myprofile.FirstMajor= first_major
			if second_major=="":
				myprofile.SecondMajor="None"
			else:
				myprofile.SecondMajor=second_major
			try:
				myprofile.LectureRecord=all_rec
			except:
				raise Exception
			myprofile.save()
			return JsonResponse({"OK":True},safe=False)
class MyCourseView(LoginRequiredMixin,PageView):
	login_url="/"
	context_object_name="MyLecture"
	paginate_by=10
	MyCourseList=[]
	class Meta:
		ordering = ['id']

	def get_template_names(self):
		user = Profile.objects.get(User =self.request.user)
		if 'page' in self.kwargs:
			template_name="html/mysugangpage.html"
			m_template_name="m_html/mysugangpage.html"
		elif len(user.LectureRecord.split("$$")[0].split("->"))<3:
			template_name = "html/notmysuganglist.html"
			m_template_name = "m_html/notmysuganglist.html"
		else:
			template_name="html/mysuganglist.html"
			m_template_name = "m_html/mysuganglist.html"
		if self.request.flavour == "mobile": 
			return 	[m_template_name]	
		else :
			return [template_name]
	def get_context_data(self,**kwargs):
		context=super(MyCourseView,self).get_context_data(**kwargs)
		
		return context
	def get_queryset(self):
		user = Profile.objects.get(User =self.request.user)

		MyCourseList =user.LectureRecord.split("$$") 
		count=0
		for data in MyCourseList:
			splitdata =data.split("->")
			try:
				splitdata[2] = splitdata[2][1:].split("외")!=None and splitdata[2][1:].split("외")[0] or splitdata[2][1:]
			except:
				break
			MyCourseList[count]=splitdata
			MyCourseList[count]=Total_Evaluation.objects.filter(Course__Code=splitdata[0],Course__CourseName=splitdata[1],Course__Professor__contains=splitdata[2]).order_by("Course__Semester")[0]
			count+=1
		
		
		
		self.MyCourseList=MyCourseList

		return MyCourseList

class CategorySystemView(LoginRequiredMixin,PageView):
	login_url="/"
	template_name = "html/categorypage.html"
	context_object_name = "PageBoard"
	paginate_by=10
	Dic={}
	def get_template_names(self):
		user = Profile.objects.get(User =self.request.user)
		if 'page' in self.kwargs:
			template_name="html/categorypage.html"
			m_template_name="m_html/categorypage.html"
		else:
			template_name="html/categorypage.html"
			m_template_name = "m_html/categorypage.html"
		if self.request.flavour == "mobile": 
			return 	[m_template_name]	
		else :
			return [template_name]
	def get_queryset(self):
		logger = logging.getLogger("mysite2.lecture") 
		
		for key in self.request.GET.keys():
			self.Dic[key]= self.request.GET[key]
		major = self.Dic['major'] != "0" and self.Dic['major'] or "0"
		category = self.Dic['category'] != "0" and self.Dic['category'] or "0"

		ordered = self.Dic['ordered'] != "0" and self.Dic['ordered'] or "0"
		orderdata=''
		
		if(ordered=="최신순"):
			orderdata='Total_Count'
		else:
			orderdata='-Total_Count'
		if(major =="0" and category =="0"):
			return Total_Evaluation.objects.all()
		elif(major!="0" and category !="0"):	
			return Total_Evaluation.objects.filter(Course__Category=category,Course__Major__icontains=major).order_by(orderdata,'id')
		elif major=="0":
			return Total_Evaluation.objects.filter(Course__Category=category).order_by(orderdata)
		elif category=="0":
			return Total_Evaluation.objects.filter(Course__Major__contains=major).order_by(orderdata)
		
	def get_context_data(self,**kwargs):
		context=super(CategorySystemView,self).get_context_data(**kwargs)
		for key in self.Dic.keys():
			context[key]= self.Dic[key]
		return context

class JsonResponse_Total_Evaluation(LoginRequiredMixin,ListAPIView):
	
	paginate_by=10
	serializer_class =Total_Evaluation_Serializer
	queryset=Total_Evaluation.objects.all()
		#return JsonResponse(serializer.errors, status=400)
	def get(self,request,*args,**kwargs):
		if 'page' in self.kwargs:
			page= kwargs['page']
		start = (int(page)-1)*10
		end = int(page)*10
		query = self.get_queryset()[start:end]
		serializer = Total_Evaluation_Serializer(query,many=True)

		return Response(serializer.data,status=200)
		#return JsonResponse(serializer.errors, status=400)
	def post(self,request,*args,**kwargs):
		#serializer = Total_Evaluation_Serializer(self.qureyset,many=True)
		return Response(serializer.data,status=200)
	








def MyPage(request):	#MyPage 루트
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	dic = {'user':request.user,'BestBoard':BestBoardView(),'TotalCountBoard':TotalEvalutionCount()}
		
	if request.flavour =='full':
			return render(request,'html/sealmypage.html',dic)
	else:	
			return render(request,"m_skins/m_html/sealmypage.html", dic) 

def About(request): #About template 루트
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")

	dic = {'user':request.user, 'BestBoard':BestBoardView(),'TotalCountBoard':TotalEvalutionCount()}
	
	if request.flavour =='full':
			return render(request,'html/about.html',dic)
	else:	
			return render(request,"m_skins/m_html/about.html",dic)

def Schedule(request): #Schedule template 기능
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	
	dic={'user':request.user,'BestBoard':BestBoardView(),'TotalCountBoard':TotalEvalutionCount()}

	if request.flavour =='full':
		return render(request,'html/schedule.html',dic)
	else:
		return render(request,"m_skins/m_html/schedule.html", dic)

def Judgement(request): # 신고 게시판 기능

	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	dic = {'user':request.user,'BestBoard':BestBoardView(),'TotalCountBoard':TotalEvalutionCount()}
	if request.flavour =='full':
		return render(request,'html/subscribe_report.html',dic)
	else:
		return render(request,"m_skins/m_html/subscribe_report.html",dic)

	
	
@csrf_protect
def Page(request): #Main Page를 보여주는 함수 
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	try:
		if request.method =="POST":
			PostDic = dict()
			for key in request.POST.keys(): #현재 ajax에서 받아온 post값들 key를 비교해서 dictionary로 표현해서 씀
				Data=request.POST[key]	
				PostDic[key] =request.POST[key]
			if 'Course' in request.POST.keys(): 
				if request.POST['Course']!="": # 강의 이름이 입력 되었을 때 해당 강의이름의 code까지 얻어 오기 위함
					if 'Code' not in request.POST.keys():
						A=Lecture.objects.filter(CourseName =PostDic['Course'])[0]
						PostDic['Code']= A.Code
			else:
				PostDic['Course']= ""
			if 'ProSelect' not in request.POST.keys():
				PostDic['ProSelect'] = 0
			 
	except ValueError:
			raise Http404() 
	
	PostDic['Page']= PostDic['Page'] !="0" and PostDic['Page'] or "1" #페이지 위치에 따른 값 결정
	
	
	#웹에 뿌려줄 template 종류 정하는 함수(functionhelper 참고)
	#target = TargetTemplate(PostDic['Current'])
	target = "page.html"
	#메인에다가 강의 정보 뿌려주는 함수(functionhelper 참고)
	template = MainPageView(request.user, request.session['PageInformation'],int(PostDic['Page']),0,mobile)


	#왜 했는지 기억안남...
	request.session['PageInformation'] = template['PageInformation']
	if request.flavour =='full':
		return render(request,'html/'+target,template)
	else:
		return render(request,'m_skins/m_html/'+target,template)

def SubScript(request): #아직 뭐하는 기능인지 모르겠음
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")

	dic = {'user':request.user,'BestBoard':BestBoardView(),'TotalCountBoard':TotalEvalutionCount()}

	if request.flavour =='full':
		return render(request,'html/subscribe_improve.html',dic)
	else:
		return render(request,"m_skins/m_html/subscribe_improve.html",dic)

def SiteMap(request): #사이트 맵
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	dic = {'user':request.user}

	if request.flavour =='full':
		return render(request,'html/sitemap.html',dic)
	else:
		return render(request,"m_skins/m_html/sitemap.html",dic )

def MyCourse(request): #내가 추천한 목록 보여주는 페이지로 감
		if CheckingLogin(request.user.username):
			return HttpResponseRedirect("/")
		MyProfile = Profile.objects.get(User=request.user)
		
		LikePage=LikePage_Course.objects.filter(CreatedID= MyProfile)
		RecommendPage= Recommend_Course.objects.filter(CreatedID = MyProfile)
		
		dic = {'user':request.user, 
				'RecommendPage':RecommendPage,
				'LikePage':LikePage,
				'BestBoard':BestBoardView(),'TotalCountBoard':TotalEvalutionCount()}
		if request.flavour =='full':
			return render(request,'html/mycourses.html',dic)
		else:
			return render(request,"m_skins/m_html/mycourses.html", dic)
'''
@csrf_protect
def Search(request): #과목 검색 기능
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	Mobile = request.flavour
	if request.method =="POST":
		SearchData = request.POST['search']
		SearchData.upper()
		#여기 문제
		LectureData = [[]]

		j=0
		try: 
			"""
			밑의 알고리즘은 현재 DB에 등록 되어있는 강의 이름을 토대로 group by로 묶어서 중복되는 강의이름을 하나로 묶어 버린후에
			그 강의이름 정보를 토대로 다시 DB에서 호출하는데 그 강의중 중복되는 정보만 추출하면 되는 거라 하나씩 불러서 그 부른 강의들을
			list화 시킴. 그리고 나서 그 list화 시킨 강의 정보를 다시 전체 평가 한 강의 부분 DB에서 다시 호출해 강의마다 평가된 
			평가 갯수를 다 더해서 함
			ps)물론 DB하나 더 만들면 더 간단한 알고리즘이 되겠지만 어차피 DB에서 한번더 불러야 하는건 마찬가지라 속도가 비슷할 거같아서
			안만듬
			"""
			if Mobile == "full":
				PageBoard=Total_Evaluation.objects.filter(Q(Course__CourseName__icontains=SearchData) | Q(Course__Professor__icontains=SearchData)).distinct().order_by("Course__CourseName")[0:10]
			else:
				PageBoard=Total_Evaluation.objects.filter(Q(Course__CourseName__icontains=SearchData) | Q(Course__Professor__icontains=SearchData)).distinct()[0:5]
		
		except:
			LectureData[0]=None
		if Mobile == "full":
			DBCount = Total_Evaluation.objects.filter(Q(Course__CourseName__icontains=SearchData) | Q(Course__Professor__icontains=SearchData)).distinct().count()
			SearchCount=DataCount(10,DBCount)
		else:
			DBCount = Total_Evaluation.objects.filter(Q(Course__CourseName__icontains=SearchData) | Q(Course__Professor__icontains=SearchData)).distinct().count()
			SearchCount=DataCount(5,DBCount)
		
		if DBCount != 0 : 
			L_Data=PageView(LectureData)
		else:
			L_Data=[[]]
			L_Data[0]=None
		PageInformation =[1,1,1]

		if Mobile =="full":
			PageInformation=FirstPageView(SearchCount)
			T_Count = PageTotalCount(SearchCount,PageInformation)
		else:
			PageInformation=MobileFirstPageView(SearchCount)
			T_Count = MobilePageTotalCount(SearchCount,PageInformation,3)

		request.session['SearchPageInformation'] = PageInformation
		request.session['SearchValue'] = SearchData

		dic = {
				'user':request.user,
				'BestBoard':BestBoardView(),
				'Search' : L_Data,
				'PageInformation' : PageInformation,
				'TotalCount':T_Count,
				'PageBoard':PageBoard,
				'TotalCountBoard':TotalEvalutionCount()
			}
		if request.flavour =='full':
			return render(request,'html/search.html',dic)
		else:
			return render(request,'m_skins/m_html/search.html', dic)
	else:
		return HttpResponseRedirect("/")
@csrf_protect
def SearchPage(request):#Search부분 ajax pagenation을 위해 만든 부분
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	Mobile = request.flavour
	if request.POST['Page'] !="0":
		cur_page = int(request.POST['Page'])
	else:
		cur_page = 1
		Current = request.POST['Current']

	SearchData = request.session['SearchValue']
	
	PageInformation = request.session['SearchPageInformation']

	if Mobile == 'full':
		DBCount = Total_Evaluation.objects.filter(Q(Course__CourseName__icontains=SearchData) | Q(Course__Professor__icontains=SearchData)).distinct().count()

		SearchCount = DataCount(10,DBCount)
	else :
		DBCount = Total_Evaluation.objects.filter(Q(Course__CourseName__icontains=SearchData) | Q(Course__Professor__icontains=SearchData)).distinct().count()
		SearchCount = DataCount(5,DBCount)
	
	if Mobile == 'full':
		PageInformation = CurrentPageView(SearchCount,cur_page)
		PageInformation[1]=cur_page
	else:
		PageInformation = MobileCurrentPageView(SearchCount,cur_page)
		PageInformation[1]=cur_page
	
	LectureData = [[]]
	TotalAdd=[]
	if Mobile == 'full':
		PageBoard=Total_Evaluation.objects.filter(Q(Course__CourseName__icontains=SearchData) | Q(Course__Professor__icontains=SearchData)).distinct()[(PageInformation[1]-1)*10:(PageInformation[1]-1)*10+10]
	else:
		PageBoard=Total_Evaluation.objects.filter(Q(Course__CourseName__icontains=SearchData) | Q(Course__Professor__icontains=SearchData)).distinct()[(PageInformation[1]-1)*5:(PageInformation[1]-1)*5+5]
	
	

	L_Data=PageView(LectureData)
	
	if Mobile == 'full':
		T_Count=PageTotalCount(SearchCount,PageInformation)
	else:
		T_Count=MobilePageTotalCount(SearchCount,PageInformation,3)

	request.session['SearchPageInformation'] = PageInformation
	
	dic = {
				'user':request.user,
				'BestBoard':BestBoardView(),
				'Search' : L_Data,
				'PageInformation' : PageInformation,
				'TotalCount' : T_Count,
				'PageBoard':PageBoard,
				'TotalCountBoard':TotalEvalutionCount()
			}
	if request.flavour =='full':
			return render(request,'html/searchpage.html',dic)
	else:
			return render(request,'m_skins/m_html/searchpage.html',dic )

@csrf_protect
def new_category_system(request):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	Dic={}
	for key in request.GET.keys():
		Dic[key] =request.GET[key]
	
	major = Dic['major'] != "0" and Dic['major'] or ""
	category = Dic['category'] != "0" and Dic['category'] or ""

	ordered = Dic['ordered'] != "0" and Dic['ordered'] or "최신순"
	orderdata=''
	if(ordered=="최신순"):
		orderdata='Total_Count'
	else:
		orderdata='-Total_Count'
	if(major!="" and category !=""):
		PageBoard=Total_Evaluation.objects.filter(Course__Major__contains=major,Course__Category__contains=category).order_by(orderdata)[0:10]
	elif major=="":
		PageBoard=Total_Evaluation.objects.filter(Course__Category__contains=category).order_by(orderdata)[0:10]
	elif category=="":
		PageBoard=Total_Evaluation.objects.filter(Course__Major__contains=major).order_by(orderdata)[0:10]
	DBCount=Total_Evaluation.objects.count()
	PCount = DataCount(10,DBCount)
	PageInformation = FirstPageView(PCount)
	T_Count = PageTotalCount(PCount,PageInformation)
	dic = {
		'PageBoard':PageBoard,
		'TotalCount':T_Count,
		'PageInformation':PageInformation,
		'major':major,
		'category':category,
	}

	if request.flavour =='full':
			return render(request,'html/page.html',dic)
	else:
			return render(request,'m_skins/m_html/page.html',dic )

@csrf_protect
def category_system(request):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	category_number = request.GET['category_number']

	if category_number == '1':
		category_name="학부"
		category_list =['국제어문','언론정보','경영경제','법학부','상담심리','생명과학','전산전자','콘텐츠융합디자인','기계제어','공간환경','ICT창업','창의융합교육원(인문사회)','창의융합교육원(이공)']
		subject_list = Lecture.objects.filter(Major__icontains='국제어문').values("Code","CourseName").distinct()
	elif category_number =='2':
		category_name="일반기초교양"
		category_list = ['신앙1','인성1','세계관1','세계관2','신앙3','예술','전공기초','사회과학','자연과학','리더십및문제해결','스포츠','기독교신앙기초1','기독교신앙기초2','영어1','영어2']
		subject_list = Lecture.objects.filter(CategoryDetail__icontains='신앙1').values("Code","CourseName").distinct()
	elif category_number =='3':
		category_name="글로벌"
		category_list = ['제2외국어','한국어','소통','융복합','프로그래밍기초','소프트웨어활용','ICT입문','특론및개별연구']
		subject_list=Lecture.objects.filter(CategoryDetail__icontains='제2외국어').values("Code","CourseName").distinct()
	else:
		pass
	dic = {
		'category_list':category_list,
		'category_name':category_name,
		'subject_list':subject_list
	}
	if request.flavour =='full':
			return render(request,'html/category_list.html',dic)
	else:
			return render(request,'m_skins/m_html/category_list.html',dic )
def select_subject_list(request):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")

	category_number = request.GET['category_number']
	category_select_name = request.GET['category_name']

	if category_number == '1':
		category_name="학부"
		category_list =['국제어문','언론정보','경영경제','법학부','상담심리','생명과학','전산전자','콘텐츠융합디자인','기계제어','공간환경','ICT창업','창의융합교육원(인문사회)','창의융합교육원(이공)']
		subject_list = Lecture.objects.filter(Major__icontains=category_select_name).values("Code","CourseName").distinct()
	elif category_number =='2':
		category_name="일반기초교양"
		category_list = ['신앙1','인성1','세계관1','세계관2','신앙3','예술','전공기초','사회과학','자연과학','리더십및문제해결','스포츠','기독교신앙기초1','기독교신앙기초2','영어1','영어2']
		subject_list = Lecture.objects.filter(CategoryDetail__icontains=category_select_name).values("Code","CourseName").distinct()
	elif category_number =='3':
		category_name="글로벌"
		category_list = ['제2외국어','한국어','소통','융복합','프로그래밍기초','소프트웨어활용','ICT입문','특론및개별연구']
		subject_list=Lecture.objects.filter(CategoryDetail__icontains=category_select_name).values("Code","CourseName").distinct()
	else:
		pass
	dic = {
		'category_list':category_list,
		'category_name':category_name,
		'subject_list':subject_list
	}
	if request.flavour =='full':
			return render(request,'html/category_list.html',dic)
	else:
			return render(request,'m_skins/m_html/category_list.html',dic )
# Create your views here
def search_subject_list(request):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	Mobile = request.flavour
	subject_code = request.GET['subject_category']
	subject = subject_code.split('-')
	TotalAdd=[]

	"""
	밑의 알고리즘은 현재 DB에 등록 되어있는 강의 이름을 토대로 group by로 묶어서 중복되는 강의이름을 하나로 묶어 버린후에
	그 강의이름 정보를 토대로 다시 DB에서 호출하는데 그 강의중 중복되는 정보만 추출하면 되는 거라 하나씩 불러서 그 부른 강의들을
	list화 시킴. 그리고 나서 그 list화 시킨 강의 정보를 다시 전체 평가 한 강의 부분 DB에서 다시 호출해 강의마다 평가된 
	평가 갯수를 다 더해서 함
	ps)물론 DB하나 더 만들면 더 간단한 알고리즘이 되겠지만 어차피 DB에서 한번더 불러야 하는건 마찬가지라 속도가 비슷할 거같아서
	안만듬
	"""
			
			
	LectureData=[[]]
	SearchResult = Lecture.objects.filter(Code=subject[0], CourseName=subject[1]).values("Code").distinct()[0:10]
	for lec in SearchResult:
						A=Lecture.objects.filter(Code=lec['Code'])
						LectureData[0].append(A[0])
						total=0	
						
						try:
								Eval=Total_Evaluation.objects.filter(Course__Code=lec['Code'])
								for Ev in Eval:
									total += Ev.Total_Count  
						except:
							continue
						TotalAdd.append(total)
	if Mobile == "full":
		DBCount = Lecture.objects.filter(Q(Code=subject[0]) | Q(CourseName=subject[1])).values("Code").distinct().count()
		SearchCount=DataCount(10,DBCount)
	else:
		DBCount = Lecture.objects.filter(Q(Code=subject[0]) | Q(CourseName=subject[1])).values("Code").distinct().count()
		SearchCount=DataCount(5,DBCount)
	
	if DBCount != 0 : 
		L_Data=PageView(LectureData)
	else:
		L_Data=[[]]
		L_Data[0]=None
	PageInformation =[1,1,1]

	if Mobile =="full":
		PageInformation=FirstPageView(SearchCount)
		T_Count = PageTotalCount(SearchCount,PageInformation)
	else:
		PageInformation=MobileFirstPageView(SearchCount)
		T_Count = MobilePageTotalCount(SearchCount,PageInformation,3)

	request.session['SearchPageInformation'] = PageInformation

	dic = {

				'PageInformation' : PageInformation,
				'user':request.user,
				'SubjectList':L_Data,
				'TotalAdd':TotalAdd,
				'TotalCount':T_Count
			}
	if request.flavour =='full':
		return render_to_response('html/Search_Category_Page.html',dic)
	else:
		return render_to_response('m_skins/m_html/Search_Category_Page.html',dic)
def search_subject_page(request):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	Mobile = request.flavour
	if request.GET['Page'] !="0":
		cur_page = int(request.GET['Page'])
	else:
		cur_page = 1
		Current = request.GET['Current']

	Course = request.GET['Course']
	
	PageInformation = request.session['SearchPageInformation']

	if Mobile == 'full':
		DBCount = Lecture.objects.filter(Q(CourseName__icontains=Course)).values("Code").distinct().distinct().count()
		SearchCount = DataCount(10,DBCount)
	else :
		DBCount = Lecture.objects.filter(Q(CourseName__icontains=Course)).values("Code").distinct().count()
		SearchCount = DataCount(5,DBCount)
	
	if Mobile == 'full':
		PageInformation = CurrentPageView(SearchCount,cur_page)
		PageInformation[1]=cur_page
	else:
		PageInformation = MobileCurrentPageView(SearchCount,cur_page)
		PageInformation[1]=cur_page
	
	LectureData = [[]]
	TotalAdd=[]
	if Mobile == 'full':
		temp=Lecture.objects.filter(Q(CourseName__icontains=Course)).values("Code").distinct()[(PageInformation[1]-1)*10:(PageInformation[1]-1)*10+10]
	else:
		temp=Lecture.objects.filter(Q(CourseName__icontains=Course)).values("Code").distinct()[(PageInformation[1]-1)*5:(PageInformation[1]-1)*5+5]
	LecList=[]
	for lec in temp:
				A=Lecture.objects.filter(Code=lec['Code'])
				LectureData[0].append(A[0])
				
				total=0	
				
				try:
						Eval=Total_Evaluation.objects.filter(Course__Code=lec['Code'])
						for Ev in Eval:
							total += Ev.Total_Count  
				except:
					continue
				TotalAdd.append(total)

	L_Data=PageView(LectureData)
	
	if Mobile == 'full':
		T_Count=PageTotalCount(SearchCount,PageInformation)
	else:
		T_Count=MobilePageTotalCount(SearchCount,PageInformation,3)

	request.session['SearchPageInformation'] = PageInformation
	
	dic = {
				'user':request.user,
				'BestBoard':BestBoardView(),
				'Search' : L_Data,
				'PageInformation' : PageInformation,
				'TotalCount' : T_Count,
				'TotalAdd':TotalAdd,
				'TotalCountBoard':TotalEvalutionCount()
			}
	if request.flavour =='full':
			return render(request,'html/SearchPage.html',dic)
	else:
			return render(request,'m_skins/m_html/SearchPage.html',dic )
'''
def GroupTotalCountRenew(request):
	if not request.user.username=='admin_seal':
		return HttpResponseRedirect('/')

	Total_Eval_List = Total_Evaluation.objects.all()
	Group_Total_Evaluation.objects.all().delete()
	for Total_Eval in Total_Eval_List:
		try:
			Group_Total = Group_Total_Evaluation.objects.get(CourseName = Total_Eval.Course.CourseName,Code = Total_Eval.Course.Code)
		except:
			Group_Total=None
		if Group_Total is None:
			Group_Total = Group_Total_Evaluation(CourseName = Total_Eval.Course.CourseName,
				Code = Total_Eval.Course.Code,GroupTotalCount=Total_Eval.Total_Count)
		else:
			Group_Total.GroupTotalCount +=Total_Eval.Total_Count
		Group_Total.save()
	return HttpResponseRedirect("/")

def renewDB(request):
	#이건 되도록 쓰지마세요
	if not request.user.username=='admin_seal':
		return HttpResponseRedirect('/')

	Course_EvalList = Course_Evaluation.objects.all()
	for Course_Eval in Course_EvalList:
		if Course_Eval.What_Answer == 1:
			Course_Eval.What_Answer =1000
		elif Course_Eval.What_Answer == 2:
			Course_Eval.What_Answer = 100
		elif Course_Eval.What_Answer ==3 :
			Course_Eval.What_Answer=10
		elif Course_Eval.What_Answer ==4 :
			Course_Eval.What_Answer =5
		if Course_Eval.Course_Answer == 1:
			Course_Eval.Course_Answer =100
		elif Course_Eval.Course_Answer == 2:
			Course_Eval.Course_Answer = 10
		elif Course_Eval.Course_Answer ==3 :
			Course_Eval.Course_Answer=5
		Course_Eval.save()
	Lecture_List = Lecture.objects.all().order_by("Semester")
	Total_Eval_List = Total_Evaluation.objects.all().delete()
	for lec in Lecture_List:
		pro = lec.Professor.split("외")!=None and lec.Professor.split("외")[0] or lec.Professor
		pro = pro.split("외")!=None and pro.split("외")[0] or pro

		lec.save()
		temp_total= Total_Evaluation.objects.filter(Course__Code=lec.Code,Course__CourseName=lec.CourseName,Course__Professor__contains=pro).count()
		if(temp_total ==0):
			new_lec = Lecture.objects.filter(Code=lec.Code,CourseName=lec.CourseName,Professor__contains=pro).order_by("Semester")[0]
			Total_Evaluation(Course=new_lec).save()

	'''
	for Course_Eval in Course_EvalList:
		Course_Professor = Course_Eval.Course.Professor.split("외")[0] !=None and Course_Eval.Course.Professor.split("외")[0] or Course_Eval.Course.Professor
		Course_Code = Course_Eval.Course.Code
		Course_CourseName = Course_Eval.Course.CourseName
		LectureObject=Lecture.objects.filter(Code=Course_Code, Professor__contains=Course_Professor, CourseName=Course_CourseName).order_by("Semester")[0]
		Course_Eval.Course = LectureObject
		Course_Eval.save()
	'''
	
	for Course_Eval in Course_EvalList:
		temp_pro=Course_Eval.Course.Professor.split("외")[0] != None and Course_Eval.Course.Professor.split("외")[0] or Course_Eval.Course.Professor
		Course_Professor = temp_pro.split("외")[0] != None and temp_pro.split("외")[0] or temp_pro
		
		Total_Eval = Total_Evaluation.objects.get(Course__Code=Course_Eval.Course.Code, Course__Professor__contains=Course_Professor,Course__CourseName=Course_Eval.Course.CourseName)
		
	
		Total_Professor = Total_Eval.Course.Professor.split("외")[0] != None and Total_Eval.Course.Professor.split("외")[0] or Total_Eval.Course.Professor
		if Total_Eval.Course.CourseName ==Course_Eval.Course.CourseName and Total_Eval.Course.Code ==Course_Eval.Course.Code and Total_Professor == Course_Professor:
			Total_Eval.Total_Homework+=Course_Eval.Homework
			Total_Eval.Total_Level_Difficulty+=Course_Eval.Level_Difficulty
			Total_Eval.Total_Count += 1
			Total_Eval.Total_StarPoint+=Course_Eval.StarPoint
			if Course_Eval.Check ==True:
				Total_Eval.Total_Recommend +=1

			if Course_Eval.What_Answer-1000 >=0:
				Total_Eval.Total_Long_Answer +=1				
			elif Course_Eval.What_Answer%1000-100 >=0:
				Total_Eval.Total_Short_Answer+=1
			elif Course_Eval.What_Answer%100-10 >=0:
				Total_Eval.Total_Mix+=1
			elif Course_Eval.What_Answer%10-1 >=0:
				Total_Eval.Total_Unknown_Answer+=1
			
			if Course_Eval.Course_Answer%1000-100>=0:
				Total_Eval.Total_Book_Like+=1
			elif Course_Eval.Course_Answer%100-10 >=0:
				Total_Eval.Total_Ppt_Like+=1
			elif Course_Eval.Course_Answer%10-1>=0:
				Total_Eval.Total_Practice_Like+=1
		
		Total_Eval.save()
		Course_Eval.Total_Course_id=Total_Eval.id
		Course_Eval.save() 

	return HttpResponseRedirect("/")
def renewTableCount(request):
	if not request.user.username=='admin_seal':
		return HttpResponseRedirect('/')

	Course_Eval=Course_Evaluation.objects
	Count=CountTable.objects.count()
	if Count==0:
		CTable=CountTable(TotalCount=Course_Eval.count())
	else:
		CTable = CountTable.objects.all()[0:1]
		

	CourseList=Course_Eval.all()
	GLS = 0
	ISL = 0
	ME = 0
	SOF = 0
	SOCAS = 0
	SESE =0
	MCE = 0
	CCD = 0
	LS = 0
	CSEE = 0
	CPSW = 0
	ICT = 0
	SCCE = 0
	for Course in CourseList:
		Code = Course.Course.Code[0:3]
		if Code == "ENG" or Code == "GEK" or Code == "GCS" or Code == "PCO" or Code == "ISL" or Code == "PST":
			GLS += 1
		elif Code =="ISE":
			ISL += 1
		elif Code =="GMP" or Code == "MEC":
			ME += 1
		elif Code =="LAW" or Code == "UIL":
			SOF +=1
		elif Code =="CCC":
			SOCAS += 1
		elif Code =="CUE":
			SESE +=1
		elif Code =="HMM":
			MCE += 1
		elif Code =="IID":
			CCD +=1
		elif Code =="BFT":
			LS += 1
		elif Code =="ECE" or Code =="ITP":
			CSEE+=1
		elif Code =="CSW":
			CPSW +=1
		elif Code =="SIE":
			ICT +=1
		elif Code =="SIE":
			SCEE+=1
	if Count==0:
		CTable.GLS=GLS 
		CTable.ISL=ISL
		CTable.ME=ME 
		CTable.SOF=SOF 
		CTable.SOCAS=SOCAS 
		CTable.SESE=SESE 
		CTable.MCE=MCE 
		CTable.CCD=CCD 
		CTable.LS=LS
		CTable.CSEE=CSEE 
		CTable.CPSW=CPSW
		CTable.ICT=ICT 
		CTable.SCCE=SCCE
		CTable.save()
	else:
		for C in CTable:
			C.TotalCount= Course_Eval.count()
			C.GLS=GLS 
			C.ISL=ISL
			C.ME=ME 
			C.SOF=SOF 
			C.SOCAS=SOCAS 
			C.SESE=SESE 
			C.MCE=MCE 
			C.CCD=CCD 
			C.LS=LS
			C.CSEE=CSEE 
			C.CPSW=CPSW
			C.ICT=ICT 
			C.SCCE=SCCE
			C.save()

	return HttpResponseRedirect("/")
def ShowEvent(request):
	if not request.user.username=='admin_seal':
		return HttpResponseRedirect('/')
	Course_Eval =Course_Evaluation.objects.filter().values("CreatedID__User__username","CreatedID__UserName","CreatedID__RecommendCount").annotate(countId=Count("id")).filter(countId__gte=6)
	return render(request,"html/event.html",{"GG":Course_Eval,"Count":Course_Eval.count()})

def MajorSelect(user):
		try:
			Student = Profile.objects.get(User =user)
		except:
			return None
		MajorCode= [[],[],[],[],[],[]]	
		FirstMajor = str(Student.FirstMajor)
		SecondMajor = str(Student.SecondMajor)
			#1전공 선택 하는 조건문
		if FirstMajor.find("국제") != -1 or FirstMajor.find("영어") != -1:
			MajorCode[0]="ISE"
			MajorCode[1]="None"
		elif FirstMajor.find("경영학") != -1 or FirstMajor.find("경제학")!= -1 or FirstMajor.find("GM")!= -1:
			MajorCode[0]="GMP"
			MajorCode[1]="MEC"
		elif FirstMajor.find("한국법") != -1 or FirstMajor.find("UIL")!= -1:
			MajorCode[0]="LAW"
			MajorCode[1]="UIL"
		elif FirstMajor.find("공연영상")!= -1 or FirstMajor.find("언론정보학")!= -1:
			MajorCode[0]="CCC"
			MajorCode[1]="None"
		elif FirstMajor.find("건설공학") != -1 or FirstMajor.find("도시환경")!= -1:
			MajorCode[0]="CUE"
			MajorCode[1]="None"
		elif FirstMajor.find("기계공학")!= -1 or FirstMajor.find("전자제어")!= -1 or FirstMajor.find("기전공학")!=-1:
			MajorCode[0]="HMM"
			MajorCode[1]="None"
		elif FirstMajor.find("시각디자인")!= -1 or FirstMajor.find("제품디자인")!= -1:
			MajorCode[0]="IID"
			MajorCode[1]="None"
		elif FirstMajor.find("생명과학")!= -1:
			MajorCode[0]="BFT"
			MajorCode[1]="None"
		elif FirstMajor.find("컴퓨터") != -1 or FirstMajor.find("전자") != -1:
			MajorCode[0]="ECE"
			MajorCode[1]="ITP"
		elif FirstMajor.find("상담심리") != -1 or FirstMajor.find("사회복지")!= -1:
			MajorCode[0]="CSW"
			MajorCode[1]="None"
		#elif FirstMajor.find("global")!= -1 :
	#		MajorCode[0]="GEA"
	#		MajorCode[1]="None"
		elif FirstMajor.find("영어학과")!= -1 or FirstMajor.find("경영학과")!= -1 or FirstMajor.find("사회복지학과")!= -1:
			MajorCode[0]="SIE"
			MajorCode[1]="None"
		elif FirstMajor==None :
			MajorCode[2]="None"
			MajorCode[3]="None"
			MajorCode[4]="None"
			MajorCode[5]="None"
		else:
			MajorCode[0]="ENG"
			MajorCode[1]="GEK"
			MajorCode[2]="GCS"
			MajorCode[3]="PCO"
			MajorCode[4]="ISL"
			MajorCode[5]="PST"

		if SecondMajor.find("국제")!=-1 or SecondMajor.find("영어")!=-1:
			MajorCode[2]="ISE"
			MajorCode[3]="None"
		elif SecondMajor.find("경영학")!=-1 or SecondMajor.find("경제학")!=-1 or SecondMajor.find("GM")!=-1:
			MajorCode[2]="GMP"
			MajorCode[3]="MEC"
		elif SecondMajor.find("한국법")!=-1 or SecondMajor.find("UIL")!=-1:
			MajorCode[2]="LAW"
			MajorCode[3]="UIL"
		elif SecondMajor.find("공연영상") !=-1 or SecondMajor.find("언로정보학")!=-1:
			MajorCode[2]="CCC"
			MajorCode[3]="None"
		elif SecondMajor.find("건설공학") !=-1 or SecondMajor.find("도시환경")!=-1:
			MajorCode[2]="CUE"
			MajorCode[3]="None"
		elif SecondMajor.find("기계공학")!=-1 or SecondMajor.find("전자제어")!=-1 or SecondMajor.find("기전공학")!=-1:
			MajorCode[2]="HMM"
			MajorCode[3]="None"
		elif SecondMajor.find("시각디자인")!=-1 or SecondMajor.find("제품디자인")!=-1:
			MajorCode[2]="IID"
			MajorCode[3]="None"
		elif SecondMajor.find("생명과학")!=-1:
			MajorCode[2]="BFT"
			MajorCode[3]="None"
		elif SecondMajor.find("컴퓨터")!=-1 or SecondMajor.find("전자")!=-1:
			MajorCode[2]="ECE"
			MajorCode[3]="ITP"
		elif SecondMajor.find("상담심리")!=-1 or SecondMajor.find("사회복지")!=-1:
			MajorCode[2]="CSW"
			MajorCode[3]="None"
		elif SecondMajor.find("global")!=-1:
			MajorCode[2]="GEA"
			MajorCode[3]="None"
		elif SecondMajor.find("영어학과") !=-1 or SecondMajor.find("경영학과") !=-1 or SecondMajor.find("사회복지학과")!=-1:
			MajorCode[2]="SIE"
			MajorCode[3]="None"
		elif SecondMajor==None :
			MajorCode[2]="None"
			MajorCode[3]="None"
			MajorCode[4]="None"
			MajorCode[5]="None"
		else:
			MajorCode[2]="GCS"
			MajorCode[3]="PCO"
			MajorCode[4]="ISL"
			MajorCode[5]="PST"
		return MajorCode

