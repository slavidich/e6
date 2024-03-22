from django.shortcuts import render, redirect
from rest_framework.response import Response

from .models import Profile, ChatMessages, Room, Message
from .forms import ChangeProfile, CreateRoom
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from .serializers import *

# Create your views here.
def profileview(request, username):
    profileuser = User.objects.filter(username=username).first()
    if not profileuser:
        ...
    return render(request, 'profile.html', {'title':f'Профиль {profileuser}', 'profileuser':profileuser})

def profilechange(request):
    user = request.user
    if not Profile.objects.filter(user=user):
        Profile.objects.create(user=user)
    if request.method == 'POST':
        form = ChangeProfile(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            form.save()
            return redirect('profile', user.username)
    else:

        form = ChangeProfile(instance=user.profile)
    context = {
        'title': 'Редактирование профиля',
        'form':form,
    }
    return render(request, 'profilechange.html', context)

def userlist(request):
    currentpage = int(request.GET.get('page') or 1)
    usernamesearch = request.GET.get('username')
    users = User.objects.filter(username__contains=usernamesearch)[:5] if usernamesearch else User.objects.all()
    p = Paginator(users, 7)
    pagelist = list(p.get_elided_page_range(currentpage, on_each_side=1, on_ends=1))
    users = p.get_page(currentpage)
    context = {
        'title': 'Все пользователи',
        'users': users,
        'usernamesearch': usernamesearch,
        'pagelist': pagelist,
        'currentpage': currentpage,
    }
    return render(request, 'userlist.html', context)

def roomlist (request):

    context = {
        'title':'Комнаты'
    }
    return render(request, 'rooms.html', context)

def createroom(request):
    context = {
        'title': 'Создание комнаты',
    }
    if request.method=='GET':
        context['form']=CreateRoom()
    elif request.method=='POST':
        context['form']= CreateRoom(request.POST)
        context['form'].add_error(None, 'none field erorr')

    return render(request, 'createroom.html', context)


def usertouserchat(request, username):
    chat = Room.objects.filter(ischat=True, members=request.user).filter(members=User.objects.get(username=username)).first()
    if not chat:
        chat = Room.objects.create(ischat=True).members.add(request.user, User.objects.get(username=username))

    if request.method=='POST':
        text =  request.POST.get('textmsg')
        if text:
            Message.objects.create(room=chat[0], sender=request.user, text=text)

    messages = Message.objects.filter(room=chat)


    context = {
        'title': f'Чат с {username}',
        'messages': messages,
        'chat_id': chat.id,
    }
    return render(request, 'chat.html', context)

def roomview(request, roomname):
    context = {
        'title': f'Комната {roomname}'
    }
    return render(request, 'rooms.html', context)

# --- API ---
class MessageList(generics.ListCreateAPIView):
   queryset = Message.objects.all()
   serializer_class = MessageSerializer

class UserSearchByUserName(generics.GenericAPIView):
    serializer_class = UserSearchByUsernameSerializer
    def get(self, request, format=None):
        username =  request.query_params['username']
        try:
            user = User.objects.get(username=username)
            serializer = UserSearchByUsernameSerializer(user, many=False)
            return Response(serializer.data)
        except:
            return Response(status=418)



