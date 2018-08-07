# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from lecture.models import Lecture
import xlrd
from index.models import *
# selenium module
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# csrf
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from bs4 import BeautifulSoup
from django.views.generic import TemplateView
import mechanicalsoup
import time
import logging
def func_strip(arg):
	try:
		arg = arg.strip()
		return arg
	except AttributeError:
		return arg

def func_int(arg):
	try:
		return int(arg)
	except ValueError:	# String -> ValueError
		return arg
	except TypeError:	# NoneType -> TypeError
		return arg

class UpdateLoginView(TemplateView):

	def get_context_data(self,**kwargs):
		context=super(UpdateLoginView,self).get_context_data(**kwargs)
		return context
	def get_template_names(self):
		return "html/DBUpdate.html"
	def get(self,request,*args,**kwargs):
		if(request.user.username!="admin_seal"):
			return	HttpResponseRedirect("/")
		else:
			return render(request,'html/DBUpdate.html',super(UpdateLoginView,self).get_context_data(**kwargs))
class AutoFastLecUpdateView(TemplateView):
	def get_context_data(self,**kwargs):
		context=super(AutoFastLecUpdateView,self).get_context_data(**kwargs)
		return context
	def get(self,requlest,*args,**kwaregs):
		logger = logging.getLogger(__name__) 
		return HttpResponse("뭐냐")
	def post(self,request,*args, **kwargs):
		if(request.user.username!="admin_seal"):
			return	HttpResponseRedirect("/")
		hisnet_id = request.POST['HisnetID']
		hisnet_pw = request.POST['HisnetPassword']
		logger = logging.getLogger("mysite2.lecture") 
	
		hak_lst = ['2018-1']
		# cur_semester_lst = ['15-1', '15-3', '15-2', '15-4', '16-1', '16-3', '16-2']
		hakbu_lst = [
			'0001', '0007','0008','0009', '0010', '0011',
			'0012', '0021', '0022', '0024',
			'0033', '0071', '0074', '0077',
			'0078', '0079', '0090',
			'0041', '0008',
		]	# 학부 코드 list
		hakbu_dict = {
		'0001':'글로벌리더십학부',
		'0007':'창의융합교육원(자연과학계열)',
		'0008':'창의융합교육원(인문사회)',
		'0009':'창의융합교육원(이공)',
		'0010':'Global EDISON',
		'0011':'국제어문학부',
		'0012':'언론정보문화학부',
		'0021':'경영경제학부',
		'0022':'법학부',
		'0024':'상담심리사회복지학부',
		'0033':'생명과학부',
		'0041':'ICT창업학부',
		'0071':'전산전자공학부',
		'0074':'산업정보디자인학부',
		'0077':'기계제어공학부',
		'0078':'공간환경시스템공학부',
		'0079':'콘텐츠융합디자인학부',
		'0090':'산업교육학부',
		'0111':'없는학부(테스트)'
		}
		
		logger.debug("FFF")
		driver = webdriver.PhantomJS(service_log_path="/home/cra/ClassSEAL/mysite2/ghostdriver.log")
		
		logger.debug("GGG")
		driver.get("https://hisnet.handong.edu/login/login.php")
		logger.debug("LLL")
		driver.set_window_size(1024,768)
		
		idinput = driver.find_element_by_name("id")
		idinput.send_keys(hisnet_id)
		pwinput = driver.find_element_by_name("password")
		pwinput.send_keys(hisnet_pw)
		login_button = driver.find_element_by_xpath("//input[@type='image'][@src='/2012_images/intro/btn_login.gif']")
		login_button.click()
		logger.debug("AAA")
		driver.get("https://hisnet.handong.edu/haksa/hakjuk/HHAK110M.php")
		
		# logger.debug("when")
		# 
		# browser = mechanicalsoup.Browser(session=None)
	
		# logger.debug("data")
		# #이부분 쿠키 유지때문에 뭔가 무한루프 걸리는듯 해결해야함
		# page=browser.get("https://hisnet.handong.edu/login/login.php")  
		# logger.debug("error is")
		# form=page.soup.find("form",{"name":"login"}) 
		# form.find("input",{"name":"id"})["value"]= smart_text(hisnet_id).encode('euc-kr')
		# form.find("input",{"name":"password"})["value"] = hisnet_pw  

		# response=browser.submit(form,page.url)
		# contents=browser.get("https://hisnet.handong.edu/haksa/hakjuk/HHAK110M.php")
		# logger.debug("where")
		cnt = 1

		lec_lst = []
		try:
			for idx, hak in enumerate(hak_lst):
				hak_year = hak.split('-')[0]
				hak_term = hak.split('-')[1]
				# cur_semester = cur_semester_lst[idx]
				cur_semester = hak[2:]

				for hakbu in hakbu_lst:
					try:
						for page in range(1,100):
							target_url = "https://hisnet.handong.edu/for_student/course/PLES330M.php?Page=" + str(page) + "&hakbu=" + hakbu + "&isugbn=%C0%FC%C3%BC&injung=%C0%FC%C3%BC&eng=%C0%FC%C3%BC&ksearch=search&hak_year=" + hak_year + "&hak_term=" + hak_term
							
							logger.debug(str(cnt)+"start" + target_url)
							contents=driver.get(target_url) 
							logger.debug("F")
							soup = BeautifulSoup(driver.page_source,'html.parser')
							logger.debug("G")
							titles = soup.find_all(class_='tblcationTitlecls')
							# last_page = int(soup.find_all('img', src='/myboard/images/btn_say_next.gif')[0].parent.previous_sibling.previous_sibling.previous_sibling.previous_sibling.text)
							logger.debug(str(cnt)+"start" + target_url)
							
							td = titles
							for i in range(15):
								temp_lec = []
								temp = td[0].parent.next_sibling.next_sibling
								 
								td = temp.find_all('td')
								temp_lec.append(td[0].text.strip())	# 전공,선택구분
								temp_lec.append(td[1].text.strip())	# 과목코드
								temp_lec.append(func_int(td[2].text.strip()))	# 분반
								temp_lec.append(td[3].text.strip())	# 과목명(한글)
								temp_lec.append(td[3].text.strip())	# 과목명(영어)
								## Hisnet에서 더이상 영어 과목명 지원 안함에 따른 변경
								# temp_lec.append(td[3].br.previous_sibling.strip())	# 과목명(한글)
								# temp_lec.append(td[3].br.text.strip('')[1:-1])	# 과목명(영어)
								temp_lec.append(td[4].text.strip())	# 학점
								temp_lec.append(td[5].text.strip())	# 교수님
								try:
									temp_lec.append(td[6].text.split()[0])	# 강의시간
								except IndexError as e:
									temp_lec.append('')
								try:
									temp_lec.append(td[7].text.strip())	# 강의실
								except IndexError as e:
									temp_lec.append('')
								try:
									temp_lec.append(func_int(td[8].text.strip()))	# 정원
								except IndexError as e:
									temp_lec.append(0)
								try:
									temp_lec.append(func_int(td[9].text.strip()))	# 인원
								except IndexError as e:
									temp_lec.append(0)
								try:
									temp_lec.append(td[10].text.strip())	# 영어비율
								except IndexError as e:
									temp_lec.append('')
								try:
									temp_lec.append(td[11].text.strip())	# 교양구분
								except IndexError as e:
									temp_lec.append('')
								temp_lec.append(hakbu_dict[hakbu])	# 학부
								lec_lst.append(temp_lec)
								# DB 값 Update
								db_lec = Lecture.objects.filter(Semester=cur_semester, Code=temp_lec[1], Class=temp_lec[2])
								new_lec=""
								if db_lec:
									db_lec.update(
										Semester=cur_semester,
										Category=temp_lec[0],
										Code=temp_lec[1],
										Class=temp_lec[2],
										CourseName=temp_lec[3],
										CourseName_Eng=temp_lec[4],
										Credit=temp_lec[5],
										Professor=temp_lec[6],
										Period=temp_lec[7],
										ClassRoom=temp_lec[8],
										Fix_num=temp_lec[9],
										Take_num=temp_lec[10],
										EnglishRatio=temp_lec[11],
										CategoryDetail=temp_lec[12],
										Major=temp_lec[13]
									)
								else:
									new_lec = Lecture(
										Semester=cur_semester,
										Category=temp_lec[0],
										Code=temp_lec[1],
										Class=temp_lec[2],
										CourseName=temp_lec[3],
										CourseName_Eng=temp_lec[4],
										Credit=temp_lec[5],
										Professor=temp_lec[6],
										Period=temp_lec[7],
										ClassRoom=temp_lec[8],
										Fix_num=temp_lec[9],
										Take_num=temp_lec[10],
										EnglishRatio=temp_lec[11],
										CategoryDetail=temp_lec[12],
										Major=temp_lec[13]							
									)
									new_lec.save()
								temp_professor = temp_lec[6].split("외") !=None and temp_lec[6].split("외")[0] or temp_lec[6]
			
								temp_total=Total_Evaluation.objects.filter(Course__Code=temp_lec[1],Course__CourseName=temp_lec[4],Course__Professor=temp_professor).count()
								if temp_total == 0:
										if new_lec:
											Total_Evaluation(Course=new_lec).save()
								cnt += 1

					except AttributeError as e:
						logger.debug("attri")
						continue
		except:
			logger.error("Error")
			return HttpResponse("에러로 인한 return")
		return HttpResponse(str(cnt)+'개의 데이터를 성공적으로 입력했습니다.')

