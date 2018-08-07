from django.db import models
from login.models import Profile
import datetime
# Create your models here.

class SugangList(models.Model):
	"""docstring for ClassName"""
	CreatedID = models.ForeignKey(Profile)
	Content = models.TextField(max_length=200)
	create_date = models.DateTimeField(default=datetime.datetime.today())
	update_date = models.DateTimeField(default=datetime.datetime.today())
	def __unicode__(self):
		return self.CreatedID.User.username