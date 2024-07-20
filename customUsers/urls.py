from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('user_info/', views.user_info_view, name='user_info'),
    path('update_user/', views.update_user_view, name='update_user'),
    path('change_password/', views.change_password_view, name='change_password'),
]
