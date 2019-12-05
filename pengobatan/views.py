from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse

# Memasukan model dan form
from accounts.models import SerojaUser, PasienInfo, PetugasInfo, DokterInfo, ApotekerInfo
from pengobatan.models import PoliInfo, JadwalPraktekInfo, ObatInfo, PengobatanInfo
from guidelines.models import Guideline
from pengobatan.forms import VerifikasiForm, BerobatForm, SelesaiForm, JadwalForm, PengobatanForm, PenolakanForm, UbahProfilForm, PoliForm
from guidelines.forms import GuidelineForm

# Fungsi utilitas
from datetime import datetime, timedelta, time

# Utilitas untuk mendapatkan nilai waktu penentu awal hari ini dan akhir hari ini
def waktu_hari_ini():
    mulai = datetime.now().date()
    akhir = mulai + timedelta(1)
    waktu_mulai = datetime.combine(mulai, time())
    waktu_akhir = datetime.combine(akhir, time())
    return waktu_mulai, waktu_akhir

# Utilitas untuk mendapatkan informasi akun berdasarkan tipe
def load_akun_by_tipe(user, tipe):
    if tipe == 'pasien':
        akun_data = PasienInfo.objects.get(user=user)
    elif tipe == 'petugas':
        akun_data = PetugasInfo.objects.get(user=user)
    elif tipe == 'dokter':
        akun_data = DokterInfo.objects.get(user=user)
    elif tipe == 'apoteker':
        akun_data = ApotekerInfo.objects.get(user=user)
    return akun_data

## Fungsi utilitas untuk menyimpan informasi dengan form biasa
def profil_to_model(akunModel, akunForm, modelTemplate):
    akunModel.nama = akunForm.cleaned_data['nama']
    akunModel.tempat_lahir = akunForm.cleaned_data['tempat_lahir']
    akunModel.tanggal_lahir = akunForm.cleaned_data['tanggal_lahir']
    akunModel.jenis_kelamin = akunForm.cleaned_data['jenis_kelamin']
    akunModel.nomor_telepon = akunForm.cleaned_data['nomor_telepon']
    akunModel.alamat = akunForm.cleaned_data['alamat']

    return akunModel

# Create your views here.

# Halaman profil pengguna
# Informasi pengguna
def profil(request, tipe):
    waktu = datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")

    if request.user.is_authenticated:
        akun = load_akun_by_tipe(request.user, tipe)
        if request.user.tipe == 'petugas' and tipe == 'petugas':
            return render(request, 'petugas/profil.html', context={
                                                            'waktu': waktu,
                                                            'user': akun,
                                                            })
        if request.user.tipe == 'dokter' and tipe == 'dokter':
            return render(request, 'dokter/profil.html', {'waktu': waktu, 'user': akun})
        if request.user.tipe == 'apoteker' and tipe == 'apoteker':
            return render(request, 'apoteker/profil.html', {'waktu': waktu, 'user': akun})
        else:
            return redirect('welcome')

# Mengubah informasi profil
def ubah_profil(request, tipe):
    waktu = datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")

    if request.user.is_authenticated:
        akun = load_akun_by_tipe(request.user, tipe)
        berubah = False
        if request.method == "POST":
            profil_form = UbahProfilForm(data=request.POST)
            if profil_form.is_valid():
                if request.user.tipe == 'petugas' and tipe == 'petugas':
                    profil_data = PetugasInfo.objects.get(user=request.user)
                    profil_data = profil_to_model(profil_data, profil_form, PetugasInfo)
                elif request.user.tipe == 'dokter' and tipe == 'dokter':
                    profil_data = DokterInfo.objects.get(user=request.user)
                    profil_data = profil_to_model(profil_data, profil_form, DokterInfo)
                elif request.user.tipe == 'apoteker' and tipe == 'apoteker':
                    profil_data = ApotekerInfo.objects.get(user=request.user)
                    profil_data = profil_to_model(profil_data, profil_form, ApotekerInfo)
                profil_data.save()
                berubah = True
                return redirect("pengobatan:ubah_profil", tipe=tipe)
            else:
                messages.info(request, "Perubahan gagal dilakukan")
                return redirect("pengobatan:ubah_profil", tipe=tipe)
        else:
            profil_form = UbahProfilForm()
        if request.user.tipe == 'petugas' and tipe == 'petugas':
            return render(request, 'petugas/ubah_profil.html', context={
                                                                'berubah': berubah,
                                                                'profil_form': profil_form,
                                                                'user': akun,
                                                                'waktu': waktu
                                                                })
        elif request.user.tipe == 'dokter' and tipe == 'dokter':
            return render(request, 'dokter/ubah_profil.html', context={
                                                                'berubah': berubah,
                                                                'profil_form': profil_form,
                                                                'user': akun,
                                                                'waktu': waktu
                                                                })
        elif request.user.tipe == 'apoteker' and tipe == 'apoteker':
            return render(request, 'apoteker/ubah_profil.html', context={
                                                                'berubah': berubah,
                                                                'profil_form': profil_form,
                                                                'user': akun,
                                                                'waktu': waktu,
                                                                })
    else:
        return redirect('welcome')