@csrf_exempt
def AutoFastLecUpdate(request):
	if not request.user.username=='admin_seal':
		return HttpResponseRedirect('/')
	"""
	Hisnet 개설시간표 자동 update function
	"""
	if request.method == 'POST':
		hisnet_id = request.POST['HisnetID']
		hisnet_pw = request.POST['HisnetPassword']
		
		hak_lst = ['2017-2']
		# cur_semester_lst = ['15-1', '15-3', '15-2', '15-4', '16-1', '16-3', '16-2']
		hakbu_lst = [
			'0001', '0007','0008','0009', '0010', '0011',
			'0012', '0021', '0022', '0024',
			'0033', '0071', '0074', '0077',
			'0078', '0079', '0090',
			'0041', '0008',
		]	# 학부 코드 list
		hakbu_dict = {
		'0001':'글로벌리더십학부',
		'0007':'창의융합교육원(자연과학계열)',
		'0008':'창의융합교육원(인문사회)',
		'0009':'창의융합교육원(이공)',
		'0010':'Global EDISON',
		'0011':'국제어문학부',
		'0012':'언론정보문화학부',
		'0021':'경영경제학부',
		'0022':'법학부',
		'0024':'상담심리사회복지학부',
		'0033':'생명과학부',
		'0041':'ICT창업학부',
		'0071':'전산전자공학부',
		'0074':'산업정보디자인학부',
		'0077':'기계제어공학부',
		'0078':'공간환경시스템공학부',
		'0079':'콘텐츠융합디자인학부',
		'0090':'산업교육학부',
		'0111':'없는학부(테스트)'
		}
		browser = mechanicalsoup.Browser()
						
		page=browser.get("https://hisnet.handong.edu/login/login.php")  

		form=page.soup.find("form",{"name":"login"}) 
		form.find("input",{"name":"id"})["value"]= smart_text(username).encode('euc-kr')
		form.find("input",{"name":"password"})["value"] = password  
		
		response=browser.submit(form,page.url)
		contents=browser.get("https://hisnet.handong.edu/haksa/hakjuk/HHAK110M.php")
		
		cnt = 1

		lec_lst = []
		for idx, hak in enumerate(hak_lst):
			hak_year = hak.split('-')[0]
			hak_term = hak.split('-')[1]
			# cur_semester = cur_semester_lst[idx]
			cur_semester = hak[2:]

			for hakbu in hakbu_lst:
				try:
					for page in range(1,100):
						target_url = "https://hisnet.handong.edu/for_student/course/PLES330M.php?Page=" + str(page) + "&hakbu=" + hakbu + "&isugbn=%C0%FC%C3%BC&injung=%C0%FC%C3%BC&eng=%C0%FC%C3%BC&ksearch=search&prof_name=&gwamok=&gwamok_code=&hak_year=" + hak_year + "&hak_term=" + hak_term
						contents=browser.get(target_url) 
						soup = contents.soup
						titles = soup.find_all(class_='tblcationTitlecls')
						# last_page = int(soup.find_all('img', src='/myboard/images/btn_say_next.gif')[0].parent.previous_sibling.previous_sibling.previous_sibling.previous_sibling.text)

						td = titles
						for i in range(15):
							temp_lec = []
							temp = td[0].parent.next_sibling.next_sibling
							td = temp.find_all('td')
							temp_lec.append(td[0].text.strip())	# 전공,선택구분
							temp_lec.append(td[1].text.strip())	# 과목코드
							temp_lec.append(func_int(td[2].text.strip()))	# 분반
							temp_lec.append(td[3].text.strip())	# 과목명(한글)
							temp_lec.append(td[3].text.strip())	# 과목명(영어)
							## Hisnet에서 더이상 영어 과목명 지원 안함에 따른 변경
							# temp_lec.append(td[3].br.previous_sibling.strip())	# 과목명(한글)
							# temp_lec.append(td[3].br.text.strip('')[1:-1])	# 과목명(영어)
							temp_lec.append(td[4].text.strip())	# 학점
							temp_lec.append(td[5].text.strip())	# 교수님
							try:
								temp_lec.append(td[6].text.split()[0])	# 강의시간
							except IndexError as e:
								temp_lec.append('')
							temp_lec.append(td[7].text.strip())	# 강의실
							temp_lec.append(func_int(td[8].text.strip()))	# 정원
							temp_lec.append(func_int(td[9].text.strip()))	# 인원
							temp_lec.append(td[10].text.strip())	# 영어비율
							temp_lec.append(td[11].text.strip())	# 교양구분
							temp_lec.append(hakbu_dict[hakbu])	# 학부
							lec_lst.append(temp_lec)
							# DB 값 Update
							db_lec = Lecture.objects.filter(Semester=cur_semester, Code=temp_lec[1], Class=temp_lec[2])
							new_lec=""
							if db_lec:
								db_lec.update(
									Semester=cur_semester,
									Category=temp_lec[0],
									Code=temp_lec[1],
									Class=temp_lec[2],
									CourseName=temp_lec[3],
									CourseName_Eng=temp_lec[4],
									Credit=temp_lec[5],
									Professor=temp_lec[6],
									Period=temp_lec[7],
									ClassRoom=temp_lec[8],
									Fix_num=temp_lec[9],
									Take_num=temp_lec[10],
									EnglishRatio=temp_lec[11],
									CategoryDetail=temp_lec[12],
									Major=temp_lec[13]
								)
							else:
								new_lec = Lecture(
									Semester=cur_semester,
									Category=temp_lec[0],
									Code=temp_lec[1],
									Class=temp_lec[2],
									CourseName=temp_lec[3],
									CourseName_Eng=temp_lec[4],
									Credit=temp_lec[5],
									Professor=temp_lec[6],
									Period=temp_lec[7],
									ClassRoom=temp_lec[8],
									Fix_num=temp_lec[9],
									Take_num=temp_lec[10],
									EnglishRatio=temp_lec[11],
									CategoryDetail=temp_lec[12],
									Major=temp_lec[13]							
								)
								new_lec.save()
							temp_professor = temp_lec[6].split("외") !=None and temp_lec[6].split("외")[0] or temp_lec[6]
		
							temp_total=Total_Evaluation.objects.filter(Course__Code=temp_lec[1],Course__CourseName=temp_lec[4],Course__Professor=temp_professor).count()
							if temp_total == 0:
									if new_lec:
										Total_Evaluation(Course=new_lec).save()
							cnt += 1
				except AttributeError as e:
					continue
		return HttpResponse('성공적으로 데이터를 입력했습니다.')
	else:
		return HttpResponseRedirect('/')


