# -*- coding: utf-8 -*-
# -*- coding: euc-kr -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from functionhelper.views import *
from sugangpage.models import SugangList
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.views.generic import View,ListView
from base.views import PageView
# Create your views here.

class SugangPageView(LoginRequiredMixin,PageView):
	login_url="/"
	paginate_by=10
	context_object_name="SugangList"
	renew_professor_name=""
	def get_template_names(self):
		flavour = self.request.flavour
		if 'page' in self.kwargs:
			if flavour == "mobile":
				template_name = "m_html/sugangpage.html"
			else:
				template_name="html/sugangpage.html"
			template_name="html/sugangpage.html"
		else:
			if flavour == "mobile":
				template_name = "m_html/sugang.html"
			else:
				template_name="html/sugang.html"
		return 	[template_name]	
	
	def get_queryset(self):
		return SugangList.objects.all().order_by("-id")

class SugangPageCreateView(LoginRequiredMixin,TemplateView):
	login_url="/"
	def get(self,request,*args,**kwagrs):
		content = self.request.GET['Content']
		UserData = Profile.objects.get(User = self.request.user)
		newsugangpage = SugangList(Content=content,CreatedID=UserData)
		newsugangpage.save()
		return HttpResponseRedirect("/SugangChange")

class SugangPageDeleteView(LoginRequiredMixin,TemplateView):
	login_url="/"
	def post(self,request,*args,**kwargs):
		DataID = request.POST['ID']
		UserData = Profile.objects.get(User = request.user)
		DSugang=''
		try:
			DSugang=SugangList.objects.get(id=DataID,CreatedID=UserData)
		except:
			DSugang=None
		if(DSugang==None):
			return HttpResponse(status=500)
		else:
			DSugang.delete()
			return HttpResponse(status=200)
'''
def sugangpage(request):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")

	sugangpagelist = SugangList.objects.all()

	return render(request,'html/sugangpage.html',
		{
			"SugangList" : sugangpagelist
		})	
def sugangpageWrite(request):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	if request.method =="POST":
		content = request.POST['Content']
		UserData = Profile.objects.get(User = request.user)
		newsugangpage = SugangList(Content=content,CreatedID=UserData)
		newsugangpage.save()
		return HttpResponseRedirect("/Suga")

def sugangpageDelete(request):
	if CheckingLogin(request.user.username):
		return HttpResponseRedirect("/")
	if request.method =="POST":
		DataID = request.POST['ID']
		UserData = Profile.objects.get(User = request.user)
		DSugang=''
		try:
			DSugang=SugangList.objects.get(id=DataID,CreatedID=UserData)
		except:
			DSugang=None
		if(DSugang==None):
			return HttpResponse(status=500)
		else:
			DSugang.delete()
			return HttpResponse(status=200)
'''