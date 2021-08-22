from django.urls import path, include
from django.conf import settings
from . import views
from django.contrib import admin
from django.conf.urls.static import static



urlpatterns =[
	path('home/',views.home),
	path('',views.home),
    path('login/', views.login_call),
    path('signup/', views.signup_call),
    path('logout/', views.logout_call),
    path('interest/', views.interest),
    path('time/',views.timesp,name='timesp'),
    path('single/',views.single_page, name='single_page'),

    path('news/',views.news_api, name="news_api")


]
