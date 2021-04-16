from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('themes/', views.ThemesView.as_view(), name='themes'),
    path('handler/', views.handler, name='handler'),
    path('themes/<str:theme_name>', views.ThemeView.as_view(), name='theme'),
    path('themes/tasks/<int:task_id>', views.TaskView.as_view(), name='task'),
    path('themes/tasks/upload', views.upload_task, name='upload_task')
]