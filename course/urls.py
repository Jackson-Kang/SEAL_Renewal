from django.conf.urls import url

from course import views

urlpatterns = [
	url(r'^Course/(?P<courseid>\d+)$',views.CourseView.as_view(),name="Course"),
	url(r'^Course/(?P<courseid>\d+)/(?P<page>\d+)$',views.CourseView.as_view(),name="Page"),
	url(r'^download/',views.DownloadView.as_view(),name="Download")
]