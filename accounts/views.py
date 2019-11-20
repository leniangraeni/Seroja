from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from accounts.forms import UserForm
from django.contrib.auth.decorators import login_required
from accounts.models import User
import datetime

def signup(request):
    return render(request, 'signup.html')

def petugas_signup(request):
    registered = False
    akun = 'Petugas'

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

    return render(request, 'signup_form.html', 
                    {'user_form': user_form,
                     'registered': registered,
                     'akun': akun})

def dokter_signup(request):
    registered = False
    akun = 'Dokter'

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

    return render(request, 'signup_form.html', 
                    {'user_form': user_form,
                     'registered': registered,
                     'akun': akun})

def apoteker_signup(request):
    registered = False
    akun = 'Apoteker'
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

    return render(request, 'signup_form.html', 
                    {'user_form': user_form,
                     'registered': registered,
                     'akun': akun})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('accounts:home')
            # return HttpResponse('Berhasil Login')
        else:
            print("login failed")
            print('Username: {} and password {}'.format(username, password))
    
    else:
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('accounts:login')

def home(request):
    waktu = datetime.datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")
    if request.user.is_authenticated:
        if request.user.user_type == 1:
            return render(request, 'petugas/home.html', {'waktu': waktu})
        if request.user.user_type == 2:
            return render(request, 'dokter/home.html', {'waktu': waktu})
        if request.user.user_type == 3:
            return render(request, 'apoteker/home.html', {'waktu': waktu})