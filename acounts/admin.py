# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
 
from acounts.models import Profile
 
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = '프로필'
 
# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )
 
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# Register your models here.
