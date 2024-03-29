from django.urls import path
from .import views

urlpatterns = [
     path('login/', views.loginPage, name="login"),

     path('', views.home, name="home"),
     path('space/<str:pk>/', views.space, name="space"),
     path('takingPhoto/', views.takingPhoto, name="takingPhoto"),

     path('create-space/', views.createSpace, name="create-space"),
     path('update-space/<str:pk>/', views.updateSpace, name="update-space"),
     path('delete-space/<str:pk>/', views.deleteSpace, name="delete-space"),

]