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

class AkunRegistrationForm(forms.Form):
    # Pilihan Masukan
    JK_CHOICES = (
        (0, 'laki-laki'),
        (1, 'perempuan'),
    )

    # Informasi Datadiri
    nama          = forms.CharField(max_length=20)
    tempat_lahir  = forms.CharField(max_length=20)
    tanggal_lahir = forms.DateField()
    jenis_kelamin = forms.ChoiceField(choices=JK_CHOICES)
    nomor_telepon = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'type':'number'}))
    alamat        = forms.CharField(widget=forms.Textarea())
    tipe          = forms.IntegerField()
