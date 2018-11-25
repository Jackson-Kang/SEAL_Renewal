	# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from login.models import Profile
from index.models import *
from functionhelper.views import CheckingLogin
from django.contrib.auth.mixins import LoginRequiredMixin
from base.views import *
from django.views.generic import TemplateView
from bs4 import BeautifulSoup
from django.http import HttpResponseRedirect, Http404,JsonResponse
# django encoding

# Create your views here.
#암호 바꾸기
class MyPageView(LoginRequiredMixin,PageView):
	login_url="/"
	paginate_by=10
	context_object_name="PageBoard"
	renew_professor_name=""
	def get_template_names(self):
		flavour = self.request.flavour
		if 'page' in self.kwargs:
			if flavour == "mobile":
				template_name = "m_html/mypage.html"
			else :
				template_name="html/mypage.html"
		else:
			if flavour == "mobile":
				template_name = "m_html/mypage.html"
			else:
				template_name="html/mypage.html"
		return 	[template_name]	
	
	def get_queryset(self):
		UserData = Profile.objects.get(User = self.request.user)
		return Course_Evaluation.objects.filter(CreatedID=UserData).order_by('-id')
class NickNameChangeView(LoginRequiredMixin,TemplateView):
	def get_context_data(self,**kwargs):
		context=super(NickNameChangeView,self).get_context_data(**kwargs)
		return context
	def post(self,request):
		nickname = request.POST['Nickname']
		myprofile = Profile.objects.filter(User = request.user)
		is_same = Profile.objects.filter(UserName = nickname)
		if len(is_same) > 0:	# 중복 여부 검사
			raise  Exception		# 사실상 의도된 에러 발생.

		myprofile.update(UserName = nickname)
	
		return JsonResponse("OK",safe=False)
class MyCourseUpdateRedirectView(LoginRequiredMixin,TemplateView):
	def post(self, request, *args, **kwargs):
		ID = request.POST['id']
		UserProfile=Profile.objects.get(User = request.user)
		CourseData = Course_Evaluation.objects.get(id=ID)
		ProfessorName = CourseData.Course.Professor.split("외")!=None and CourseData.Course.Professor.split("외")[0] or CourseData.Course.Professor
		SemesterData = Lecture.objects.filter(Code = CourseData.Course.Code, CourseName=CourseData.Course.CourseName, Professor__contains=ProfessorName).order_by('-Semester')
		SemesterList=list()
		for semester in SemesterData:
			if semester.Semester not in SemesterList:
				SemesterList.append(semester.Semester)

		CourseBoard = Course_Evaluation.objects.get(id=ID,CreatedID=UserProfile) #DB 고유 ID로 접근해서 검색		
		
		totalcount=0
		MyCourseBoard = None
		CourseBoard.Course.Professor=ProfessorName
		Description=Description_Answer.objects.filter(Course__id=ID,CreatedID=UserProfile)
				
		dic = {'user':request.user,
	          #'BestBoard':BestBoardView(),
	           'CourseBoard':CourseBoard,
	    	   'Description':Description,
	           'SemesterData':SemesterList,
	           #'TotalCountBoard':TotalEvalutionCount()
				}
		
		return render(request, 'html/updateform.html',dic)
		

class MyCourseUpdateView(LoginRequiredMixin,TemplateView):
	def post(self,request,*args, **kwargs):
		#new_Speedy= (request.POST['sl1'] !="" and int(request.POST['sl1']) or 5)
		postdata={}
		#key : CourseName,Code,Semester,Professor,homework-count,level-diff,CourseComment,Starvalue,Who,mytext[],paper_value[],course_value[]
		for key in self.request.POST.keys():
			if '[]' in key:
				postdata[key]=self.request.POST.getlist(key)
			elif key !="Professor":
				postdata[key]=self.request.POST[key]
			else : 
				postdata[key]= self.request.POST['Professor'].split("외")[0] != None and self.request.POST['Professor'].split("외")[0] or Professor
		#lecture = Lecture.objects.get(id = self.request.POST['id'])		
		#postdata['Code'] = lecture.Code
		#postdata['CourseName'] = lecture.CourseName
		#postdata['Semester'] = lecture.Semester
		#postdata['Professor'] = lecture.Professor.split("외")[0] != None and lecture.Professor.split("외")[0] or lecture.Professor		


		LectureData=Lecture.objects.filter(Code = postdata['Code'], CourseName=postdata['CourseName'], Professor__contains = postdata['Professor'], Semester =postdata['Semester'])[0]
		UserData = Profile.objects.get(User = request.user)
		UpdateCourseEval=Course_Evaluation.objects.get(Course__CourseName= postdata['CourseName'], Course__Code = postdata['Code'], Course__Professor__contains=postdata['Professor'],CreatedID=UserData)
		UpdateTotalEval = Total_Evaluation.objects.filter(Course__CourseName=postdata['CourseName'], Course__Code = postdata['Code'], Course__Professor__contains=postdata['Professor'])[0]
	
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

		for new_paper_item in postdata['paper_value']:
			total_new_paper_value += int(new_paper_item)
		for new_course_item in postdata['course_value']:
			total_new_course_value += int(new_course_item)

	
		UpdateCourseEval.Homework =postdata['homework-count']
		UpdateCourseEval.Level_Difficulty =postdata['level-diff']
		UpdateCourseEval.StarPoint =postdata['StarValue']
		

		UpdateCourseEval.What_Answer = total_new_paper_value
		UpdateCourseEval.Course_Answer = total_new_course_value
		UpdateCourseEval.Who_Answer = new_Who
		UpdateCourseEval.CourseComment = postdata['CourseComment']
		
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

		UpdateTotalEval.Total_Homework += UpdateCourseEval.Homework
		UpdateTotalEval.Total_Level_Difficulty += UpdateCourseEval.Level_Difficulty
		UpdateTotalEval.Total_StarPoint += UpdateCourseEval.StarPoint

		UpdateTotalEval.save()
		UpdateCourseEval.Total_Course_ID=UpdateTotalEval.id
		UpdateCourseEval.save()
		return HttpResponseRedirect("/MyPage")
