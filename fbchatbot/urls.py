from django.conf.urls import url
from fbchatbot import views

urlpatterns = [
	
	url(r'^$',views.fbchat,name="fbchat"),
	url(r'^/prescription$', views.index),
	url(r'^/prescribe$', views.prescribe),
	url(r'^/call_reminder$', views.call_reminder),
]