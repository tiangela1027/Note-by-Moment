from django.urls import path
from . import views

app_name = 'hub'
urlpatterns = [
    path('', views.viewCollections, name="home"),
    path('add/', views.addStamp, name="add"),
    path('submitStamp/', views.submitStamp, name="submit"),
    path('calendar/', views.calendar, name="calendar"),
    path('updateCalendar/', views.updateCalendar, name="updateCalendar"),
    path('userProfile/', views.userProfile, name="user"),
    path('updateUser/', views.updateUserProfile, name="updateUserProfile")
]