@csrf_exempt
def auto_lec_update(request):
	if not request.user.username=='admin_seal':
		return HttpResponseRedirect('/')
	"""
	Hisnet 개설시간표 자동 update function
	"""
	if request.method == 'POST':
		hisnet_id = request.POST['HisnetID']
		hisnet_pw = request.POST['HisnetPassword']
		hisnet_url = "http://hisnet.handong.edu/login/login.php"
		hak_year = "2010"
		hak_term = "1"
		cur_semester = "10-1"
		hakbu_lst = [
			'0001', '0009', '0010', '0011',
			'0012', '0021', '0022', '0024',
			'0033', '0071', '0074', '0077',
			'0078', '0079', '0090'
		]	# 학부 코드 list
		hakbu_dict = {
		'0001':'글로벌리더십학부',
		'0009':'창의융합교육원',
		'0010':'Global EDISON',
		'0011':'국제어문학부',
		'0012':'언론정보문화학부',
		'0021':'경영경제학부',
		'0022':'법학부',
		'0024':'상담심리사회복지학부',
		'0033':'생명과학부',
		'0071':'전산전자공학부',
		'0074':'산업정보디자인학부',
		'0077':'기계제어공학부',
		'0078':'공간환경시스템공학부',
		'0079':'콘텐츠융합디자인학부',
		'0090':'산업교육학부'
		}
		# hakbu_lst = ['0071']	# Debug list

		# 히스넷 로그인
		driver = webdriver.PhantomJS(service_log_path='/opt/bitnami/python/lib/python2.7/site-packages/selenium/webdriver/phantomjs/ghostdriver.log')
		driver.get(hisnet_url)
		driver.set_window_size(1024,768)
		main_login_frame = driver.find_element_by_name("MainFrame")
		driver.switch_to_frame(main_login_frame)
		idinput = driver.find_element_by_name("id")
		idinput.send_keys(hisnet_id)
		pwinput = driver.find_element_by_name("password")
		pwinput.send_keys(hisnet_pw)
		login_button = driver.find_element_by_xpath("//input[@type='image'][@src='/2012_images/intro/btn_login.gif']")
		login_button.click()

		prev_db = Lecture.objects.filter(Semester=cur_semester)
		prev_db.delete()

		all_info_lst = []
		for hakbu in hakbu_lst:
			# 학부 설정 후 첫페이지 이동
			first_link = "https://hisnet.handong.edu/for_student/course/PLES330M.php?hak_year=" \
			 + hak_year \
			 + "&hak_term=" \
			 + hak_term \
			 + "&prof_name=&gwamok=&gwamok_code=&hakbu=" \
			 + hakbu \
			 + "&isugbn=%C0%FC%C3%BC&injung=%C0%FC%C3%BC&ksearch=search"
			driver.get(first_link)

			try:
				link_02 = driver.find_element_by_link_text("02")	# 2page 없으면 1page 만 존재
				last_button = driver.find_element_by_xpath("//img[@src='/myboard/images/btn_say_last.gif']")	# 마지막 페이지 이동 버튼
				last_button.click()
			except NoSuchElementException as e:
				pass
			try:
				last_num = int(driver.find_element_by_class_name("orangebold").text)	# 마지막 페이지 number
			except NoSuchElementException as e:
				continue

			hakbu_info_lst = []
			for page in range(1, last_num+1):	# from 1 to last_num
				href = "https://hisnet.handong.edu/for_student/course/PLES330M.php?Page=" \
				 + str(page) \
				 + "&hak_year=" \
				 + hak_year \
				 + "&hak_term=" \
				 + hak_term \
				 + "&prof_name=&gwamok=&gwamok_code=&hakbu=" \
				 + hakbu \
				 + "&isugbn=%C0%FC%C3%BC&injung=%C0%FC%C3%BC&ksearch=search"
				driver.get(href)
				for i in range(2, 17):	# 1 page 당 15 강의, 1번째는 컬럼명
					try:
						lec_parent = driver.find_element_by_xpath("//table[@id='att_list']/tbody/tr["+ str(i) + "]")
						lec_category = lec_parent.find_element_by_xpath("./td[1]").text 	# 과목구분
						lec_code = lec_parent.find_element_by_xpath("./td[2]").text 	# 과목코드
						lec_class = lec_parent.find_element_by_xpath("./td[3]").text 	# 과목분반
						lec_name = lec_parent.find_element_by_xpath("./td[4]").text 	# 과목명
						kr_name = lec_name.split('\n')[0]
						en_name = lec_name.split('\n')[1][1:-1]	# 괄호 제외
						lec_credit = lec_parent.find_element_by_xpath("./td[5]").text 	# 과목학점
						lec_prof = lec_parent.find_element_by_xpath("./td[6]").text # 담당교수
						lec_period = lec_parent.find_element_by_xpath("./td[7]").text 	# 강의시간
						kr_period = lec_period.split('\n')[0]	# 강의시간(한글)
						lec_room = lec_parent.find_element_by_xpath("./td[8]").text 	# 강의실
						lec_fix_num = lec_parent.find_element_by_xpath("./td[9]").text # 수강정원
						lec_take_num = lec_parent.find_element_by_xpath("./td[10]").text # 수강인원
						lec_eng_ratio = lec_parent.find_element_by_xpath("./td[11]").text # 영어비율
						lec_category_detail = lec_parent.find_element_by_xpath("./td[12]").text # 교양실무
						temp_lec = (
							lec_category, lec_code, lec_class, kr_name,
							lec_credit, lec_prof, kr_period, lec_room,
							lec_fix_num, lec_take_num, lec_eng_ratio, lec_category_detail,
							en_name
						)
						temp_lec = list(map(func_strip, temp_lec))	# tuple -> list(strip_string)
						hakbu_info_lst.append(temp_lec)
						temp_lec[9] = func_int(temp_lec[9])
						temp_lec[2] = func_int(temp_lec[2])
						temp_lec[8] = func_int(temp_lec[8])
						# DB 값 Update
						db_lec = Lecture.objects.filter(Semester=cur_semester, Code=temp_lec[1], Class=temp_lec[2])

						if db_lec:
							db_lec.update(
								Semester=cur_semester,
								Category=temp_lec[0],
								Code=temp_lec[1],
								Class=temp_lec[2],
								CourseName=temp_lec[3],
								Credit=temp_lec[4],
								Professor=temp_lec[5],
								Period=temp_lec[6],
								ClassRoom=temp_lec[7],
								Fix_num=temp_lec[8],
								Take_num=temp_lec[9],
								EnglishRatio=temp_lec[10],
								CategoryDetail=temp_lec[11],
								CourseName_Eng=temp_lec[12],
								Major=hakbu_dict[hakbu]
							)
						else:
							new_lec = Lecture(
								Semester=cur_semester,
								Category=temp_lec[0],
								Code=temp_lec[1],
								Class=temp_lec[2],
								CourseName=temp_lec[3],
								Credit=temp_lec[4],
								Professor=temp_lec[5],
								Period=temp_lec[6],
								ClassRoom=temp_lec[7],
								Fix_num=temp_lec[8],
								Take_num=temp_lec[9],
								EnglishRatio=temp_lec[10],
								CategoryDetail=temp_lec[11],
								CourseName_Eng=temp_lec[12],
								Major=hakbu_dict[hakbu]								
							)
							new_lec.save()
					except NoSuchElementException as e:		# page에 강의가 15개 이하인 경우
						break
			all_info_lst.append(hakbu_info_lst)
		return HttpResponse('성공적으로 데이터를 입력했습니다.')
	else:
		return HttpResponseRedirect('/')


