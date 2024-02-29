from django.shortcuts import render, redirect
from .models import Profile
from .forms import ChangeProfile
from django.contrib.auth.models import User
from django.core.paginator import Paginator


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