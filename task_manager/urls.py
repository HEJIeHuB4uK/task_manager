from django.urls import path
from main import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/v1/signup/', views.sign_up_user, name='signup'),
    path('api/v1/login/', views.log_in_user, name='login'),
    path('api/v1/logout/', views.log_out_user, name='logout'),
    path('api/v1/users/', views.user_list, name='users'),
    path('api/v1/projects/', views.project_list, name='projects'),
    path('api/v1/project/<int:pk>/', views.update_project, name='update_projects'),
    path('api/v1/tasks/', views.task_list, name='tasks'),
    path('api/v1/task/<int:pk>/', views.update_task, name='update_task'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'), 
]