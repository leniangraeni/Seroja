from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from accounts.forms import UserForm
from django.contrib.auth.decorators import login_required
from accounts.models import User


def petugas_signup(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
            if 'surat_tugas' in request.FILES:
                user.surat_tugas = request.FILES['surat_tugas']

            user.set_password(user.password)
            user.user_type  = 1
            user.save()

            registered = True
            return HttpResponse('Berhasil membuat akun')
        
        else:
            print(user_form.errors)
    
    else:
        user_form = UserForm()

    return render(request, 'signup.html', 
                    {'user_form': user_form,
                     'registered': registered})

def dokter_signup(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
            if 'surat_tugas' in request.FILES:
                user.surat_tugas = request.FILES['surat_tugas']

            user.set_password(user.password)
            user.user_type  = 2
            user.save()

            registered = True
            return HttpResponse('Berhasil membuat akun')
        
        else:
            print(user_form.errors)
    
    else:
        user_form = UserForm()

    return render(request, 'signup.html', 
                    {'user_form': user_form,
                     'registered': registered})

def apoteker_signup(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
            if 'surat_tugas' in request.FILES:
                user.surat_tugas = request.FILES['surat_tugas']

            user.set_password(user.password)
            user.user_type  = 3
            user.save()

            registered = True
            return HttpResponse('Berhasil membuat akun')
        
        else:
            print(user_form.errors)
    
    else:
        user_form = UserForm()

    return render(request, 'signup.html', 
                    {'user_form': user_form,
                     'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.user_type == 1:
                login(request, user)
                return HttpResponse('Berhasil login petugas')
            if user.user_type == 2:
                login(request, user)
                return HttpResponse('Berhasil login dokter')
            if user.user_type == 3:
                login(request, user)
                return HttpResponse('Berhasil login apoteker')
            
        else:
            print("login failed")
            print('Username: {} and password {}'.format(username, password))
    
    else:
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return HttpResponse('Berhasil Logout')