# Halaman beranda untuk pengguna yang sudah login
def beranda(request, tipe):
    waktu = datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")
    awal, akhir = waktu_hari_ini()

    if request.user.is_authenticated:
        akun = load_akun_by_tipe(request.user, tipe)
        if akun is None:
            return redirect('welcome')
        if request.user.tipe == 'petugas' and tipe == 'petugas':
            berkas = PengobatanInfo.objects.filter(sudah_verifikasi=False, ditolak=False, tanggal_berkunjung__gte=awal, tanggal_berkunjung__lte=akhir).order_by('-tanggal_berkunjung')
            return render(request, 'petugas/beranda.html', context={
                                                                'waktu': waktu,
                                                                'user': akun,
                                                                'berkas': berkas,
                                                            })
        if request.user.tipe == 'dokter' and tipe == 'dokter':
            antrian_pasien = PengobatanInfo.objects.filter(dokter=akun, sudah_verifikasi=True, sudah_ditangani=False, ditolak=False, tanggal_berkunjung__gte=awal, tanggal_berkunjung__lte=akhir).order_by('-tanggal_berkunjung')
            antrian_apotek = PengobatanInfo.objects.filter(dokter=akun, sudah_verifikasi=True, sudah_ditangani=True, tanggal_berkunjung__gte=awal, tanggal_berkunjung__lte=akhir).order_by('-tanggal_berkunjung')
            return render(request, 'dokter/beranda.html', context={
                                                            'waktu': waktu,
                                                            'user': akun,
                                                            'antrian_pasien': antrian_pasien,
                                                            'antrian_apotek': antrian_apotek,
                                                        })
        if request.user.tipe == 'apoteker' and tipe == 'apoteker':
            antrian_obat_masuk = PengobatanInfo.objects.filter(sudah_verifikasi=True, sudah_ditangani=True, sudah_berobat=False, ditolak=False, tanggal_berkunjung__gte=awal, tanggal_berkunjung__lte=akhir).order_by('tanggal_berkunjung')
            log_obat_keluar = PengobatanInfo.objects.filter(sudah_berobat=True)
            return render(request, 'apoteker/beranda.html', context={
                                                            'waktu': waktu,
                                                            'user': akun,
                                                            'antrian_obat_masuk': antrian_obat_masuk,
                                                            'log_obat_keluar': log_obat_keluar,
                                                            })
        return redirect('welcome')
    else:
        return redirect('welcome')

