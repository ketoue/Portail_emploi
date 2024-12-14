from django.urls import path
from . import views

urlpatterns = [
   path('', views.dashboard, name='dashboard'),
    path('recruiter/cvs/', views.recruiter_cvs, name='recruiter-cvs'),
    
   
]
