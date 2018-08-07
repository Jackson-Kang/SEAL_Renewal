from django.conf.urls import url

from lecture import views

urlpatterns = [
	url(r'^UpdateDB/$', views.UpdateLoginView.as_view(),name='UpdateDB'),
	url(r'^CurUpdate/$', views.AutoFastLecUpdateView.as_view(),name='Curupdate'),
]