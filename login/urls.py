from django.conf.urls import url

from login import views

urlpatterns = [
	url(r'^$', views.LoginView.as_view(),name='Login'),
	url(r'^Logout/$',views.LogoutView.as_view(),name='Logout'),
	url(r'^RegisterInfo/$', views.RegisterInfoView.as_view(),name="RegisterInfo"),
	url(r'^Register/$',views.RegisterView.as_view(),name="Register"),
	url(r'^Cancel/$',views.CancelView.as_view(), name="Cancel")
]