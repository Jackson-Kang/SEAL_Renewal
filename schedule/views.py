# -*- coding: utf-8 -*-
# -*- coding: euc-kr -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.conf import settings
from lecture.models import *
from login.models import *
from functionhelper.views import *
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User	# user model 등록

cur_semester = '18-1'

# 시간표 선택시 검색 기능
@csrf_protect
def SelectPeriod(request, period, page):
	"""
	period -> 테이블에서 선택한 강의시간
	page -> pagination에서 선택한 page
	"""
	Mobile =request.flavour
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")

	elif request.method =="POST":
 		category = request.POST['category']
		major = request.POST['major']
		SearchName = request.POST['SearchName']
		Page = request.POST['Page']

		cur_page = int(page)
		start = 6 * (cur_page-1)
		end = 6 * cur_page

		SelectMajor=Major(major)
		SelectCategory=Category(category)
		if SelectMajor == "전체" :
			SelectMajor=""

		if SelectCategory=="전체":
			# Category 전체, NULL값까지 같이 찾음.
			# SelectCategory= ""
			if not period[1:3].isdigit():	# 1교시의 경우 10교시가 같이 나오는 것을 방지하기 위한 장치
				DBCount = Lecture.objects.filter(Major__contains=SelectMajor, CourseName__contains=SearchName, Semester=cur_semester, Period__contains=period[:-1]).exclude(Period__contains='10').count()
				lec_cnt = DataCount(6,DBCount)
				lec_lst = Lecture.objects.filter(Major__contains=SelectMajor, CourseName__contains=SearchName, Semester=cur_semester, Period__contains=period[:-1]).exclude(Period__contains='10')[start:end]
			else:
				DBCount = Lecture.objects.filter(Major__contains=SelectMajor, CourseName__contains=SearchName, Semester=cur_semester, Period__contains=period[:-1]).count()
				lec_cnt = DataCount(6,DBCount)
				lec_lst = Lecture.objects.filter(Major__contains=SelectMajor, CourseName__contains=SearchName, Semester=cur_semester, Period__contains=period[:-1])[start:end]
		else:
			# Category가 있는 경우
			if not period[1:3].isdigit():	# 1교시의 경우 10교시가 같이 나오는 것을 방지하기 위한 장치
				DBCount = Lecture.objects.filter(Major__contains=SelectMajor, CategoryDetail__contains=SelectCategory, CourseName__contains=SearchName, Semester=cur_semester, Period__contains=period[:-1]).exclude(Period__contains='10').count()
				lec_cnt = DataCount(6,DBCount)
				lec_lst = Lecture.objects.filter(Major__contains=SelectMajor, CategoryDetail__contains=SelectCategory, CourseName__contains=SearchName, Semester=cur_semester, Period__contains=period[:-1]).exclude(Period__contains='10')[start:end]
			else:
				DBCount = Lecture.objects.filter(Major__contains=SelectMajor, CategoryDetail__contains=SelectCategory, CourseName__contains=SearchName, Semester=cur_semester, Period__contains=period[:-1]).count()
				lec_cnt = DataCount(6,DBCount)
				lec_lst = Lecture.objects.filter(Major__contains=SelectMajor, CategoryDetail__contains=SelectCategory, CourseName__contains=SearchName, Semester=cur_semester, Period__contains=period[:-1])[start:end]

		total_page = ( (lec_cnt - 1) / 6 ) + 1
		is_odd = lec_cnt % 2

		total = [lec_lst]
		TotalBoard = PageView(total)
		if Mobile =="full":
				PageInformation = FirstPageView(lec_cnt)
		else:
				PageInformation = MobileFirstPageView(lec_cnt)
		PageInformation[1]=cur_page
		my_profile = Profile.objects.filter(User_id=request.user.id)[0]
		my_lec_table = MakeTable(request, my_profile)
		ctx = {
			'user':request.user,
			'period':period,
			'total_page': Mobile == "full" and PageTotalCount(lec_cnt,PageInformation) or MobilePageTotalCount(lec_cnt,PageInformation,3),
			'lec_lst':lec_lst,
			'is_odd':is_odd,
			'cur_page':cur_page,
			'TotalBoard':TotalBoard,
			"my_lec_table": my_lec_table,
			"my_profile": my_profile,
			"PageInformation":PageInformation,
			'BestBoard':BestBoardView(),
			'SelectMajor':major,
			'SelectCategory':category,
			'SearchName':SearchName,
			'TotalCountBoard':TotalEvalutionCount()
		
		}

		# request.session['cur_page'] = cur_page + 1
		if request.flavour =='full':
			return render(request,'html/scheduleSearch.html',ctx)
		else:
			return render(request,'m_skins/m_html/scheduleSearch.html', ctx)

