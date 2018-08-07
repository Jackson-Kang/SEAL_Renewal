from django.db import models

# Create your models here.

class UniversityClass(models.Model):
	ClassName=models.CharField(max_length=30)
	ClassCode=models.CharField(max_length=10)

