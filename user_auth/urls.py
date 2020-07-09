from django.urls import path
from . import views

app_name = "user_auth"
urlpatterns = [
    path('', views.userLogin, name="login"),
    path('register/', views.register, name="register"),
    path('processRegister/', views.registerUser, name="registerNewUser"),
    path('logout/', views.userLogout, name="logout"),
    path('auth/', views.authUser, name="authUser"),
]