@csrf_protect
def SearchSelectPeriod(request):
	"""
	period -> 테이블에서 선택한 강의시간
	page -> pagination에서 선택한 page
	"""
	Mobile = request.flavour
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	elif request.method=="POST":
		period = request.POST['Period']
		cur_page = int(request.POST['Page'])
		major = request.POST['SelectMajor']
		category = request.POST['SelectCategory']
		SearchName = request.POST['SearchName']
		# cur_page = request.session['cur_page']

		start = 6 * (cur_page-1)
		end = 6 * cur_page

		SelectMajor=Major(major)
		SelectCategory=Category(category)
		if SelectMajor == "전체" :
			SelectMajor=""

		if SelectCategory=="전체":
			# Category 전체, NULL값까지 같이 찾음.
			# SelectCategory= ""
			if not period[1:3].isdigit():	# 1교시의 경우 10교시가 같이 나오는 것을 방지하기 위한 장치
				DBCount = Lecture.objects.filter(Major__contains=SelectMajor, CourseName__contains=SearchName, Semester=cur_semester, Period__contains=period[:-1]).exclude(Period__contains='10').count()
				lec_cnt = DataCount(6,DBCount)
				lec_lst = Lecture.objects.filter(Major__contains=SelectMajor, CourseName__contains=SearchName, Semester=cur_semester, Period__contains=period[:-1]).exclude(Period__contains='10')[start:end]
			else:
				DBCount = Lecture.objects.filter(Major__contains=SelectMajor, CourseName__contains=SearchName, Semester=cur_semester, Period__contains=period[:-1]).count()
				lec_cnt = DataCount(6,DBCount)
				lec_lst = Lecture.objects.filter(Major__contains=SelectMajor, CourseName__contains=SearchName, Semester=cur_semester, Period__contains=period[:-1])[start:end]
		else:
			# Category가 있는 경우
			if not period[1:3].isdigit():	# 1교시의 경우 10교시가 같이 나오는 것을 방지하기 위한 장치
				DBCount = Lecture.objects.filter(Major__contains=SelectMajor, CategoryDetail__contains=SelectCategory, CourseName__contains=SearchName, Semester=cur_semester, Period__contains=period[:-1]).exclude(Period__contains='10').count()
				lec_cnt = DataCount(6,DBCount)
				lec_lst = Lecture.objects.filter(Major__contains=SelectMajor, CategoryDetail__contains=SelectCategory, CourseName__contains=SearchName, Semester=cur_semester, Period__contains=period[:-1]).exclude(Period__contains='10')[start:end]
			else:
				DBCount = Lecture.objects.filter(Major__contains=SelectMajor, CategoryDetail__contains=SelectCategory, CourseName__contains=SearchName, Semester=cur_semester, Period__contains=period[:-1]).count()
				lec_cnt = DataCount(6,DBCount)
				lec_lst = Lecture.objects.filter(Major__contains=SelectMajor, CategoryDetail__contains=SelectCategory, CourseName__contains=SearchName, Semester=cur_semester, Period__contains=period[:-1])[start:end]
		total_page = ( (lec_cnt - 1) / 6 ) + 1
		is_odd = lec_cnt % 2

		total = [lec_lst]
		TotalBoard = PageView(total)
		if Mobile =="full":
				PageInformation = CurrentPageView(lec_cnt,cur_page)
		else :
				PageInformation =MobileCurrentPageView(lec_cnt,cur_page)
		PageInformation[1]=cur_page
		my_profile = Profile.objects.filter(User_id=request.user.id)[0]
		my_lec_table = MakeTable(request, my_profile)

		ctx = {
			'user':request.user,
			'period':period,
			'total_page': Mobile == "full" and PageTotalCount(lec_cnt,PageInformation) or MobilePageTotalCount(lec_cnt,PageInformation,3),
			'lec_lst':lec_lst,
			'is_odd':is_odd,
			'cur_page':cur_page,
			'TotalBoard':TotalBoard,
			"my_lec_table": my_lec_table,
			"my_profile": my_profile,
			"PageInformation" : PageInformation,
			'BestBoard':BestBoardView(),
			'SelectMajor':major,
			'SelectCategory':category,
			'SearchName':SearchName,
			'TotalCountBoard':TotalEvalutionCount()
		}

		# request.session['cur_page'] = cur_page + 1
		if request.flavour =='full':
			return render(request,'html/scheduleSearch.html',ctx)
		else:
			return render(request,'m_skins/m_html/scheduleSearch.html', ctx)

