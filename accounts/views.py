# Fungsi untuk mengirim dan menerima informasi dari template
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

# Fungsi untuk autentikasi dan session
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Model dan Form
from accounts.forms import UserForm, AkunRegistrationForm
from accounts.models import PasienInfo, PetugasInfo, DokterInfo, ApotekerInfo

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
    container.tipe = akunForm.cleaned_data['tipe']

    return container

## Fungsi register untuk semua jenis akun
def akun_register(request, tipe):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
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
            if tipe == 1:
                messages.info(request, "Username telah digunakan")
            else:
                messages.info(request, "Nomor Pegawai telah digunakan")
            return redirect("accounts:akun_register", tipe=tipe)
    else:
        user_form = UserForm()
        akun_form = AkunRegistrationForm()

    return render(request, "akun_register.html", context={
                                                        'registered': registered,
                                                        'user_form': user_form,
                                                        'akun_form': akun_form,
                                                        'tipe': tipe,
                                                     })
# Halaman untuk login akun
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

def akun_login(rqeuest):
    

# Halaman home untuk pengguna yang sudah login
def home(request):
    waktu = datetime.datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")
    if request.user.is_authenticated:
        if request.user.user_type == 1:
            return render(request, 'petugas/homInformasi tidak valide.html', {'waktu': waktu})
        if request.user.user_type == 2:
            return render(request, 'dokter/home.html', {'waktu': waktu})
        if request.user.user_type == 3:
            return render(request, 'apoteker/home.html', {'waktu': waktu})
