# -*- coding: utf-8 -*-
# -*- coding: euc-kr -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from index.models import *
from lecture.models import *
from mycourse.models import *
from django.views.decorators.csrf import csrf_protect
from functionhelper.views import *
import datetime

import sys

reload(sys)  
sys.setdefaultencoding('utf8')
#현재 내가 추천한 강의 보여주는 함수
def MyCourse(request):
		if CheckingLogin(request.user.username):
			return HttpResponseRedirect("/")
        
		Mobile = request.flavour
		Data=MyCoursePage(request,1,Mobile)
		if request.flavour =='full':
			return render(request,'html/mycourses.html',Data)
		else:
			return render(request,"m_skins/m_html/mycourses.html", Data)
#위의 함수 세부함수
def MyCoursePage(request,Page,Mobile):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	try:
		if Mobile == "full":
			PageFirst=10*(int(Page)-1)
			PageLast =10*(int(Page)-1)+10
		else:
			PageFirst=5*(int(Page)-1)
			PageLast =5*(int(Page)-1)+5	
	except:
		raise Http404()
	
	MyProfile = Profile.objects.get(User=request.user)
	

	RecommendPage=[]
	LikePage=[]
	
	Recommend = Recommend_Course.objects.filter(CreatedID = MyProfile)[PageFirst:PageLast]			
	
	for Board in Recommend:
			renew_professor=Board.Course.Course.Professor.split("외")[0] !=0 and Board.Course.Course.Professor.split("외")[0] or Board.Course.Course.Professor
			a=Lecture.objects.filter(Semester=Board.Course.Course.Semester,CourseName=Board.Course.Course.CourseName,Professor__contains = renew_professor, Code = Board.Course.Course.Code)[0]
			RecommendData =Total_Evaluation(Course =a)
			RecommendDataList = Total_Evaluation.objects.filter(Course__CourseName=Board.Course.Course.CourseName,Course__Professor__contains = renew_professor, Course__Code = Board.Course.Course.Code)
			for ReData in RecommendDataList:
				RecommendData.Total_Speedy+=ReData.Total_Speedy
				RecommendData.Total_Homework +=ReData.Total_Homework
				RecommendData.Total_Level_Difficulty+=ReData.Total_Level_Difficulty
				RecommendData.Total_StarPoint += ReData.Total_StarPoint
				RecommendData.Total_Count+= ReData.Total_Count
				RecommendData.Total_Recommend += ReData.Total_Recommend

			RecommendData.Total_Speedy=RecommendData.Total_Speedy/RecommendData.Total_Count
			RecommendData.Total_Homework =RecommendData.Total_Homework/RecommendData.Total_Count
			RecommendData.Total_Level_Difficulty=RecommendData.Total_Level_Difficulty/RecommendData.Total_Count
			RecommendData.Total_StarPoint = RecommendData.Total_StarPoint/RecommendData.Total_Count 
			RecommendData.id =Board.id
			RecommendData.Course.Professor=renew_professor

			RecommendPage.append(RecommendData)	
			
	Like=Like_Course.objects.filter(CreatedID = MyProfile)[PageFirst:PageLast]

	for Board2 in Like:
			try :
					LikeData=Total_Evaluation.objects.get(Course=Board2.Course)
			except:
					LikeData = Total_Evaluation(Course =Board2.Course)
					LikeData.Total_Speedy=5
					LikeData.Total_Homework =5
					LikeData.Total_Level_Difficulty=5
				
			if LikeData.Total_Count==0:
				LikePage.append(LikeData)
				break
	
			#LikeData.Total_Speedy=LikeData.Total_Speedy/LikeData.Total_Count
			LikeData.Total_Homework =LikeData.Total_Homework/LikeData.Total_Count
			LikeData.Total_Level_Difficulty=LikeData.Total_Level_Difficulty/LikeData.Total_Count
			LikeData.Total_StarPoint = LikeData.Total_StarPoint/LikeData.Total_Count
			LikePage.append(LikeData)
	Count = [[],[]]
	Eval_Count=Course_Evaluation.objects.filter(CreatedID = MyProfile).count()
	Like_Count=Like_Course.objects.filter(CreatedID = MyProfile).count()
	
	if Mobile == "full":
		Count[0] = DataCount(10,Eval_Count)
		Count[1]=DataCount(10,Like_Count)
	else:
		Count[0] = DataCount(5,Eval_Count)
		Count[1]=DataCount(5,Like_Count)

	PageInformation=list()
	TotalCount=list()
	if Mobile == "full":

		for i in range(0,2):
			PageInformation.append(CurrentPageView(Count[i],Page))									
			TotalCount.append(PageTotalCount(Count[i],PageInformation[i]))
	else:
		for i in range(0,2):
			PageInformation.append(MobileCurrentPageView(Count[i],Page))									
			TotalCount.append(MobilePageTotalCount(Count[i],PageInformation[i],3))
	PageInformation[0][1]=Page
	MyCoursePageData=dict()
	MyCoursePageData={'user':request.user, 
						'BestBoard':BestBoardView(),
						'RecommendPage':RecommendPage,
						'LikePage':LikePage,
						'PageInformation' : PageInformation,
						'TotalCount':TotalCount,
						'Page':Page,
						'TotalCountBoard':TotalEvalutionCount()
			
						}
	return MyCoursePageData