def MakeTable(request, my_profile):
	## 나의 강의목록 불러오기
	my_lec_lst = my_profile.MyLecture.all()
	
	# empty list로 채워진 11*6 size Table 생성
	my_lec_table = []
	for i in range(11):
		my_lec_table.append([])
		for j in range(6):
			my_lec_table[i].append([])

	# days_dic = {u"월":0, u"화":1, u"수":2, u"목":3, u"금":4, u"토":5}
	days_dic = {u"Mon":0, u"Tue":1, u"Wed":2, u"Thu":3, u"Fri":4, u"Sat":5}

	# 나의 강의정보 테이블 별로 삽입하기. 중복 확인 필수.
	for lec in my_lec_lst:
		# lec_info_lst = (lec.CourseName, lec.Class, lec.Professor, lec.ClassRoom,)
		p_lst = lec.Period.split(",")
		for period in p_lst:
			if period == "":
				break;
			day = days_dic[period[:3]]	# 0번째 값은 요일, ex) "월" -> 0
			my_lec_table[int(period[3:])-1][day] = lec	# -1(index계산), 나머지는 교시, 10교시 이상 있을 수 있음 주의.

	return my_lec_table

@csrf_protect
def SelectLecture(request):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")

	if request.method == "POST":
		ccode = request.POST['ccode']
		cname = request.POST['cname']
		cprof = request.POST['cprof']
		cperiod = request.POST['cperiod']
		
		## period 없는 경우 예외처리(ex. 사회봉사 등)

		## 나의 강의목록 추가하기
		my_profile = Profile.objects.filter(User_id=request.user.id)[0]
		is_duplicated = False
		split_period = cperiod.split(",")
		my_lec_lst = my_profile.MyLecture.all()
		my_lec_period_lst = []
		for lec in my_lec_lst:
			p_lst = lec.Period.split(",")
			for period in p_lst:
				my_lec_period_lst.append(period)	# 나의 강의목록 시간 모두 리스트로 작성
		for p in split_period:
			if p in my_lec_period_lst:
				is_duplicated = True	# 나의 강의목록 시간 중에 중복되는 시간 있을 시 True.
		if is_duplicated:	# 중복될 시 바로 return 처리, confirm 처리 추후 개발
			# my_lec = Lecture.objects.filter(Code=ccode, Professor=cprof, Period=cperiod)[0]
			my_lec_table = MakeTable(request, my_profile)

			Dic = {
			"my_lec_table": my_lec_table,
			'BestBoard':BestBoardView(),'TotalCountBoard':TotalEvalutionCount()
		
			}
			if request.flavour =='full':
				return render(request,'html/scheduleTable.html',Dic)
			else:
				return render(request,'m_skins/m_html/scheduleTable.html',Dic)
		if cprof == "None":
			cprof = None
		# Unique한 value를 위한 Key = (Code, Class, Semester) or (Code, Prof, Period, Semster) -> but, prof=null 일 경우 중복에러 가능
		my_lec = Lecture.objects.filter(Semester=cur_semester, Code=ccode, Professor=cprof, Period=cperiod)[0]
		my_profile.MyLecture.add(my_lec)
		my_profile.save()
		my_lec_table = MakeTable(request, my_profile)

		Dic = {
			"my_lec_table": my_lec_table,
			'BestBoard':BestBoardView(),'TotalCountBoard':TotalEvalutionCount()

		
		}
		if request.flavour =='full':
				return render(request,'html/scheduleTable.html',Dic)
		else:
				return render(request,'m_skins/m_html/scheduleTable.html', Dic)

