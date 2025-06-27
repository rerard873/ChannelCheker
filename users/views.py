
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect
from  django.contrib import auth
from users.forms import UserAuthForm

from users.forms import UserRegisterForm, AvatarChangeForm


# Create your views here.
# TODO  добписть автоирзацию а именно ограничить количество попыток, сообщения пльзователю
# TODO сообщение вы успешно зарегестрировались
def login(request):
    if request.method == 'POST':
        form = UserAuthForm(data = request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username = username, password = password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('home'))
    else:
        form = UserAuthForm()
    context = {'form' : form}
    return render(request,'users/login.html',context)
# TODO убрать выберете файл если аватара нет и поставить стнаднартный
def profile(request):
    if request.method == "POST":
        form = AvatarChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return  HttpResponseRedirect(reverse('users:profile'))
    else:
        form = AvatarChangeForm(instance=request.user)
    context = {'form': form}
    return render(request,'users/profile.html',context)

# TODO проверка что уже нет в БД и избалвение от повторного захода
# TODO проверка одинаковости логина
# TODO сообщение что пользователь зарегестрировался
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegisterForm()
    context = {'form' : form}
    return render(request,'users/register.html',context)

def logout(request):
    auth.logout(request)
    return  HttpResponseRedirect(reverse('home'))