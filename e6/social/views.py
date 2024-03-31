from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile, ChatMessages, Room, Message
from .forms import ChangeProfile, CreateRoom
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from .serializers import *

# Create your views here.
@login_required
def index(request):
    return redirect('accounts')
def profileview(request, username):
    profileuser = User.objects.filter(username=username).first()
    if not profileuser:
        ...
    return render(request, 'profile.html', {'title':f'Профиль {profileuser}', 'profileuser':profileuser})

@login_required
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

@login_required
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

@login_required
def roomlist (request):
    rooms = Room.objects.filter(members=request.user, ischat=False)
    context = {
        'title':'Комнаты',
        'rooms':rooms,
    }
    return render(request, 'rooms.html', context)

@login_required
def createroom(request):
    context = {
        'title': 'Создание комнаты',
    }
    if request.method=='GET':
        context['form']=CreateRoom()
    elif request.method=='POST':
        roomname = request.POST['roomname']
        room = Room.objects.filter(roomname=roomname).first()
        if room:
            context['form'] = CreateRoom(request.POST)
            context['form'].add_error(None, 'Такое название комнаты уже занято!')
        else:
            members = dict(request.POST)['listuser']
            room = Room.objects.create(roomname=roomname, admin=request.user, ischat=False)
            room.members.add(*members)
            room.save()

            return redirect('room', roomname=room.roomname)

    return render(request, 'createroom.html', context)

@login_required
def roomview(request, roomname):
    room = Room.objects.get(roomname=roomname)
    messages = Message.objects.filter(room=room)
    context = {
        'title': f'Комната {roomname}',
        'room': room,
        'messages':messages,
    }
    if request.user not in room.members.all():
        return redirect('rooms')
    return render(request, 'room.html', context)

@login_required
def usertouserchat(request, username):
    chat = Room.objects.filter(ischat=True, members=request.user).filter(members=User.objects.get(username=username)).first()
    if not chat:
        chat = Room.objects.create(ischat=True).members.add(request.user, User.objects.get(username=username))

    messages = Message.objects.filter(room=chat)
    context = {
        'title': f'Чат с {username}',
        'messages': messages,
        'chat_id': chat.id,
    }
    return render(request, 'chat.html', context)



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

class AddUserToRoom(APIView):
    def post(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
        except:
            return Response({'error':'Пользователь не найден'}, status=400)
        try:
            room = Room.objects.get(id=request.data['roomid'])
            if user in room.members.all():
                return Response({'error': 'Данный пользователь уже есть в комнате'}, status=400)
            room.members.add(user)
            return Response({'username': user.username})
        except:
            return Response({'error': 'Что то пошло не так...'}, 400)

class DelUserFromRoom(APIView):
    def delete(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
            room = Room.objects.get(id=request.data['roomid'])
        except:
            return Response(status=500)
        if not request.user==room.admin:
            return Response(status=403)
        room.members.remove(user)
        return Response( status=200)