class MyCourseDeleteView(LoginRequiredMixin,PageView):
	def post(self,request,*args, **kwargs):
		CourseID = request.POST['id']
		#Page = request.POST['CurrentPage']
		#Page= int(Page)
		# if Mobile == "full":
		# 	PageFirst=10*(int(Page)-1)
		# 	PageLast =10*(int(Page)-1)+10
		# else:
		# 	PageFirst=5*(int(Page)-1)
		# 	PageLast =5*(int(Page)-1)+5	

		
		UserData = Profile.objects.get(User = request.user)
		try:
		 	Group_Total = Group_Total_Evaluation.objects.get(Code=Code,CourseName=CourseName)
		except:
			Group_Total = None
		DeleteData=Course_Evaluation.objects.filter(id = CourseID)[0]
		ProfessorName = DeleteData.Course.Professor.split("외")!=None and DeleteData.Course.Professor.split("외")[0] or DeleteData.Course.Professor
		Delete_Dis = Description_Answer.objects.filter(Course__CourseName=DeleteData.Course.CourseName, Course__Code = DeleteData.Course.Code, Course__Professor__contains=ProfessorName, CreatedID=UserData)
		

		UpdateData=Total_Evaluation.objects.filter(Course__Code = DeleteData.Course.Code, Course__CourseName=DeleteData.Course.CourseName, Course__Professor__contains = ProfessorName)[0]

		
			
		#UpdateData.Total_Speedy -= DeleteData.Speedy
		UpdateData.Total_Homework -= DeleteData.Homework
		UpdateData.Total_Level_Difficulty -= DeleteData.Level_Difficulty
		UpdateData.Total_StarPoint -= DeleteData.StarPoint
		if DeleteData.Check is True:
			UpdateData.Total_Recommend -=1

		if DeleteData.What_Answer == 1:
			UpdateData.Total_Long_Answer -=1
			
		elif DeleteData.What_Answer ==2:
			UpdateData.Total_Short_Answer -=1
		elif DeleteData.What_Answer ==3:
			UpdateData.Total_Mix -= 1
		elif DeleteData.What_Answer ==4:
			UpdateData.Total_Unknown_Answer -=1
		if DeleteData.Course_Answer == 1:
			UpdateData.Total_Book_Like -= 1
		elif DeleteData.Course_Answer ==2:
			UpdateData.Total_Ppt_Like-=1
		elif DeleteData.Course_Answer ==3:
			UpdateData.Total_Practice_Like -=1
		
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

		#Recommend = Recommend_Course.objects.filter(CreatedID = UserData)[PageFirst:PageLast]			
		#RecommendPage =[]
		#for Board in Recommend:
		#	renew_professor=Board.Course.Course.Professor.split("외")[0] !=0 and Board.Course.Course.Professor.split("외")[0] or Board.Course.Course.Professor
		#	a=Lecture.objects.filter(Semester=Board.Course.Course.Semester,CourseName=Board.Course.Course.CourseName,Professor__contains = renew_professor, Code = Board.Course.Course.Code)[0]
		#	RecommendData =Total_Evaluation(Course =a)
		#	RecommendDataList = Total_Evaluation.objects.filter(Course__CourseName=Board.Course.Course.CourseName,Course__Professor__contains = renew_professor, Course__Code = Board.Course.Course.Code)
		#	for ReData in RecommendDataList:
		#		RecommendData.Total_Speedy+=ReData.Total_Speedy
		#		RecommendData.Total_Homework +=ReData.Total_Homework
		#		RecommendData.Total_Level_Difficulty+=ReData.Total_Level_Difficulty
		#		RecommendData.Total_StarPoint += ReData.Total_StarPoint
		#		RecommendData.Total_Count+= ReData.Total_Count
		#		RecommendData.Total_Recommend += ReData.Total_Recommend

		#	RecommendData.Total_Speedy=RecommendData.Total_Speedy/RecommendData.Total_Count
		#	RecommendData.Total_Homework =RecommendData.Total_Homework/RecommendData.Total_Count
		#	RecommendData.Total_Level_Difficulty=RecommendData.Total_Level_Difficulty/RecommendData.Total_Count
		#	RecommendData.Total_StarPoint = RecommendData.Total_StarPoint/RecommendData.Total_Count 
			
		#	RecommendData.Course.Professor=renew_professor
		#	RecommendPage.append(RecommendData)	
		
		UserData = Profile.objects.get(User = request.user)
		UserData.RecommendCount = Course_Evaluation.objects.filter(CreatedID=UserData).count()
		UserData.save()

		# CTable = CountTable.objects.all()[0]
		# CTable.TotalCount-=1

		# Code = DeleteData.Course.Code[0:3]
		# if Code == "ENG" or Code == "GEK" or Code == "GCS" or Code == "PCO" or Code == "ISL" or Code == "PST":
		# 	CTable.GLS+=1 
		# elif Code =="ISE":
		# 	CTable.ISL += 1
		# elif Code =="GMP" or Code == "MEC":
		# 	CTable.ME += 1
		# elif Code =="LAW" or Code == "UIL":
		# 	CTable.SOF +=1
		# elif Code =="CCC":
		# 	CTable.SOCAS += 1
		# elif Code =="CUE":
		# 	CTable.SESE +=1
		# elif Code =="HMM":
		# 	CTable.MCE += 1
		# elif Code =="IID":
		# 	CTable.CCD +=1
		# elif Code =="BFT":
		# 	CTable.LS += 1
		# elif Code =="ECE" or Code =="ITP":
		# 	CTable.CSEE+=1
		# elif Code =="CSW":
		# 	CTable.CPSW +=1
		# elif Code =="SIE":
		# 	CTable.ICT +=1
		# elif Code =="SIE":
		# 	CTable.SCEE+=1
		# CTable.save()
		Data={

		'User':UserData,
		#"RecommendPage":RecommendPage,
		#'PageInformation' : PageInformation,
		#'TotalCount':TotalCount,
		#'Page':Page
		}
		
		return HttpResponseRedirect("/MyPage")
		#return render(request,'html/RecommendPage.html',Data)
