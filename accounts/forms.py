from django import forms
from django.contrib.auth.models import User
from accounts.models import PetugasInfo, DokterInfo, ApotekerInfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta():
        model = User
        fields = (
            'username', 'password',
        )

class PetugasForm(forms.ModelForm):
    nomor_telepon = forms.CharField(widget=forms.TextInput(attrs={'type':'number'}))
    nomor_pegawai = forms.CharField(widget=forms.TextInput(attrs={'type':'number'}))

    class Meta():
        model = PetugasInfo
        fields = (
            'nama', 'tempat_lahir', 'tanggal_lahir', 'jenis_kelamin', 'nomor_telepon', 'alamat', 'nomor_pegawai', 'surat_tugas', 'profil',
        )

class DokterForm(forms.ModelForm):
    nomor_telepon = forms.CharField(widget=forms.TextInput(attrs={'type':'number'}))
    nomor_pegawai = forms.CharField(widget=forms.TextInput(attrs={'type':'number'}))

    class Meta():
        model = DokterInfo
        fields = (
            'nama', 'tempat_lahir', 'tanggal_lahir', 'jenis_kelamin', 'nomor_telepon', 'alamat', 'nomor_pegawai', 'surat_tugas', 'profil',
        )

class ApotekerForm(forms.ModelForm):
    nomor_telepon = forms.CharField(widget=forms.TextInput(attrs={'type':'number'}))
    nomor_pegawai = forms.CharField(widget=forms.TextInput(attrs={'type':'number'}))

    class Meta():
        model = ApotekerInfo
        fields = (
            'nama', 'tempat_lahir', 'tanggal_lahir', 'jenis_kelamin', 'nomor_telepon', 'alamat', 'nomor_pegawai', 'surat_tugas', 'profil',
        )
