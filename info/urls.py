from django.urls import path
from .import views

urlpatterns = [
    path('update-info/', views.update_info, name='update-info'),
    path('info-details/<int:pk>/', views.info_details, name='info-details'),
    path('edit-info/<int:job_pk>/', views.edit_info, name='edit-info'),

]
