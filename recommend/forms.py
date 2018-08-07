from django import forms

from index.models import Course_Evaluation
class SearchCourseForm(forms.Form):
	pass
class RecommendForm(forms.Form):
	def __init__(self,*args,**kwargs):
		super(RecommendForm, self).__init__(*args, **kwargs)
		CourseName=forms.CharField()
		Code=forms.CharField()
		Professor=forms.CharField()
		Homework = forms.IntegerField()
		Level_Difficulty = forms.IntegerField()
		CourseComment = forms.CharField(widget=forms.Textarea())
		StarPoint =forms.FloatField()
		Who_Answer = forms.CharField()
class RecommendQueryForm(forms.Form):
	def __init__(self,qs=None,qs2=None,*args,**kwargs):
		super(RecommendQueryForm, self).__init__(*args, **kwargs)
		Course = forms.ModelChoiceField(queryset=qs)
		CreatedID = forms.ModelChoiceField(queryset=qs2)
		