def lec_update(request):
	if not request.user.username=='admin_seal':
		return HttpResponseRedirect('/')

	semester_lst = [
	'11-1', '11-2', '11-3', '11-4', 
	'12-1', '12-2', '12-3', '12-4', 
	'13-1', '13-2', '13-3', '13-4', 
	'14-1', '14-2', '14-3', '14-4'
	]
	# semester_lst = ['15-2']
	semester_lst.sort(reverse=True)
	
	file_location = "/opt/bitnami/apps/django/django_projects/darkzero/mysite2/gasul_table/"
	# 학부별 정리
	for semester in semester_lst:
		file_lst = [
			file_location+semester+'/0001.xlsx',
			file_location+semester+'/0009.xlsx',
			file_location+semester+'/0010.xlsx',
			file_location+semester+'/0011.xlsx',
			file_location+semester+'/0012.xlsx',
			file_location+semester+'/0021.xlsx',
			file_location+semester+'/0022.xlsx',
			file_location+semester+'/0024.xlsx',
			file_location+semester+'/0033.xlsx',
			file_location+semester+'/0071.xlsx',
			file_location+semester+'/0074.xlsx',
			file_location+semester+'/0077.xlsx',
			file_location+semester+'/0078.xlsx',
			file_location+semester+'/0090.xlsx'
		]
		for xls in file_lst:
			try:
				workbook = xlrd.open_workbook(xls)
			except:
				continue
			sheet = workbook.sheet_by_index(0)
			lec_lst = []
			for row in range(3, sheet.nrows, 4):
				lec_info = []
				for col in range(sheet.ncols):
					val = sheet.cell_value(row,col)
					# if val == '' :	# 값이 NULL이면 조작안함
					lec_info.append(val)
				lec_info.append(sheet.cell_value(row+1,3))	# 과목영어이름
				lec_info.append(sheet.cell_value(row+1,5))	# 교수님 성함
				lec_lst.append(lec_info)
			for var in lec_lst:
				if var[9] == '':
					var[9] = 0
				else:
					var[9] = int(var[9])
				if not (var[4] == ''):
					var[4] = int(var[4])
				if not (var[8] == ''):
					var[8] = int(var[8])
				var = list(map(func_strip, var))
				try:
					d_lec = Lecture.objects.filter(Semester=semester, Code=var[1], Class=var[2])
					if d_lec: # 업데이트 가능한 요소들
						d_lec.update(
							Class=var[2],
							Credit=var[4],
							Period=var[6],
							ClassRoom = var[7],
							Fix_num = var[8],
							Take_num = var[9],
							EnglishRatio = var[10],
							Professor = var[-1]
							)
					else:
						new_lec = Lecture(
							Semester=semester,
							Category=var[0],
							Code=var[1],
							Class=var[2],
							CourseName=var[3],
							Credit=var[4],
							Major=var[5],
							Period=var[6],
							ClassRoom=var[7],
							Fix_num=var[8],
							Take_num=var[9],
							EnglishRatio=var[10],
							CategoryDetail=var[11],
							CourseName_Eng=var[-2],
							Professor=var[-1],
							)
						new_lec.save()
				except:
					return HttpResponse('데이터 입력 중 오류가 발생했습니다.')
	return HttpResponse('성공적으로 데이터를 입력했습니다.')


