# -*- coding: utf-8 -*-
# -*- coding: euc-kr -*-


from django.db import models
from lecture.models import Lecture
from login.models import Profile
from index.models import Course_Evaluation



#두개다 one to many 관계라서 뭘고쳐야할지 모르겠넴

class Recommend_Course(models.Model):
	Course = models.ForeignKey(Course_Evaluation)
	CreatedID = models.ForeignKey(Profile)

	def __unicode__(self):
		return u'%s %s %s' % (self.Course.Course.CourseName,self.Course.Course.Professor, self.CreatedID.UserName)

class Like_Course(models.Model):
	Course = models.ForeignKey(Lecture)
	CreatedID = models.ForeignKey(Profile)

	def __unicode__(self):
		return u'%s %s' % (self.Course.CourseName, self.CreatedID.UserName)
# Create your models here.
