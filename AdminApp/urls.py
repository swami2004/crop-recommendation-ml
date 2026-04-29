from django.urls import path
from AdminApp import views

urlpatterns = [
    path('', views.index),
    path('login', views.login, name='login'),
    path('logaction', views.logaction, name='logaction'),
    path('logout', views.admin_logout, name='admin_logout'),
    path('home', views.adminhome, name='admin_dashboard'),
    path('upload', views.upload, name='upload'),
    path('preprocess', views.preprocess, name='preprocess'),
    path('decision', views.decision, name='train_decision_tree'),
    path('svm', views.svm, name='train_svm'),
    path('comparison', views.comparison, name='model_comparison'),
    path('user_management', views.user_management, name='user_management'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('view_user/<int:user_id>/', views.view_user_details, name='view_user'),
    path('data_management', views.data_management, name='data_management'),
    path('model_management', views.model_management, name='model_management'),
]
