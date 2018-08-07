from django.contrib import admin
from index.models import *


class Total_EvaluationAdmin(admin.ModelAdmin):
	list_display=['course_name','Total_Homework','Total_Speedy',
	'Total_Level_Difficulty','Total_Count','Total_StarPoint']
	def course_name(self,obj):
		return obj.Course.CourseName
	course_name.admin_order_field=u'CourseName'
	course_name.short_description=u'CourseName'
class Course_EvaluationAdmin(admin.ModelAdmin):
	list_display=['student_name','course_name','Homework','Speedy',
	'Level_Difficulty','StarPoint']
	def student_name(self,obj):
		return obj.CreatedID.User.username
	def course_name(self,obj):
		return obj.Course.CourseName
	student_name.admin_order_field=u'Student'
	student_name.short_description=u'Student'

class UploadAdmin(admin.ModelAdmin):
	list_display=['student_name','upload_file']
	def student_name(self,obj):
		return obj.CreatedID.User.username
	
admin.site.register(Description_Answer)	
admin.site.register(Course_Evaluation,Course_EvaluationAdmin)
admin.site.register(Total_Evaluation,Total_EvaluationAdmin)
admin.site.register(Group_Total_Evaluation)
admin.site.register(CountTable)
admin.site.register(UploadFile)

# Register your models here.
