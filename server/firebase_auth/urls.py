from django.urls import path
from .views import Home, Register, Login 

urlpatterns = [
    path('home/', Home.as_view(), name='home'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
]