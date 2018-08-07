# -*- coding: utf-8 -*-
# -*- coding: euc-kr -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from index.models import *
from lecture.models import *
from login.models import *
from notice.models import *
from django.views.decorators.csrf import csrf_protect
import datetime  #오늘날짜 불러오기 위한 import
from django.db.models import Q
from functionhelper.views import *


def NoticeMain(request):#Notice 기능
		
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")

	count=Notice_Board.objects.count()
	
	PageFirst = (1-1)*8
	PageLast = (1-1)*8 + 8
	PageBoard = Notice_Board.objects.order_by('-id')[PageFirst:PageLast] 
	
	T_Count = DataCount(8,count) #총 페이지수(아마 고쳐야할듯)
	
	PageInformation=(FirstPageView(T_Count))
		
	Today = datetime.datetime.now()
	
	dic =  {'user':request.user,
		   'BestBoard':BestBoardView(),
		   'PageBoard':PageBoard, 
		   'PageInformation':PageInformation,
		   'TotalCount' : PageTotalCount(T_Count,PageInformation),
		   'Today':Today,
		   'TotalCountBoard':TotalEvalutionCount()
			}
	if request.flavour =='full':
			return render(request,'html/notice.html',dic)
	else:
			return render(request,"m_skins/m_html/notice.html",dic)
@csrf_protect
def Notice(request): #Notice Page 넘겨졌을때 나오는 페이지

	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	try:
		offset = int(request.POST['Page'])
	except ValueError:
		raise Http404()

	#페이지 수 정보
	PageFirst = (offset-1)*8
	PageLast = (offset-1)*8 + 8
	PageBoard = Notice_Board.objects.order_by('-id')[PageFirst:PageLast] 
	#페이지 넘기는 기능

	count = Notice_Board.objects.count()

	T_Count=DataCount(8,count)

	PageInformation=CurrentPageView(T_Count,offset)


	TotalCount = PageTotalCount(T_Count,PageInformation)

	Today =datetime.date.today()    
	PageInformation[1]=offset	
	dic={'user':request.user, 
				  'BestBoard':BestBoardView(),
				   'PageBoard':PageBoard,
				   'TotalCount' : TotalCount,
				   'Today' :Today,
				   'PageInformation':PageInformation,
				   'TotalCountBoard':TotalEvalutionCount()
       			  }
	if request.flavour =='full':
			return render(request,'html/NoticeList.html',dic)
	else:
			return render(request,"m_skins/m_html/NoticeList.html",dic)

def Notice_Read(request, offset): #Notice Read 기능
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()

	Current = Notice_Board.objects.filter(id=offset).get()
	Current.ClickScore +=1
	Current.save()

	NoticeCount = Notice_Board.objects.count()

	if offset ==1:
		Next = 1
	else:
		Next = offset-1
	if offset == NoticeCount:
		Previous = NoticeCount
	else:
		Previous = offset+1
	
	dic ={'user':request.user,
		'BestBoard':BestBoardView(),
		'Previous' :Previous,
		'Next' :Next,
		'Board':Current,
		'TotalCountBoard':TotalEvalutionCount()}
	if request.flavour =='full':
			return render(request,'html/notice-contents.html',dic)
	else:
		return render(request,"m_skins/m_html/notice-contents.html", dic)


def Notice_Write(request): #Q&A Write 기능
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")

	dic = {'user':request.user}
	if request.flavour =='full':
		return render(request,'html/subscribe_notice.html',dic)
	else:
		return render(request,"m_skins/m_html/subscribe_notice.html",dic)
@csrf_protect
def Notice_Writing(request):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	if request.method =="POST":
		new_Text=request.POST['msg-body-txtarea']		
		new_TextWriter = Profile.objects.get(User=request.user)
		new_TextName = request.POST['msg-title-input']
		created = datetime.datetime.now()
		new_Notice = Notice_Board(Text=new_Text, TextWriter = new_TextWriter.UserName, TextName=new_TextName)
		new_Notice.save()
	return HttpResponseRedirect("/Notice")
# Create your views here.