#MyCourse쪽 비동기식 구현
@csrf_protect
def MyCoursePageNation(request):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")


	if request.method =="POST":
		Page = int(request.POST['Page'])
		CurrentPage = request.POST['CurrentPage']
	CheckingLogin(request.user.username)
	Data=MyCoursePage(request,Page,request.flavour)
	if CurrentPage == "RecommendPageNation":
		template="RecommendPage.html"
	else:
		template ="LikePage.html"
	if request.flavour =='full':
			return render_to_response('html/'+template,Data)
	else:
			return render_to_response('m_skins/m_html/'+template, Data)


@csrf_protect
def CourseDelete(request):
	Mobile = request.flavour
	if CheckingLogin(request.user.username):
			return HttpResponseRedirect("/")

	if request.method == "POST":
		Code = request.POST['Code']
		Professor = request.POST['Professor']
		Period = request.POST['Period']
		Semester= request.POST['Semester']
		CourseName = request.POST['CourseName']
		Page = request.POST['CurrentPage']
		Page= int(Page)
		if Mobile == "full":
			PageFirst=10*(int(Page)-1)
			PageLast =10*(int(Page)-1)+10
		else:
			PageFirst=5*(int(Page)-1)
			PageLast =5*(int(Page)-1)+5	

		
		UserData = Profile.objects.get(User = request.user)
		try:
		 	Group_Total = Group_Total_Evaluation.objects.get(Code=Code,CourseName=CourseName)
		except:
			Group_Total = None
		DeleteData=Course_Evaluation.objects.filter(Course__CourseName=CourseName, Course__Code = Code, Course__Professor__contains=Professor, CreatedID=UserData)[0]
		
		Delete_Dis = Description_Answer.objects.filter(Course__CourseName=CourseName, Course__Code = Code, Course__Professor__contains=Professor,CreatedID=UserData)
		

		UpdateData=Total_Evaluation.objects.filter(Course__Code = Code, Course__CourseName=CourseName, Course__Professor__contains = Professor)[0]

		
		
			
		#UpdateData.Total_Speedy -= DeleteData.Speedy
		UpdateData.Total_Homework -= DeleteData.Homework
		UpdateData.Total_Level_Difficulty -= DeleteData.Level_Difficulty
		UpdateData.Total_StarPoint -= DeleteData.StarPoint
		if DeleteData.Check is True:
			UpdateData.Total_Recommend -=1

		if DeleteData.What_Answer == 1:
			UpdateData.Total_Long_Answer +=1
			
		elif DeleteData.What_Answer ==2:
			UpdateData.Total_Short_Answer +=1
		elif DeleteData.What_Answer ==3:
			UpdateData.Total_Mix += 1
		elif DeleteData.What_Answer ==4:
			UpdateData.Total_Unknown_Answer +=1
		if DeleteData.Course_Answer == 1:
			UpdateData.Total_Book_Like += 1
		elif DeleteData.Course_Answer ==2:
			UpdateData.Total_Ppt_Like+=1
		elif DeleteData.Course_Answer ==3:
			UpdateData.Total_Practice_Like +=1
		
		UpdateData.Total_Count -=1

		if UpdateData.Total_Count ==0:
			UpdateData.save()
			Delete_Dis.delete()
			DeleteData.delete()
		else:
			UpdateData.save()
			Delete_Dis.delete()
			DeleteData.delete()
		if Group_Total!=None:
			Group_Total.GroupTotalCount-=1
			Group_Total.save()

		Recommend = Recommend_Course.objects.filter(CreatedID = UserData)[PageFirst:PageLast]			
		RecommendPage =[]
		for Board in Recommend:
			renew_professor=Board.Course.Course.Professor.split("외")[0] !=0 and Board.Course.Course.Professor.split("외")[0] or Board.Course.Course.Professor
			a=Lecture.objects.filter(Semester=Board.Course.Course.Semester,CourseName=Board.Course.Course.CourseName,Professor__contains = renew_professor, Code = Board.Course.Course.Code)[0]
			RecommendData =Total_Evaluation(Course =a)
			RecommendDataList = Total_Evaluation.objects.filter(Course__CourseName=Board.Course.Course.CourseName,Course__Professor__contains = renew_professor, Course__Code = Board.Course.Course.Code)
			for ReData in RecommendDataList:
				RecommendData.Total_Speedy+=ReData.Total_Speedy
				RecommendData.Total_Homework +=ReData.Total_Homework
				RecommendData.Total_Level_Difficulty+=ReData.Total_Level_Difficulty
				RecommendData.Total_StarPoint += ReData.Total_StarPoint
				RecommendData.Total_Count+= ReData.Total_Count
				RecommendData.Total_Recommend += ReData.Total_Recommend

			RecommendData.Total_Speedy=RecommendData.Total_Speedy/RecommendData.Total_Count
			RecommendData.Total_Homework =RecommendData.Total_Homework/RecommendData.Total_Count
			RecommendData.Total_Level_Difficulty=RecommendData.Total_Level_Difficulty/RecommendData.Total_Count
			RecommendData.Total_StarPoint = RecommendData.Total_StarPoint/RecommendData.Total_Count 
			
			RecommendData.Course.Professor=renew_professor
			RecommendPage.append(RecommendData)	
		Count = [[],[]]
		Eval_Count=Course_Evaluation.objects.filter(CreatedID = UserData).count()
		Like_Count=Like_Course.objects.filter(CreatedID = UserData).count()
		
		if Mobile == "full":
			Count[0] = DataCount(10,Eval_Count)
			Count[1]=DataCount(10,Like_Count)
		else:
			Count[0] = DataCount(5,Eval_Count)
			Count[1]=DataCount(5,Like_Count)
		PageInformation=list()
		TotalCount=list()
		if Mobile == "full":

			for i in range(0,2):
				PageInformation.append(CurrentPageView(Count[i],Page))									
				TotalCount.append(PageTotalCount(Count[i],PageInformation[i]))
		else:
			for i in range(0,2):
				PageInformation.append(MobileCurrentPageView(Count[i],Page))									
				TotalCount.append(MobilePageTotalCount(Count[i],PageInformation[i],3))
		PageInformation[0][1]=Page
	
		UserData = Profile.objects.get(User = request.user)
		UserData.RecommendCount = Course_Evaluation.objects.filter(CreatedID=UserData).count()
		UserData.save()

		CTable = CountTable.objects.all()[0]
		CTable.TotalCount-=1

		Code = DeleteData.Course.Code[0:3]
		if Code == "ENG" or Code == "GEK" or Code == "GCS" or Code == "PCO" or Code == "ISL" or Code == "PST":
			CTable.GLS+=1 
		elif Code =="ISE":
			CTable.ISL += 1
		elif Code =="GMP" or Code == "MEC":
			CTable.ME += 1
		elif Code =="LAW" or Code == "UIL":
			CTable.SOF +=1
		elif Code =="CCC":
			CTable.SOCAS += 1
		elif Code =="CUE":
			CTable.SESE +=1
		elif Code =="HMM":
			CTable.MCE += 1
		elif Code =="IID":
			CTable.CCD +=1
		elif Code =="BFT":
			CTable.LS += 1
		elif Code =="ECE" or Code =="ITP":
			CTable.CSEE+=1
		elif Code =="CSW":
			CTable.CPSW +=1
		elif Code =="SIE":
			CTable.ICT +=1
		elif Code =="SIE":
			CTable.SCEE+=1
		CTable.save()
		Data={

		'User':UserData,
		"RecommendPage":RecommendPage,
		'PageInformation' : PageInformation,
		'TotalCount':TotalCount,
		'Page':Page
		}
		if request.flavour=="full":
			return render(request,'html/RecommendPage.html',Data)
		else:
			return render(request,'m_skins/m_html/RecommendPage.html',Data)