# Halaman detail pengobatan, berisi pilihan validasi atau tolak berkas
def detail_pengobatan(request, tipe, antrian):
    waktu = datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")

    if request.user.is_authenticated:
        akun = load_akun_by_tipe(request.user, tipe)
        if akun is None:
            return redirect('welcome')

        if request.user.tipe == 'petugas' and tipe == 'petugas':
            berkas = PengobatanInfo.objects.get(id=antrian)

            if request.method == "POST":
                penolakan_form = PenolakanForm(data=request.POST, instance=berkas)
                verifikasi_form = VerifikasiForm(data=request.POST)
                if penolakan_form.is_valid():
                    if verifikasi_form.is_valid():
                        if verifikasi_form.cleaned_data['verifikasi'] == '1':
                            berkas.sudah_verifikasi = True
                            berkas.ditolak = False
                        else:
                            berkas = penolakan_form.save()
                            berkas.ditolak = True
                        petugas = PetugasInfo.objects.get(user=request.user)
                        berkas.petugas = petugas
                        berkas.save()
                    else:
                        return HttpResponse("Ada kesalahan")
            else:
                penolakan_form = PenolakanForm(data=request.POST, instance=berkas)
                verifikasi_form = VerifikasiForm()

            return render(request, 'petugas/detail_pengobatan.html', context={
                                                                        'berkas': berkas,
                                                                        'penolakan_form': penolakan_form,
                                                                        'verifikasi_form': verifikasi_form,
                                                                        'user': akun,
                                                                        'waktu': waktu
                                                                    })
        if request.user.tipe == 'dokter' and tipe == 'dokter':
            berkas = PengobatanInfo.objects.get(id=antrian)
            obats = ObatInfo.objects.all()

            if request.method == "POST":
                berobat_form = BerobatForm(data=request.POST)
                obat_form = PengobatanForm(data=request.POST, instance=berkas)
                if obat_form.is_valid():
                    if berobat_form.is_valid():
                        if berobat_form.cleaned_data['berobat'] == '1':
                            berkas = obat_form.save()
                            berkas.sudah_ditangani = True
                            berkas.ditolak = False
                        dokter = DokterInfo.objects.get(user=request.user)
                        berkas.dokter = dokter
                        berkas.save()
                        return redirect("pengobatan:detail_pengobatan", tipe=tipe, antrian=antrian)
                    else:
                        return HttpResponse("Ada kesalahan")
            else:
                berobat_form = BerobatForm()
                obat_form = PengobatanForm(data=request.POST, instance=berkas)

            return render(request, 'dokter/detail_antrian.html', context={
                                                                        'berkas': berkas,
                                                                        'berobat_form': berobat_form,
                                                                        'obat_form': obat_form,
                                                                        'obats': obats,
                                                                        'user': akun,
                                                                        'waktu': waktu
                                                                    })
        if request.user.tipe == 'apoteker' and tipe == 'apoteker':
            berkas = PengobatanInfo.objects.get(id=antrian)

            if request.method == "POST":
                penolakan_form = PenolakanForm(data=request.POST, instance=berkas)
                selesai_form = SelesaiForm(data=request.POST)
                if penolakan_form.is_valid():
                    if selesai_form.is_valid():
                        if selesai_form.cleaned_data['selesai'] == '1':
                            berkas.sudah_berobat = True
                            berkas.ditolak = False
                        elif selesai_form.cleaned_data['selesai'] == '0':
                            berkas = penolakan_form.save()
                            berkas.sudah_berobat = False
                            berkas.ditolak = True
                        apoteker = ApotekerInfo.objects.get(user=request.user)
                        berkas.apoteker = apoteker
                        berkas.save()
                        return redirect("pengobatan:detail_pengobatan", tipe=tipe, antrian=antrian)
                    else:
                        return HttpResponse("Ada kesalahan")
            else:
                selesai_form = SelesaiForm()
                penolakan_form = PenolakanForm(data=request.POST, instance=berkas)

            return render(request, 'apoteker/detail_antrian.html', context={
                                                                        'berkas': berkas,
                                                                        'selesai_form': selesai_form,
                                                                        'penolakan_form': penolakan_form,
                                                                        'user': akun,
                                                                        'waktu': waktu
                                                                    })
        else:
            return redirect('pengobatan:beranda', tipe=request.user.tipe)
    else:
        return redirect('welcome')

# Halaman untuk menampilkan kondisi antrian pasien dan log dari pasien
def antrian_pasien(request, tipe):
    waktu = datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")

    if request.user.is_authenticated:
        akun = load_akun_by_tipe(request.user, tipe)
        if akun is None:
            return redirect('welcome')

        if request.user.tipe == 'petugas' and tipe == 'petugas':
            awal, akhir = waktu_hari_ini()
            antrian_pasien = PengobatanInfo.objects.filter(sudah_verifikasi=True, sudah_ditangani=False, tanggal_berkunjung__gte=awal, tanggal_berkunjung__lte=akhir).order_by('-tanggal_berkunjung')
            log_antrian = PengobatanInfo.objects.all().order_by('-tanggal_berkunjung')
            return render(request, 'petugas/antrian_pasien.html', context={
                                                                    'antrian_pasien':antrian_pasien,
                                                                    'log_antrian': log_antrian,
                                                                    'waktu': waktu,
                                                                    'user': akun,
                                                                })
        else:
            return redirect('pengobatan:beranda', tipe=request.user.tipe)
    else:
        return redirect('welcome')

# Halaman untuk menampilkan daftar poli dan pilihan untuk melihat detailnya
def poli(request, tipe):
    waktu = datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")

    if request.user.is_authenticated:
        akun = load_akun_by_tipe(request.user, tipe)
        if akun is None:
            return redirect('welcome')

        if request.user.tipe == 'petugas' and tipe == 'petugas':
            poli_info = PoliInfo.objects.all()
            return render(request, 'petugas/poli.html', context={
                                                            'poli': poli_info,
                                                            'waktu': waktu,
                                                            'user': akun,
                                                        })
        else:
            return redirect('pengobatan:beranda', tipe=request.user.tipe)
    else:
        return redirect('welcome')

