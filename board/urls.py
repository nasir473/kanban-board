from django.urls import path
from . import views

urlpatterns = [
    path('', views.board_view, name='board'),
    path('create/', views.create_task, name='create_task'),
    path('update/<int:task_id>/', views.update_task_status, name='update_task_status'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
]
