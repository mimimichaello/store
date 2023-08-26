from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

# from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid(): # Проверка на валидность
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password) # Проверка на подлинность
            if user: # Проверка действительно ли есть такой пользователь
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index')) # / означает, что перенаправление идет на главную страницу

    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поздравляем, Вы успешно зарегистрировались!!!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)

def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        # instance=request.user - чтобы данные обновлялись, а не перезаписывались
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user) # instance=request.user - чтобы отображались данные после регистрации
    context = {'title': 'Store - Профиль',
               'form': form,
               'baskets': Basket.objects.filter(user=request.user),
               }
    return render(request, 'users/profile.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index')) # Выход из системы
