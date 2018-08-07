# -*- coding: utf-8 -*-
# -*- coding: euc-kr -*-

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from index.models import *
from lecture.models import *
from login.models import *
from qna.models import *	
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.db.models import Q
from functionhelper.views import *


def QnAMain(request): #Q&A 메인 
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	count=QnA_Board.objects.count()

	PageFirst=0
	PageLast =8
	
	T_Count = DataCount(8,count)#총 페이지수(아마 고쳐야할듯)
	
	PageInformation=(FirstPageView(T_Count))

	TotalCount=PageTotalCount(T_Count,PageInformation)

	Today = datetime.datetime.today()
	
	PageBoard=(QnA_Board.objects.order_by('-id')[PageFirst:PageLast])
	
	Reply_Board=[]#reply DB 저장할 공간

	for Board in PageBoard:
			#QnA 글에 맞춰서 reply 글도 그 QnA 고유 ID기준으로 reply 데이터 불러옴
			Reply_Board.append(Reply.objects.filter(QuestionID = int(Board.id)))
		#except:
		#Reply_Board=None
	dic = {'user':request.user,
		  'BestBoard':BestBoardView(),
		   'PageBoard':PageBoard,
		   'ReplyBoard':Reply_Board,
		   'TotalCount' : TotalCount, 
		   'PageInformation' : PageInformation,
		   'Today' : Today,
		   'TotalCountBoard':TotalEvalutionCount()
		   }
	if request.flavour =='full':
		return render_to_response('html/QnA.html',dic)
	else:
		return render_to_response("m_skins/m_html/qna.html",dic)

@csrf_exempt		
def QnA(request): #Q&A 페이지로 넘겼을때 나오는 기능

	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	try:
		offset = int(request.POST['Page'])
	except ValueError:
		raise Http404()

	#페이지 총 수
	PageFirst = (offset-1)*8
	PageLast = (offset-1)*8 + 8
	PageBoard = QnA_Board.objects.order_by('-id')[PageFirst:PageLast]
	#######	게시판 페이지 넘기는 기능

	count = QnA_Board.objects.count()
	
	T_Count=DataCount(8,count)
	#PageInformation = list()
    
	PageInformation=CurrentPageView(T_Count,offset)


	TotalCount=PageTotalCount(T_Count,PageInformation)

	Today =datetime.date.today()


	Reply_Board=[]
	for Board in PageBoard:
		Reply_Board.append(Reply.objects.filter(QuestionID = int(Board.id)))
			#QnA 글에 맞춰서 reply 글도 그 QnA 고유 ID기준으로 reply 데이터 불러옴
			

	PageInformation[1]=offset
	dic =  {'user':request.user,
		  'BestBoard':BestBoardView(),
		   'PageBoard':PageBoard,
		   'ReplyBoard':Reply_Board,
		   'TotalCount' : TotalCount, 
		   'PageInformation' : PageInformation,
		   'Today' : Today,
		   'TotalCountBoard':TotalEvalutionCount()
		   }

	if request.flavour =='full':
		return render_to_response('html/QnAList.html',dic)
	else:
		return render_to_response("m_skins/m_html/QnAList.html",dic)
	
def QnAWrite(request): #Q&A Write 기능
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	dic = {'user':request.user, 'BestBoard':BestBoardView(),'TotalCountBoard':TotalEvalutionCount()}
	if request.flavour =='full':
		return render_to_response('html/subscribe_faq.html',dic)
	else:
		return render_to_response("m_skins/m_html/subscribe_faq.html", dic)
@csrf_exempt
def QnA_Writing(request):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	if request.method =="POST":
		new_Text=request.POST['msg-body-txtarea']		
		new_TextWriter = Profile.objects.get(User=request.user)
		new_TextName = request.POST['msg-title-input']
		created = datetime.datetime.now()
		new_QnA = QnA_Board(Text=new_Text, TextWriter = new_TextWriter, TextName=new_TextName)
		new_QnA.save()
	return HttpResponseRedirect("/QnA")
def QnARead(request, offset): #Q&A read 기능
		if CheckingLogin(request.user.username):
				return HttpResponseRedirect("/")
		try:
			offset = int(offset)
		except ValueError:
			raise Http404()
		QnABoard = QnA_Board.objects.filter().order_by('-id')
		QnACount = QnABoard.count()
		CurrentIndex = 0

		for Board in QnABoard: 
			if Board.id ==offset:
				Current = Board
				break
			CurrentIndex+=1
		Current.ClickScore +=1
		Current.save()

		if CurrentIndex==0:
			Previous = QnABoard[CurrentIndex].id
		else:
			Previous = QnABoard[CurrentIndex-1].id
		if QnACount<=  CurrentIndex+1:
			Next = QnABoard[CurrentIndex].id
		else:
			Next = QnABoard[CurrentIndex+1].id

		try:
			QnA_Reply = Reply.objects.filter(QuestionID = Current.id)
		except:
			QnA_Reply =None
		
		dic = 	{'user':request.user, 
			'Current':Current, 
			'QnA_Reply' : QnA_Reply,
			'Previous' : Previous,
			'Next':Next,
			'BestBoard':BestBoardView(),'TotalCountBoard':TotalEvalutionCount()}

		if request.flavour =='full':
			return render_to_response('html/qna-contents.html',dic)
		else:
			return render_to_response("m_skins/m_html/qna-contents.html", dic)

def QnA_Reply(request, offset): 
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dic ={'user':request.user, 'ID':offset}	
	if request.flavour =='full':
			return render_to_response('html/subscribe_reply.html',dic)
	else:
			return render_to_response("m_skins/m_html/subscribe_reply.html",dic)
@csrf_exempt
def QnA_Replying(request,offset):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	if request.method =="POST":
		try:
			offset = int(offset)
		except ValueError:
			raise Http404()
		Current = QnA_Board.objects.filter(id=offset).get()

	
		new_Text=request.POST['msg-body-txtarea2']		
		new_TextWriter = Profile.objects.get(User=request.user)
		new_TextName = request.POST['msg-title-input2']
		created = datetime.datetime.now()
		Question_ID = Current.id
		new_QnAReply = Reply(QuestionID= Question_ID,TextWriter = new_TextWriter, Text=new_Text, TextName=new_TextName)
		new_QnAReply.save()
	return HttpResponseRedirect("/QnA")
@csrf_exempt
def Improvement_Write(request):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	if request.method=="POST":
		new_Text=request.POST['msg-body-txtarea']		
		new_TextWriter = Profile.objects.get(User=request.user)
		new_TextName = request.POST['msg-title-input']
		new_Improvement = Improvement(Text=new_Text, TextWriter = new_TextWriter, TextName=new_TextName)
		new_Improvement.save()
		return HttpResponseRedirect("/")
	else:
		return HttpResponseRedirect("/")

@csrf_exempt
def Judgement_Write(request):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	if request.method=="POST":
		new_Text=request.POST['msg-body-txtarea']		
		new_TextWriter = Profile.objects.get(User=request.user)
		new_TextName = request.POST['msg-title-input']
		new_Judgement = Judgement(Text=new_Text, TextWriter = new_TextWriter, TextName=new_TextName)
		new_Judgement.save()
		return HttpResponseRedirect("/")
	else:
		return HttpResponseRedirect("/")
# Create your views here.
		