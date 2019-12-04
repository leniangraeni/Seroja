
# Fungsi untuk mengirim dan menerima informasi dari template
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

# Fungsi untuk autentikasi dan session
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Model dan Form
from accounts.forms import SerojaUserForm, AkunRegistrationForm
from accounts.models import SerojaUser, PasienInfo, PetugasInfo, DokterInfo, ApotekerInfo
from guidelines.models import Guideline

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

def akun_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('pengobatan:beranda', tipe=user.tipe)
        else:
            messages.info(request, "Nomor Pegawai atau Password salah")
            return redirect('accounts:login')
    else:
        return render(request, 'login.html')

def akun_logout(request):
    logout(request)
    return redirect('welcome')
