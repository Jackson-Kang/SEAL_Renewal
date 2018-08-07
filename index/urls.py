from django.conf.urls import url

from index import views

from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
	url(r'^Search/',views.SearchView.as_view(),name="Search"),
	url(r'^Page/(?P<page>\d+)$',views.MainPageView.as_view(),name="Page"),
	url(r'^CPage/(?P<page>\d+)$',views.CategorySystemView.as_view(),name="CategoryPage"),
	url(r'^SPage/(?P<page>\d+)$',views.SearchView.as_view(),name="SearchPage"),
	url(r'^Category_Change/',views.CategorySystemView.as_view(),name="CategorySystem"),
	url(r'^MyCourse/$',views.MyCourseView.as_view(),name="MyCourse"),
	url(r'^MyCourse/(?P<page>\d+)$',views.MyCourseView.as_view(),name="MPage"),
	url(r'^AutoSearch/$',views.AutoSearchView.as_view(),name="AutoSearch"),
	url(r'^renewDB/$',views.renewDB),
	url(r'^StudentInformationChangeView/$',views.StudentInformationChangeView.as_view(),name="InformationChange"),
	url(r'^api/GetTotalCourse/(?P<page>\d+)$',views.JsonResponse_Total_Evaluation.as_view(),name="GetTotalCourse")
]

urlpatterns = format_suffix_patterns(urlpatterns)