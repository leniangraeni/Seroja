from django import forms
from accounts.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 
                    'nomor_pegawai', 'avatar', 'surat_tugas')