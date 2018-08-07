from rest_framework import serializers

from index.models import Total_Evaluation, Course_Evaluation
from lecture.models import Lecture
class Total_Evaluation_Serializer(serializers.ModelSerializer):
	Course_Name=serializers.ReadOnlyField(source='Course.CourseName', read_only=True)
	class Meta:
		model = Total_Evaluation
		fields = ('Course_Name','Total_Homework','Total_Level_Difficulty',
				'Total_Count','Total_StarPoint','Total_Recommend'
			,'Total_Mix','Total_Short_Answer','Total_Long_Answer',
			'Total_Unknown_Answer','Total_Book_Like','Total_Ppt_Like','Total_Practice_Like')