@csrf_protect
def RemoveLecture(request):
	CheckingLogin(request.user.username)

	if request.method == "POST":
		ccode = request.POST['ccode']
		cclass = request.POST['cclass'][1:-1]
		## period 없는 경우 예외 처리(ex. 사회봉사 등)

		## 나의 강의목록 제거하기
		my_profile = Profile.objects.filter(User_id=request.user.id)[0]

		my_lec = Lecture.objects.filter(Code=ccode, Class=cclass, Semester=cur_semester)[0]
		my_profile.MyLecture.remove(my_lec)
		my_profile.save()
		my_lec_table = MakeTable(request, my_profile)

		Dic = {
			"my_lec_table": my_lec_table,
		}
		if request.flavour =='full':
				return render(request,'html/scheduleTable.html',Dic)
		else:
			return render(request,'m_skins/m_html/scheduleTable.html', Dic)


@csrf_protect
def SearchSubject(request):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	Mobile =request.flavour
 	if request.method =="POST":
 		PostDic=dict()
 		for key in request.POST.keys():
	 		PostDic[key] = request.POST[key]
		if PostDic['Page'] !="0":
			PostDic['Page'] = int(PostDic['Page']) 		
			New=0
		else:
			PostDic['Page'] = 1
			New =1
		#cur_page = int(offset)

		start = 6 *(PostDic['Page']-1)
		end = 6 * (PostDic['Page'])

		SelectMajor=Major(PostDic['major'])
		SelectCategory=Category(PostDic['category'])
		if SelectMajor == "전체" :
			SelectMajor=""

		if SelectCategory=="전체":
			# SelectCategory= ""
			DBCount = Lecture.objects.filter(Major__contains=SelectMajor, CourseName__contains=PostDic['SearchName'], Semester=cur_semester).count()
			SubjectCount = DataCount(6,DBCount)
			Subject = Lecture.objects.filter(Major__contains=SelectMajor, CourseName__contains=PostDic['SearchName'], Semester=cur_semester)[start:end]
		else:
			DBCount = Lecture.objects.filter(Major__contains=SelectMajor, CategoryDetail__contains=SelectCategory, CourseName__contains=PostDic['SearchName'], Semester=cur_semester).count()
			SubjectCount = DataCount(6,DBCount)
			Subject = Lecture.objects.filter(Major__contains=SelectMajor, CategoryDetail__contains=SelectCategory, CourseName__contains=PostDic['SearchName'], Semester=cur_semester)[start:end]

		if New == 1:
			if Mobile == "full":
					PageInformation = FirstPageView(SubjectCount)
					TotalCount=PageTotalCount(SubjectCount,PageInformation)
			else :
					PageInformation = MobileFirstPageView(SubjectCount)
					TotalCount=MobilePageTotalCount(SubjectCount,PageInformation,3)
		else :
			if Mobile =="full":
					PageInformation = CurrentPageView(SubjectCount,PostDic['Page'])
					PageInformation[1]=PostDic['Page']
					TotalCount = PageTotalCount(SubjectCount,PageInformation)
			else:
					PageInformation = MobileCurrentPageView(SubjectCount,PostDic['Page'])
					PageInformation[1]=PostDic['Page']
					TotalCount = MobilePageTotalCount(SubjectCount,PageInformation,3)
				
		TotalBoard = PageView([Subject])
		my_profile = Profile.objects.filter(User_id=request.user.id)[0]
		my_lec_table = MakeTable(request, my_profile)
		Dic = {
				'user':request.user,
				'Subject':Subject,
				'SelectMajor' : SelectMajor,
				'SubjectCount':SubjectCount,
				'SearchName':PostDic['SearchName'],
				'PageInformation':PageInformation,
				'total_page':TotalCount,
				'cur_page':PostDic['Page'],
				"my_lec_table": my_lec_table,
				"my_profile": my_profile,
				"TotalBoard": TotalBoard,
				'BestBoard':BestBoardView(),
				'TotalCountBoard':TotalEvalutionCount()
		}
		if request.flavour =='full':
			return render(request,'html/scheduleTemplate.html',Dic)
		else:
			return render(request,'m_skins/m_html/scheduleTemplate.html', Dic)
	else:
		my_profile = Profile.objects.filter(User_id=request.user.id)[0]
		my_lec_table = MakeTable(request, my_profile)
		Dic = {
				'user': request.user,
				"my_lec_table": my_lec_table,
				"my_profile": my_profile,
				'BestBoard':BestBoardView(),
				'TotalCountBoard':TotalEvalutionCount()
		}
		if request.flavour =='full':
			return render(request,'html/schedule.html',Dic)
		else:
			return render(request,'m_skins/m_html/schedule.html', Dic)

