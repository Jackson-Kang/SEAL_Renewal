# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from lecture.models import Lecture

class Profile(models.Model):
	class Meta:
		verbose_name = u'프로필'
		verbose_name_plural = u'프로필'
	User = models.OneToOneField(settings.AUTH_USER_MODEL)
	FirstMajor = models.CharField(max_length=30)
	SecondMajor = models.CharField(max_length=30)
	UserName = models.CharField(max_length=30)
	Point = models.IntegerField(default=0)
	RecommendCount = models.IntegerField(default=0)
	LikeCount = models.IntegerField(default=0)
	LectureRecord = models.TextField(null=True)
	MyLecture = models.ManyToManyField(Lecture)
	
	def __unicode__(self):
		return self.User.username


# Create your models here.