def tambah_poli(request, tipe):
    waktu = datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")

    if request.user.is_authenticated:
        akun = load_akun_by_tipe(request.user, tipe)
        dokter = DokterInfo.objects.all()
        if request.method == "POST":
            poli_form = PoliForm(data=request.POST)
            if poli_form.is_valid():
                poli_form.save()
                return redirect('pengobatan:poli', tipe=tipe)
            else:
                messages.info(request, "Perubahan gagal dilakukan")
                return redirect("pengobatan:poli", tipe=tipe, )
        else:
            poli_form = PoliForm()
        return render(request, 'petugas/tambah_poli.html', context={
                                                            'user': akun,
                                                            'poli_form': poli_form,
                                                            'dokter': dokter
                                                            })
    else:
        return redirect('welcome')

def ubah_poli(request, tipe, nama_poli):
    waktu = datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")

    if request.user.is_authenticated:
        akun = load_akun_by_tipe(request.user, tipe)
        poli_data = PoliInfo.objects.get(pk=nama_poli)
        dokter = DokterInfo.objects.all()
        poli = PoliInfo.objects.all()
        if request.method == "POST":
            poli_form = PoliForm(data=request.POST, instance=poli_data)
            if poli_form.is_valid():
                poli_form.save()
                return redirect('pengobatan:poli', tipe=tipe)
            else:
                messages.info(request, "Perubahan gagal dilakukan")
                return redirect("pengobatan:poli", tipe=tipe )
        else:
            poli_form = PoliForm()
        return render(request, 'petugas/ubah_poli.html', context={
                                                            'user': akun,
                                                            'poli_form': poli_form,
                                                            'dokter': dokter,
                                                            'poli': poli
                                                            })
    else:
        return redirect('welcome')

# Halaman untuk melihat detail jadwal dan mengubah jadwal terkait
def tambah_jadwal(request, tipe, nama_poli):
    waktu = datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")

    if request.user.is_authenticated:
        akun = load_akun_by_tipe(request.user, tipe)
        polis = PoliInfo.objects.all()
        dokters = DokterInfo.objects.all()
        if request.method == "POST":
            jadwal_form = JadwalForm(data=request.POST)
            if jadwal_form.is_valid():
                jadwal_form.save()
                return redirect('pengobatan:poli', tipe=tipe)
            else:
                messages.info(request, "Perubahan gagal dilakukan")
                return redirect("pengobatan:poli", tipe=tipe)
        else:
            jadwal_form = JadwalForm()
        return render(request, 'petugas/tambah_jadwal.html', context={
                                                            'user': akun,
                                                            'jadwal_form': jadwal_form,
                                                            'polis': polis,
                                                            'dokters': dokters
                                                            })
    else:
        return redirect('welcome')

def ubah_jadwal(request, tipe, nama_poli, jadwal):
    waktu = datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")

    if request.user.is_authenticated:
        akun = load_akun_by_tipe(request.user, tipe)
        polis = PoliInfo.objects.all()
        dokters = DokterInfo.objects.all()
        jadwal_data = JadwalPraktekInfo.objects.get(pk=jadwal)
        if request.method == "POST":
            jadwal_form = JadwalForm(data=request.POST, instance=jadwal_data)
            if jadwal_form.is_valid():
                jadwal_data = jadwal_form.save()
                return redirect('pengobatan:poli', tipe=tipe)
            else:
                messages.info(request, "Perubahan gagal dilakukan")
                return redirect("pengobatan:poli", tipe=tipe)
        else:
            jadwal_form = JadwalForm(instance=jadwal_data)
        return render(request, 'petugas/ubah_jadwal.html', context={
                                                            'user': akun,
                                                            'jadwal_form': jadwal_form,
                                                            'polis': polis,
                                                            'jadwal': jadwal_data,
                                                            'dokters': dokters
                                                            })
    else:
        return redirect('welcome')

# def ubah_jadwal(request, tipe, nama_poli, jadwal):
#     waktu = datetime.now()
#     waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")

