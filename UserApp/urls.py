from django.urls import path
from UserApp import views
urlpatterns=[
    path('login', views.login),
    path('register', views.register),
    path('RegAction', views.RegAction),
    path('logaction', views.logaction),
    path('viewprofile', views.viewprofile),
    path('uploadtest', views.uploadtest),
    path('CropAction', views.CropAction),
    path('feedbackAction', views.feedbackAction),
    path('feedback', views.feedback),
    path('home', views.home),

]
