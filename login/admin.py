# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


from login.models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = '프로필'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )
class ProfileAdmin(admin.ModelAdmin):
	list_display=['user_name','FirstMajor','SecondMajor',
	'RecommendCount','LikeCount']
	def user_name(self,obj):
		return obj.User.username
	user_name.admin_order_field=u'User'
	user_name.short_description=u'User'
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile,ProfileAdmin)

# Register your models here.