#     if request.user.is_authenticated:
#         akun = load_akun_by_tipe(request.user, tipe)
#         berubah = False
#         jadwal_data = JadwalPraktekInfo.objects.get(pk=jadwal)
#         dokter = DokterInfo.objects.all()
#         poli = PoliInfo.objects.all()
#         if request.method == "POST":
#             jadwal_form = JadwalForm(data=request.POST, instance=jadwal_data)
#             if jadwal_form.is_valid():
#                 jadwal_data = jadwal_form.save()
#                 berubah = True
#                 return redirect('pengobatan:poli', tipe=tipe)
#             else:
#                 messages.info(request, "Perubahan gagal dilakukan")
#                 return redirect("pengobatan:jadwal", tipe=tipe, nama_poli=nama_poli, jadwal=jadwal_data.id )
#         else:
#             jadwal_form = JadwalForm(instance=jadwal_data)
#         return render(request, 'petugas/ubah_jadwal.html', context={
#                                                             'berubah': berubah,
#                                                             'jadwal_form': jadwal_form,
#                                                             'user': akun,
#                                                             'dokter': dokter,
#                                                             'poli': poli
#                                                             })
#     else:
#         return redirect('welcome')

# Halaman untuk menampilkan petunjuk dan merubah petunjuk
def petunjuk(request, tipe):
    waktu = datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")

    if request.user.is_authenticated:
        akun = load_akun_by_tipe(request.user, tipe)
        if akun is None:
            return redirect('welcome')

        if request.user.tipe == 'petugas' and tipe == 'petugas':
            guides = Guideline.objects.all()
            return render(request, 'petugas/petunjuk.html', context={
                                                            'guides' : guides,
                                                            'waktu': waktu,
                                                            'user': akun
                                                            })
        else:
            return redirect('pengobatan:beranda', tipe=request.user.tipe)
    else:
        return redirect('welcome')

# Halaman untuk mengubah isi petunjuk
def ubah_petunjuk(request, id, tipe):
    waktu = datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")

    if request.user.is_authenticated:
        akun = load_akun_by_tipe(request.user, tipe)
        if akun is None:
            return redirect('welcome')

        if request.user.tipe == 'petugas' and tipe == 'petugas':
            berubah = False
            guide = get_object_or_404(Guideline, pk=id)
            petunjuk_form = GuidelineForm(instance=guide)
            if request.method == "POST":
                petunjuk_form = GuidelineForm(request.POST, request.FILES, instance=guide)
                if petunjuk_form.is_valid():
                    petunjuk_form.save()
                    return redirect('pengobatan:petunjuk', tipe=request.user.tipe)

                berubah = True
            else:
                petunjuk_form = GuidelineForm()

            return render(request, 'petugas/ubah_petunjuk.html', context={
                                                            'petunjuk_form': petunjuk_form,
                                                            'guides': guide,
                                                            'waktu': waktu,
                                                            'user': akun,
                                                        })
        else:
            return redirect('pengobatan:beranda', tipe=request.user.tipe)
    else:
        return redirect('welcome')

def log_obat(request, tipe):
    waktu = datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")

    if request.user.is_authenticated:
        akun = load_akun_by_tipe(request.user, tipe)
        if akun is None:
            return redirect('welcome')

        if request.user.tipe == 'dokter' and tipe == 'dokter':
            awal, akhir = waktu_hari_ini()
            pasien_berobat = PengobatanInfo.objects.filter(dokter=akun, sudah_berobat=True)
            return render(request, 'dokter/log_pemberian_obat.html', context={
                                                                    'pasien_berobat': pasien_berobat,
                                                                    'waktu': waktu,
                                                                    'user': akun,
                                                                })
        if request.user.tipe == 'apoteker' and tipe == 'apoteker':
            awal, akhir = waktu_hari_ini()
            pasien_berobat = PengobatanInfo.objects.filter(apoteker=akun, sudah_berobat=True)
            return render(request, 'apoteker/log_obat_keluar.html', context={
                                                                    'pasien_berobat': pasien_berobat,
                                                                    'waktu': waktu,
                                                                    'user': akun,
                                                                })
        else:
            return redirect('pengobatan:beranda', tipe=request.user.tipe)
    else:
        return redirect('welcome')

def resep_obat(request, tipe, antrian):
    waktu = datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")
    if request.user.is_authenticated:
        akun = load_akun_by_tipe(request.user, tipe)
        berkas = PengobatanInfo.objects.get(id=antrian)
        if request.method == "POST":
            obat_form = PengobatanForm(data=request.POST, instance=berkas)
            if obat_form.is_valid():
                berkas = obat_form.save()
                return redirect("pengobatan:detail_pengobatan", tipe=tipe, antrian=antrian)
            else:
                return redirect("pengobatan:resep_obat", tipe=tipe, antrian=antrian)
        else:
            obat_form = PengobatanForm()
        return render(request, 'dokter/resep_obat.html', context={
                                                            'berkas': berkas,
                                                            'user': akun,
                                                            'obat_form': obat_form,
                                                            })
    else:
        return redirect('welcome')
