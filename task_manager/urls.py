from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/signup/', views.sign_up_user, name='signup'),
    path('api/v1/login', views.log_in_user, name='login'),
    path('api/v1/logout', views.log_out_user, name='logout'),
    # path('api/v1/users', views.user_list, name='users'),
]