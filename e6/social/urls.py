from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers



urlpatterns = [
    path('accounts/profile/<slug:username>', profileview, name='profile'),
    path('accounts/profilechange', profilechange, name='profilechange'),
    path('accounts', userlist, name='accounts'),
    path('chats', chatlist, name='chats'),
    path('chats/<slug:username>', usertouserchat, name='usertouserchat'),
    path('api/messages', MessageList.as_view()),

]
