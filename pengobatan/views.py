from django.shortcuts import render

# Memasukan model dan form
from pengobatan.models import PoliInfo, JadwalPraktekInfo, ObatInfo, PengobatanInfo
from pengobatan.forms import VerifikasiForm

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
    if tipe == 'petugas':
        akun_data = PetugasInfo.objects.get(user=user)
    elif tipe == 'dokter':
        akun_data = DokterInfo.objects.get(user=user)
    elif tipe == 'apoteker':
        akun_data = ApotekerInfo.objects.get(user=user)
    return akun_data

# Create your views here.
# Halaman beranda untuk pengguna yang sudah login
def beranda(request, tipe):
    waktu = datetime.datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")
    awal, akhir = waktu_hari_ini()

    if request.user.is_authenticated:
        akun = load_akun_by_tipe(request.user, tipe)
        if akun is None:
            return redirect('welcome')
        if request.user.tipe == 'petugas' and tipe == 'petugas':
            berkas = PengobatanInfo.objects.filter(sudah_verifikasi=False, ditolak=False, tanggal_berkunjung__gte=awal, tanggal_berkunjung__lte=akhir).order_by(tanggal_berkunjung)
            return render(request, 'petugas/beranda.html', context={
                                                                'waktu': waktu,
                                                                'user': akun,
                                                                'berkas': berkas,
                                                            })
        if request.user.tipe == 'dokter' and tipe == 'petugas':
            antrian_pasien = PengobatanInfo.objects.filter(dokter=akun, sudah_verifikasi=True, ditolak=False, tanggal_berkunjung__gte=awal, tanggal_berkunjung__lte=akhir).order_by(tanggal_berkunjung)
            antrian_apotek = PengobatanInfo.objects.filter(dokter=akun, sudah_ditangani=True)
            return render(request, 'dokter/beranda.html', context={
                                                            'waktu': waktu,
                                                            'user': akun,
                                                            'antrian_pasien': antrian_pasien,
                                                            'antrian_apotek': antrian_apotek,
                                                        })
        if user.tipe == 'apoteker' and tipe == 'petugas':
            antrian_obat_masuk = PengobatanInfo.objects.filter(sudah_ditangani=True, sudah_berobat=False, ditolak=False, tanggal_berkunjung__gte=awal, tanggal_berkunjung__lte=akhir).order_by(tanggal_berkunjung)
            log_obat_keluar = PengobatanInfo.objects.filter(sudah_berobat=True)
            return render(request, 'apoteker/beranda.html', context={
                                                            'waktu': waktu,
                                                            'user': akun,
                                                            'antrian_obat_masuk': antrian_obat_masuk,
                                                            'log_obat_keluar': log_obat_keluar,
                                                            })
    else:
        return redirect('welcome')

# Halaman detail pengobatan, berisi pilihan validasi atau tolak berkas
def detail_pengobatan(request, tipe, antrian):
    waktu = datetime.datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")

    if request.user.is_authenticated:
        akun = load_akun_by_tipe(request.user, request.user.tipe)
        if akun is None:
            return redirect('welcome')

        if request.user.tipe == 'petugas' and tipe == 'petugas':
            berkas = PengobatanInfo.objects.get(id=antrian)
            check = False
            verifikasi = False
            tolak = False

            if request.method == "POST":
                verifikasi_form = VerifikasiForm(data=request.POST)

                if verifikasi_form.is_valid():
                    if verifikasi_form.cleaned_data['verifikasi']:
                        berkas['sudah_verifikasi'] = True
                        verifikasi = True
                    if verifikasi_form.cleaned_data['tolak']:
                        berkas['ditolak'] = True
                        tolak = True
                    berkas.save()
                    check = True
                else:
                    return HttpResponse("Ada kesalahan")
            else:
                verifikasi_form = VerifikasiForm()

            status = (verifikasi or tolak)
            return render(request, 'petugas/detail_pengobatan.html', context={
                                                                        'check': check,
                                                                        'berkas': berkas,
                                                                        'verifikasi': verifikasi,
                                                                        'tolak': tolak,
                                                                        'verifikasi_form': verifikasi_form,
                                                                    })
        else:
            return redirect('pengobatan:beranda', tipe=request.user.tipe)
    else:
        return redirect('welcome')

