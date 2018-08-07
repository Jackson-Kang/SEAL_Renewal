from django.db import models

# Create your models here.
class Lecture(models.Model):
	Semester = models.CharField(max_length=10, null=False)
	Category = models.CharField(max_length=20, null=False)
	Code = models.CharField(max_length=20, null=False)
	Class = models.PositiveSmallIntegerField(default=1, null=True)
	CourseName = models.CharField(max_length=80, null=True)
	CourseName_Eng = models.CharField(max_length=80, null=True)
	Credit = models.CharField(max_length=4, null=True)
	Major = models.CharField(max_length=40, null=True)
	Professor = models.CharField(max_length=30, null=True)
	Period = models.CharField(max_length=150, null=True, blank=True, default=None)
	ClassRoom = models.CharField(max_length=20, null=True, blank=True, default=None)
	Fix_num = models.PositiveSmallIntegerField(default=0, null=True)
	Take_num = models.CharField(max_length=5, null=True, blank=True)
	EnglishRatio = models.CharField(max_length=10, null=True)
	CategoryDetail = models.CharField(max_length=20, null=True, blank=True, default=None)

	def __unicode__(self):
		rt_name = "%s %s %s" % (self.CourseName, self.Professor, self.Code )
		return rt_name
	