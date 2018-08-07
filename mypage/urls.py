from django.conf.urls import url

from mypage import views

urlpatterns = [
	url(r'^MyPage/$',views.MyPageView.as_view(),name="MyPage"),
	url(r'^MyPage/NickNameChange/$',views.NickNameChangeView.as_view(),name="NickNameChange"),
	url(r'^MyPage/UpdateRedirectCourse/$',views.MyCourseUpdateRedirectView.as_view(),name="UpdateRedirectCourse"),
	url(r'^MyPage/UpdateCourse/$',views.MyCourseUpdateView.as_view(),name="UpdateCourse"),
	url(r'^MyPage/DeleteCourse/$',views.MyCourseDeleteView.as_view(),name="DeleteCourse"),
]