@csrf_protect
def UpdateRedirect(request):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	if request.method =="POST":
		CourseName=request.POST['CourseName']
		CourseCode=request.POST['Code']
		Semester=request.POST['Semester']
		Professor=request.POST['Professor']
		Course_ID=request.POST['CourseID']
	else:
		return HttpResponseRedirect("/")
	UserProfile=Profile.objects.get(User = request.user)
	SemesterData = Lecture.objects.filter(Code = CourseCode, CourseName=CourseName, Professor__contains=Professor).order_by('-Semester')
	SemesterList=list()
	for semester in SemesterData:
		if semester.Semester not in SemesterList:
			SemesterList.append(semester.Semester)

	CourseBoard = Course_Evaluation.objects.get(id=Course_ID,CreatedID=UserProfile) #DB 고유 ID로 접근해서 검색		
	
	totalcount=0
	MyCourseBoard = None
	CourseBoard.Course.Professor=Professor
	Description=Description_Answer.objects.filter(Course__id=Course_ID,CreatedID=UserProfile)
			
	dic = {'user':request.user,
          'BestBoard':BestBoardView(),
           'CourseBoard':CourseBoard,
    	   'Description':Description,
           'SemesterData':SemesterList,
           'TotalCountBoard':TotalEvalutionCount()
			}
	if request.flavour =='full':
		return render_to_response('html/update.html',dic)
	else:
		return render_to_response("m_skins/m_html/update.html",dic)
