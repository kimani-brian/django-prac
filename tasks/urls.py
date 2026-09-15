from django.urls import path
from . import views

urlpatterns = [
    # Website URL
    path('', views.home, name='home'),
    
    # API URL
    path('api/tasks/', views.TaskList.as_view(), name='task-list-api'),
    #path('api/tasks/<int:pk>/', views.TaskDetail.as_view(), name='task-detail-api'),

]