# Halaman untuk menampilkan kondisi antrian pasien dan log dari pasien
def antrian_pasien(request, tipe):
    waktu = datetime.datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")

    if request.user.is_authenticated:
        akun = load_akun_by_tipe(request.user, request.user.tipe)
        if akun is None:
            return redirect('welcome')

        if request.user.tipe == 'petugas' and tipe == 'petugas':
            awal, akhir = waktu_hari_ini()
            antrian_pasien = PengobatanInfo.objects.filter(sudah_verifikasi=True, tanggal_berkunjung__gte=awal, tanggal_berkunjung__lte=akhir)
            log_antrian = PengobatanInfo.objects.all().order_by(tanggal_berkunjung)
            return render(request, 'petugas/antrian_pasien.html', context={
                                                                    'antrian_pasien':antrian_pasien,
                                                                    'log_antrian': log_antrian,
                                                                    'waktu': waktu,
                                                                    'user': akun,
                                                                })
        else:
            return redirect('pengobatan:beranda', tipe=request.user.tip)
    else:
        return redirect('welcome')

# Halaman untuk menampilkan daftar poli dan pilihan untuk melihat detailnya
def poli(request, tipe):
    waktu = datetime.datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")

    if request.user.is_authenticated:
        akun = load_akun_by_tipe(user, user.tipe)
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

# Halaman untuk melihat jadwal dari poli
def jadwal_poli(request, tipe, nama_poli):
    waktu = datetime.datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")

    if request.user.is_authenticated:
        akun = load_akun_by_tipe(request.user, request.user.tipe)
        if akun is None:
            return redirect('welcome')

        if request.user.tipe == 'petugas' and tipe == 'petugas':
            jadwal = JadwalPraktekInfo.objects.filter(poli__name=nama_poli)
            return render(request, 'petugas/jadwal_poli.html', context={
                                                                'jadwal': jadwal,
                                                                'waktu': waktu,
                                                                'user': akun,
                                                            })
        else:
            return redirect('pengobatan:beranda', tipe=request.user.tipe)
    else:
        return redirect('welcome')

# Halaman untuk melihat detail jadwal dan mengubah jadwal terkait
def ubah_jadwal(request, tipe, nama_poli, jadwal):
    waktu = datetime.datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")

    if request.user.is_authenticated:
        akun = load_akun_by_tipe(request.user, request.user.tipe)
        if akun is None:
            return redirect('welcome')

        if request.user.tipe == 'petugas' and tipe == 'petugas':
            berubah = False
            if request.method == "POST":
                jadwal_form = JadwalForm(data=request.POST)
                jadwal = jadwal_form.save()

                berubah = True
            else:
                jadwal_form = JadwalForm()
                jadwal = JadwalForm.objects.get(pk=jadwal)

            return render(request, 'petugas/ubah_jadwal', context={
                                                            'jadwal_form': jadwal_form,
                                                            'jadwal': jadwal,
                                                            'waktu': waktu,
                                                            'user': akun,
                                                        })
        else:
            return redirect('pengobatan:beranda', tipe=request.user.tipe)
    else:
        return redirect('welcome')

# Halaman untuk menampilkan petunjuk dan merubah petunjuk
def petunjuk(request, tipe):
    waktu = datetime.datetime.now()
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

def log_obat(request):
    waktu = datetime.datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")
    user = request.user
    if user.is_authenticated:
        akun = load_akun_by_tipe(user, user.tipe)
        if user.tipe == 'dokter':
            return render(request, 'dokter/log_pemberian_obat.html', {'waktu': waktu, 'user': akun})
        if user.tipe == 'apoteker':
            return render(request, 'apoteker/log_obat_keluar.html', {'waktu': waktu, 'user': akun})

def profil(request):
    waktu = datetime.datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")
    user = request.user
    if user.is_authenticated:
        akun = load_akun_by_tipe(user, user.tipe)
        if user.tipe == 'petugas':
            return render(request, 'petugas/profil.html', {'waktu': waktu, 'user': akun})
        if user.tipe == 'dokter':
            return render(request, 'dokter/profil.html', {'waktu': waktu, 'user': akun})
        if user.tipe == 'apoteker':
            return render(request, 'apoteker/profil.html', {'waktu': waktu, 'user': akun})

def pengaturan(request):
    waktu = datetime.datetime.now()
    waktu = waktu.strftime("%A, %d-%m-%Y %H:%M")
    user = request.user
    if user.is_authenticated:
        akun = load_akun_by_tipe(user, user.tipe)
        if user.tipe == 'petugas':
            return render(request, 'petugas/pengaturan.html', {'waktu': waktu, 'user': akun})
        if user.tipe == 'dokter':
            return render(request, 'dokter/pengaturan.html', {'waktu': waktu, 'user': akun})
        if user.tipe == 'apoteker':
            return render(request, 'apoteker/pengaturan.html', {'waktu': waktu, 'user': akun})
