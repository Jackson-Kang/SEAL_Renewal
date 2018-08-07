from django.conf.urls import url

from recommend import views

urlpatterns = [
	url(r'^Recommend$', views.RecommendView.as_view(),name='Recommend'),
	url(r'^CourseSearchList/$',views.CourseListView.as_view(),name="CourseSearch"),
	url(r'^Course-Semester/$',views.CourseSelectView.as_view(),name="CourseSemester"),
	url(r'^RecommendWrite$',views.RecommendWriteView.as_view(),name="RecommendCreate"),

]