@csrf_protect
def CourseUpdate(request):
	if CheckingLogin(request.user.username):
			return HttpResponseRedirect("/")
	if request.method == "POST":
		#new_Speedy= (request.POST['sl1'] !="" and int(request.POST['sl1']) or 5)
		new_Homework= (request.POST['sl2'] !="" and int(request.POST['sl2']) or 5)
		
		new_Level_Difficulty=(request.POST['sl3'] !="" and int(request.POST['sl3']) or 5)
		
#			
		new_CourseComment=request.POST['CourseComment']
		new_Check = request.POST['ButtonCheck'] =="True" and True or False
		new_Satisfy = float(request.POST['StarValue'])
		new_Answer_list = request.POST.getlist('mytext[]')
		new_Who = request.POST['who']

#		new_Url = request.POST['url']
		new_paper_value= request.POST.getlist('paper_value[]')
		new_course_value =request.POST.getlist('course_value[]')
		CourseName=request.POST['HCourseName']
		Code=request.POST['HCourseCode']
		Semester=request.POST['HSemester']
		Professor=request.POST['HCourseProfessor']

		LectureData=Lecture.objects.filter(Code = Code, CourseName=CourseName, Professor__contains = Professor, Semester =Semester)[0]
		UserData = Profile.objects.get(User = request.user)
		UpdateCourseEval=Course_Evaluation.objects.get(Course__CourseName=CourseName, Course__Code = Code, Course__Professor__contains=Professor,CreatedID=UserData)
		UpdateTotalEval = Total_Evaluation.objects.filter(Course__CourseName=CourseName, Course__Code = Code, Course__Professor__contains=Professor)[0]
		Update_Dis = Description_Answer.objects.filter(Course__CourseName=CourseName, Course__Code = Code, Course__Professor__contains=Professor,CreatedID=UserData)


		UpdateTotalEval.Total_Speedy -= UpdateCourseEval.Speedy
		UpdateTotalEval.Total_Homework -= UpdateCourseEval.Homework
		UpdateTotalEval.Total_Level_Difficulty -= UpdateCourseEval.Level_Difficulty
		UpdateTotalEval.Total_StarPoint -= UpdateCourseEval.StarPoint


		if UpdateCourseEval.What_Answer-1000 >= 0:
			UpdateTotalEval.Total_Long_Answer -=1
		elif UpdateCourseEval.What_Answer%1000 -100 >=0:
			UpdateTotalEval.Total_Short_Answer-=1
		elif UpdateCourseEval.What_Answer%100 - 10 >=0:
			UpdateTotalEval.Total_Mix -= 1
		elif UpdateCourseEval.What_Answer%10 -1>=0:
			UpdateTotalEval.Total_Unknown_Answer -=1

		if UpdateCourseEval.Course_Answer-100 >= 0:
			UpdateTotalEval.Total_Book_Like -= 1
		elif UpdateCourseEval.Course_Answer%100 -10 >=0:
			UpdateTotalEval.Total_Ppt_Like-=1
		elif UpdateCourseEval.Course_Answer%10 -1 >=0:
			UpdateTotalEval.Total_Practice_Like -=1
		
		if UpdateCourseEval.Check==True:
			UpdateTotalEval.Total_Recommend -=1

		total_new_paper_value=0
		total_new_course_value=0

		for new_paper_item in new_paper_value:
			total_new_paper_value += int(new_paper_item)
		for new_course_item in new_course_value:
			total_new_course_value += int(new_course_item)

	
		UpdateCourseEval.Homework =new_Homework
		UpdateCourseEval.Level_Difficulty = new_Level_Difficulty
		UpdateCourseEval.StarPoint =new_Satisfy
		UpdateCourseEval.Check = new_Check

		UpdateCourseEval.What_Answer = total_new_paper_value
		UpdateCourseEval.Course_Answer = total_new_course_value
	#	UpdateCourseEval.Who_Answer = new_Who
		UpdateCourseEval.CourseComment = new_CourseComment
		
		if UpdateCourseEval.What_Answer-1000 >= 0:
			UpdateTotalEval.Total_Long_Answer +=1
		elif UpdateCourseEval.What_Answer%1000 -100 >=0:
			UpdateTotalEval.Total_Short_Answer+=1
		elif UpdateCourseEval.What_Answer%100 - 10 >=0:
			UpdateTotalEval.Total_Mix += 1
		elif UpdateCourseEval.What_Answer%10 -1>=0:
			UpdateTotalEval.Total_Unknown_Answer +=1

		if UpdateCourseEval.Course_Answer-100 >= 0:
			UpdateTotalEval.Total_Book_Like += 1
		elif UpdateCourseEval.Course_Answer%100 -10 >=0:
			UpdateTotalEval.Total_Ppt_Like+=1
		elif UpdateCourseEval.Course_Answer%10 -1 >=0:
			UpdateTotalEval.Total_Practice_Like +=1

		if UpdateCourseEval.Check == True:
			UpdateTotalEval.Total_Recommend +=1

		UpdateTotalEval.Total_Speedy += UpdateCourseEval.Speedy
		UpdateTotalEval.Total_Homework += UpdateCourseEval.Homework
		UpdateTotalEval.Total_Level_Difficulty += UpdateCourseEval.Level_Difficulty
		UpdateTotalEval.Total_StarPoint += UpdateCourseEval.StarPoint

		Update_Dis.delete()
		for new_Answer in new_Answer_list:#서술형 답변
			if new_Answer =="":
				continue
			temp=Description_Answer(CreatedID=UserData,Answer = new_Answer,Course=LectureData)
			temp.save()
		
		UpdateTotalEval.save()
		UpdateCourseEval.Total_Course_ID=UpdateTotalEval.id
		UpdateCourseEval.save()
		return HttpResponseRedirect("/MyCourse")

