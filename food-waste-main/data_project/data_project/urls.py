"""
URL configuration for data_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import home_view, register_view, login_view, create_quest_view, accepted_quests_view, quest_list_view, my_quests_view, upload_receipt_view, navbar_view, delete_quest_view

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('home/', home_view, name='home'),
    path('create_quest/', create_quest_view, name = 'create_quest'),
    path('accepted_quests/', accepted_quests_view, name = 'accepted_quests'),
    path('quest_list/', quest_list_view, name = 'quest_list'),
    path('my_quests/', my_quests_view, name = 'my_quests'),
    path('navbar/', navbar_view, name = 'navbar'),
    path('delete_quest/<str:item>/', delete_quest_view, name='delete_quest'),
    path('upload_receipt/', upload_receipt_view, name = 'upload_receipt')
    ]

