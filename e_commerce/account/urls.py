from django.urls import path
from account import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.Customerlogin, name='login')
]