# Create your views here.
@csrf_protect
def LikeDelete(request):
	Mobile = request.flavour
	if CheckingLogin(request.user.username):
			return HttpResponseRedirect("/")

	if request.method == "POST":
		Code = request.POST['Code']
		Professor = request.POST['Professor']
		Period = request.POST['Period']
		Semester= request.POST['Semester']
		CourseName = request.POST['CourseName']
		Page = request.POST['CurrentPage']
		Page= int(Page)
		PageFirst=10*(int(Page)-1)
		PageLast =10*(int(Page)-1)+10

		UserData = Profile.objects.get(User = request.user)
		DeleteData = Like_Course.objects.get(Semester=Semester,Course__CourseName=CourseName, Course__Code = Code, Course__Professor__contains=Professor,CreatedID=UserData)
		
		DeleteData.delete()
		UserData.LikeCount =Like_Course.objects.filter(CreatedID=UserData).count()
		UserData.save()
		Count=[0,0]
		Eval_Count=Course_Evaluation.objects.filter(CreatedID = UserData).count()
		Like_Count=Like_Course.objects.filter(CreatedID = UserData).count()
		
		if Mobile == "full":
			Count[0] = DataCount(10,Eval_Count)
			Count[1]=DataCount(10,Like_Count)
		else:
			Count[0] = DataCount(5,Eval_Count)
			Count[1]=DataCount(5,Like_Count)
		PageInformation=list()
		TotalCount=list()
		if Mobile == "full":

			for i in range(0,2):
				PageInformation.append(CurrentPageView(Count[i],Page))									
				TotalCount.append(PageTotalCount(Count[i],PageInformation[i]))
		else:
			for i in range(0,2):
				PageInformation.append(MobileCurrentPageView(Count[i],Page))									
				TotalCount.append(MobilePageTotalCount(Count[i],PageInformation[i],3))
		
		LikePage = Like_Course.objects.filter(CreatedID=UserData)[PageFirst:PageLast]
		Data={

		'User':UserData,
		"LikePage":LikePage,
		'PageInformation' : PageInformation,
		'TotalCount':TotalCount,
		'Page':Page
		}
		if request.flavour == "full":
			return render(request,'html/LikePage.html',Data)
		else:
			return render(request,"m_skins/m_html/LikePage.html",Data)