@csrf_protect
def DeleteMylecture(request):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")

	if request.method =="POST":
		code = request.POST['ccode']
		course = request.POST['cname']
		prof = request.POST['cprof']
	UserData =Profile.objects.get(User=request.user)
	UserData.MyLecture.filter(Code=code, Professor=prof, CourseName=course)[0].delete()
	UserData.save()
	my_lec_table = MakeTable(request, UserData)
	if request.flavour =='full':
		return render(request,'html/scheduleTable.html',{"my_lec_table": my_lec_table})
	else:
		return render(request,'m_skins/m_html/scheduleTable.html',{"my_lec_table": my_lec_table})

def Major(major):
	if major == "0001":
		major = "글로벌"
	elif major == "0009":
		major = "창의융합"
	elif major == "0010":
		major = "Global EDISON"
	elif major == "0011":
		major = "국제어문"
	elif major == "0012":
		major = "언론정보"
	elif major == "0021":
		major = "경영경제"
	elif major == "0022":
		major = "법학부"
	elif major =="0024":
		major = "상담심리"
	elif major =="0033":
		major = "생명과학"
	elif major == "0071":
		major = "전산전자"
	elif major == "0074":
		major = "산업디자인"
	elif major == "0077":
		major = "기계제어"
	elif major == "0078":
		major = "공간환경"
	elif major == "0079":
		major = "콘텐츠융합"
	elif major == "0090":
		major = "산업교육"
	else:
		major = "전체"

	return major
def Category(category):
	if category == "W04":
		category = "신앙1"
	elif category == "W05":
		category = "인성1"
	elif category == "W06":
		category = "인성2"
	elif category == "W07":
		category = "신앙2"
	elif category == "W08":
		category = "세계관1"
	elif category == "W09":
		category = "세계관2"
	elif category == "W10":
		category = "인문"
	elif category == "W11":
		category = "역사"
	elif category == "W12":
		category = "사회"
	elif category == "W13":
		category = "수학"
	elif category == "W14":
		category = "자연"
	elif category == "W15":
		category = "신앙3"
	elif category == "W16":
		category = "리더십"
	elif category == "W17":
		category = "예술"
	elif category == "W18":
		category = "전공기초"
	elif category == "W19":
		category = "외국어"
	elif category == "W22":
		category = "전공탐색"
	elif category == "W24":
		category = "제2외국어"
	elif category == "W25":
		category = "소통및융복합"
	elif category == "W26":
		category = "ICT융합기초"
	elif category == "W27":
		category = "인문학"
	elif category == "W28":
		category = "사회과학"
	elif category == "W29":
		category = "자연과학"
	elif category == "W30":
		category = "리더십문제해결"
	elif category == "W31":
		category = "스포츠"
	elif category == "W32":
		category = "영어1"
	elif category == "W33":
		category = "영어2"
	elif category == "W34":
		category = "기독교신앙기초1"
	elif category == "W35":
		category = "기독교신앙기초2"
	elif category == "W50":
		category = "실무영어"
	elif category == "W51":
		category = "실무한문"
	elif category == "W52":
		category = "실무전산"
	elif category == "W53":
		category = "실무한국어"
	elif category == "X01":
		category = "야간-영어"
	elif category == "X02":
		category = "야간-경영학"
	elif category == "X03":
		category = "야간-실무"
	elif category == "X04":
		category = "야간-교양"
	elif category == "X06":
		category = "야간-실무전산"
	elif category == "X07":
		category = "야간-실무영어"
	elif category == "X08":
		category = "야간-실무한문"
	else:
		category = "전체"

	return category
		
