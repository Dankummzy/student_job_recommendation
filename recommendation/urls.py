# recommendation/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('input/', views.student_input, name='student_input'),
    path('recommendations/<int:user_id>/', views.recommendation_page, name='recommendation_page'),
    path('profile/', views.user_profile, name='user_profile'),
    path('history/', views.recommendations_history, name='recommendations_history'),
]
