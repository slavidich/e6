from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers



urlpatterns = [
    path('accounts/profile/<slug:username>', profileview, name='profile'),
    path('accounts/profilechange', profilechange, name='profilechange'),
    path('accounts', userlist, name='accounts'),
    path('rooms', roomlist, name='rooms'),
    path('room/<slug:roomname>', roomview, name='room'),
    path('create/room', createroom, name='createroom'),
    path('chats/<slug:username>', usertouserchat, name='usertouserchat'),
    path('api/searchuser', UserSearchByUserName.as_view()),
    path('', index),
]