def NicknameChange(request):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	else:
		if request.method =="POST":
			nickname = request.POST['Nickname']
			myprofile = Profile.objects.filter(User = request.user)
			is_same = Profile.objects.filter(UserName = nickname)
			if len(is_same) > 0:	# 중복 여부 검사
				return 'Duplicate error'		# 사실상 의도된 에러 발생.

			myprofile.update(UserName = nickname)
			if request.flavour =='full':
				return render(request,'html/sealmypage.html')
			else:	
				return render(request,"m_skins/m_html/sealmypage.html")

		else:
			if request.flavour =='full':
				return render(request,'html/sealmypage.html')
			else:
				return render(request,"m_skins/m_html/sealmypage.html")
'''
@csrf_protect
def Student_Information_Change(request):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	else:
		if request.method=="POST":
			myprofile = Profile.objects.get(User= request.user)
			browser = mechanicalsoup.Browser()
				
				
			page=browser.get("https://hisnet.handong.edu/login/login.php")  

			form=page.soup.find("form",{"name":"login"}) 
			form.find("input",{"name":"id"})["value"]= smart_text(hisnet_id).encode('euc-kr')
			form.find("input",{"name":"password"})["value"] = hisnet_pw  
			
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

			browser.open("https://hisnet.handong.edu/haksa/record/HREC110M.php")
			record_contents = browser.response().read()
			record_soup = BeautifulSoup(record_contents, "html.parser")

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
			ctx = {
				'stu_num': stu_num,
				'stu_name': stu_name,
				'all_major': titles[11].next_sibling.next_sibling.text,
				'first_major': first_major,
				'second_major': second_major,
				'all_rec': all_rec,
			}
			if request.flavour =='full':
				return render(request,'html/sealmypage.html', ctx)
			else:
				return render(request,'m_skins/m_html/sealmypage.html', ctx)
'''
