# -*- coding: utf-8 -*-
# -*- coding: euc-kr -*-
from django.db import models
from login.models import Profile
from lecture.models import Lecture
import datetime
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from django.utils.encoding import smart_text
class OverwriteStorage(FileSystemStorage):
    '''
    Muda o comportamento padrão do Django e o faz sobrescrever arquivos de
    mesmo nome que foram carregados pelo usuário ao invés de renomeá-los.
    '''
    def get_available_name(self, name,max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
def upload_path_handler(self,filename):
	dirname = os.path.join(settings.MEDIA_ROOT,self.CreatedID.User.username)
	dirname = os.path.join(dirname,str(self.Course.id))

	dirname = os.path.join(dirname,smart_text(filename))
	
	return dirname

class Description_Answer(models.Model):
    CreatedID = models.ForeignKey(Profile)
    Answer = models.TextField(max_length=200)
    Course = models.ForeignKey(Lecture)
    def __unicode__(self):
        return self.CreatedID.User.username


class Total_Evaluation(models.Model):
	Course = models.ForeignKey(Lecture)
	Total_Speedy = models.IntegerField(default=0)
	Total_Homework = models.IntegerField(default=0)
	Total_Level_Difficulty = models.IntegerField(default=0)
	Total_Count =models.IntegerField(default=0)
	Total_StarPoint = models.FloatField(default=0)
	Total_Recommend = models.IntegerField(default=0, null=False)
	Total_Mix = models.IntegerField(default=0)
	Total_Short_Answer = models.IntegerField(default=0)
	Total_Long_Answer = models.IntegerField(default=0)
	Total_Unknown_Answer = models.IntegerField(default=0)
	Total_Book_Like=models.IntegerField(default=0)
	Total_Ppt_Like = models.IntegerField(default=0)
	Total_Practice_Like = models.IntegerField(default=0)

	def __unicode__(self):
		return '%s %s %s %d' % (self.Course.Code,self.Course.Professor, self.Course.CourseName,self.Course.id)

class Group_Total_Evaluation(models.Model):
	Code = models.CharField(max_length=20, null=False)
	CourseName = models.CharField(max_length=80, null=True)
	GroupTotalCount = models.IntegerField(default=0)

	def __unicode__(self):
		  return '%s %s %d' % (self.CourseName, self.Code,self.GroupTotalCount)

class CountTable(models.Model):
	TotalCount= models.IntegerField(default=0)
	WeekCount = models.IntegerField(default=0)
	GLS = models.IntegerField(default=0)#GLS
	ISL = models.IntegerField(default=0)#국제어문
	ME = models.IntegerField(default=0)#경영경제
	SOF = models.IntegerField(default=0)#법학부
	SOCAS = models.IntegerField(default=0)#언론정보
	SESE = models.IntegerField(default=0)#공간환경
	MCE = models.IntegerField(default=0)#기계제어
	CCD = models.IntegerField(default=0)#콘텐츠융합디자인학부
	LS = models.IntegerField(default=0)#생명과학부
	CSEE = models.IntegerField(default=0)#전산전자
	CPSW = models.IntegerField(default=0)#상사
	ICT = models.IntegerField(default=0)#ICT
	SCCE = models.IntegerField(default=0)#창의융합교육원

class Course_Evaluation(models.Model):
	Course = models.ForeignKey(Lecture)
	Total_Course_id = models.IntegerField(null=False)
	CreatedID = models.ForeignKey(Profile)
	Speedy = models.PositiveSmallIntegerField(default=5, null=False)
	Homework = models.PositiveSmallIntegerField(default=5, null=False)
	Level_Difficulty = models.PositiveSmallIntegerField(default=5, null=False)
	Check = models.BooleanField(default=False)
	CourseComment = models.TextField(max_length=2000)
	StarPoint =models.FloatField(default=0)
	What_Answer = models.IntegerField(default=0)
	Exam_Answer = models.ManyToManyField(Description_Answer)
	Who_Answer = models.TextField(max_length=200, null=True)
	
	Course_Answer = models.IntegerField(default=0)
	Url_Answer = models.TextField(max_length=200, null=True)
	create_date = models.DateTimeField(default=datetime.datetime.today())
	update_date = models.DateTimeField(default=datetime.datetime.today())
	
	def __unicode__(self):
			return '%s %s %s %s %s %d' % (self.Course.Code,self.Course.Professor, self.Course.CourseName,self.CreatedID,self.Course.Semester,self.Total_Course_id)
class UploadFile(models.Model):
	CreatedID = models.ForeignKey(Profile)
	Course = models.ForeignKey(Total_Evaluation)
	upload_file = models.FileField(max_length=1000,storage=OverwriteStorage(),default=None,upload_to=upload_path_handler)
	UserCourse = models.ForeignKey(Course_Evaluation,null=True)

 
# Create your models here.
