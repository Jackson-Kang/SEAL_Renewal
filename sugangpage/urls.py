from django.conf.urls import url

from sugangpage import views

urlpatterns = [
	url(r'^SugangChange/',views.SugangPageView.as_view(),name="SugangChange"),
 	url(r'^SugangInsert/',views.SugangPageCreateView.as_view(),name="SugangInsert"),
 	url(r'^SugangDelete/',views.SugangPageDeleteView.as_view(),name="SugangDelete"),
 	url(r'^SugangPageNation/(?P<page>\d+)$',views.SugangPageView.as_view(),name="SugangDelete"),
]