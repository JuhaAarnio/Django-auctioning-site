from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('profile/', views.EditProfile.as_view(), name='editprofile'),
    path('', views.EditProfile.as_view(), name='user'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('home/', views.Home.as_view(), name='home'),
]