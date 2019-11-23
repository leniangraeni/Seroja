# Fungsi untuk mengirim dan menerima informasi dari template
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
<<<<<<< HEAD
from accounts.forms import UserForm
from django.contrib.auth.decorators import login_required
from accounts.models import User
import datetime
from guidelines.models import Guideline


waktu = datetime.datetime.now()
waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")

def signup(request):
    return render(request, 'signup.html')

def petugas_signup(request):
    registered = False
    akun = 'Petugas'

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
=======
from django.contrib import messages
>>>>>>> 43e1ff24caf09a50950986b8b13a4b93fbea6ddc

# Fungsi untuk autentikasi dan session
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Model dan Form
from accounts.forms import SerojaUserForm, AkunRegistrationForm
from accounts.models import SerojaUser, PasienInfo, PetugasInfo, DokterInfo, ApotekerInfo

# Fungsi utilitas
import datetime

# Halaman pilihan jenis login
def register(request):
    return render(request, "register.html")

# Halaman untuk mendaftar akun dan menyimpan dalam database
## Fungsi utilitas untuk menyimpan informasi dengan form biasa
def akun_to_model(akunForm, modelTemplate):
    container = modelTemplate()
    container.nama = akunForm.cleaned_data['nama']
    container.tempat_lahir = akunForm.cleaned_data['tempat_lahir']
    container.tanggal_lahir = akunForm.cleaned_data['tanggal_lahir']
    container.jenis_kelamin = akunForm.cleaned_data['jenis_kelamin']
    container.nomor_telepon = akunForm.cleaned_data['nomor_telepon']
    container.alamat = akunForm.cleaned_data['alamat']

    return container

## Fungsi register untuk semua jenis akun
def akun_register(request, tipe):
    registered = False

    if request.method == "POST":
        user_form = SerojaUserForm(data=request.POST)
        akun_form = AkunRegistrationForm(data=request.POST)

        if user_form.is_valid() and akun_form.is_valid():
            user_data = user_form.save()
            user_data.set_password(user_data.password)
            user_data.save()

            if tipe == 'pasien':
                akun_data = akun_to_model(akun_form, PasienInfo)
            elif tipe == 'petugas':
                akun_data = akun_to_model(akun_form, PetugasInfo)
            elif tipe == 'dokter':
                akun_data = akun_to_model(akun_form, DokterInfo)
            elif tipe == 'apoteker':
                akun_data = akun_to_model(akun_form, ApotekerInfo)

            akun_data.user = user_data
            akun_data.save()

            registered = True
        else:
            if tipe == 'pasien':
                messages.info(request, "Username telah digunakan")
            else:
                messages.info(request, "Nomor Pegawai telah digunakan")
            return redirect("accounts:akun_register", tipe=tipe)
    else:
        user_form = SerojaUserForm()
        akun_form = AkunRegistrationForm()

    return render(request, "akun_register.html", context={
                                                        'registered': registered,
                                                        'user_form': user_form,
                                                        'akun_form': akun_form,
                                                        'tipe': tipe,
                                                     })
# Halaman untuk login akun
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect('accounts:home')
#             # return HttpResponse('Berhasil Login')
#         else:
#             print("login failed")
#             print('Username: {} and password {}'.format(username, password))
#
#     else:
#         return render(request, 'login.html')

def akun_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('accounts:home')
        else:
            messages.info(request, "Nomor Pegawai atau Password salah")
            return redirect('accounts:login')
    else:
        return render(request, 'login.html')

def akun_logout(request):
    logout(request)
    return redirect('welcome')

# Halaman home untuk pengguna yang sudah login
## Utilitas untuk mendapatkan informasi akun berdasarkan tipe
def load_akun_by_tipe(user, tipe):
    if tipe == 'petugas':
        akun_data = PetugasInfo.objects.get(user=user)
    elif tipe == 'dokter':
        akun_data = DokterInfo.objects.get(user=user)
    elif tipe == 'apoteker':
        akun_data = ApotekerInfo.objects.get(user=user)
    return akun_data

## Halaman beranda/Home
def home(request):
<<<<<<< HEAD
    if request.user.is_authenticated:
        if request.user.user_type == 1:
            return render(request, 'petugas/home.html', {'waktu': waktu})
        if request.user.user_type == 2:
            return render(request, 'dokter/home.html', {'waktu': waktu})
        if request.user.user_type == 3:
            return render(request, 'apoteker/home.html', {'waktu': waktu})

def log_obat(request):
    if request.user.is_authenticated:
        if request.user.user_type == 2:
            return render(request, 'dokter/log_pemberian_obat.html', {'waktu': waktu})
        if request.user.user_type == 3:
            return render(request, 'apoteker/log_obat_keluar.html', {'waktu': waktu})

def profil(request):
    if request.user.is_authenticated:
        if request.user.user_type == 1:
            return render(request, 'petugas/profil.html', {'waktu': waktu})
        if request.user.user_type == 2:
            return render(request, 'dokter/profil.html', {'waktu': waktu})
        if request.user.user_type == 3:
            return render(request, 'apoteker/profil.html', {'waktu': waktu})

def pengaturan(request):
    if request.user.is_authenticated:
        if request.user.user_type == 1:
            return render(request, 'petugas/pengaturan.html', {'waktu': waktu})
        if request.user.user_type == 2:
            return render(request, 'dokter/pengaturan.html', {'waktu': waktu})
        if request.user.user_type == 3:
            return render(request, 'apoteker/pengaturan.html', {'waktu': waktu})

def antrian_pasien(request):
    if request.user.is_authenticated:
        if request.user.user_type == 1:
            return render(request, 'petugas/antrian_pasien.html', {'waktu': waktu})

def poli(request):
    if request.user.is_authenticated:
        if request.user.user_type == 1:
            return render(request, 'petugas/poli.html', {'waktu': waktu})

def petunjuk(request):
    if request.user.is_authenticated:
        if request.user.user_type == 1:
            guides = Guideline.objects.all()
            return render(request, 'petugas/petunjuk.html', 
                        {'guides' : guides,
                        'waktu': waktu})
=======
    waktu = datetime.datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")
    user = request.user
    if user.is_authenticated:
        akun = load_akun_by_tipe(user, user.tipe)
        return render(request, 'home.html', context={
                                                'waktu': waktu,
                                                'user': akun,
                                            })
>>>>>>> 43e1ff24caf09a50950986b8b13a4b93fbea6ddc
