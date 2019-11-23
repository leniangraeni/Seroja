from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms
from accounts.models import SerojaUser, PetugasInfo, DokterInfo, ApotekerInfo

class SerojaUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    tipe     = forms.CharField(widget=forms.HiddenInput)

    class Meta():
        model = SerojaUser
        fields = (
            'username', 'password', 'tipe',
        )


class AkunRegistrationForm(forms.Form):
    # Pilihan Masukan
    JK_CHOICES = (
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )

    # Informasi Datadiri
    nama          = forms.CharField(max_length=20)
    tempat_lahir  = forms.CharField(max_length=20)
    tanggal_lahir = forms.DateField()
    jenis_kelamin = forms.ChoiceField(choices=JK_CHOICES)
    nomor_telepon = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'type':'number'}))
    alamat        = forms.CharField(widget=forms.Textarea())
