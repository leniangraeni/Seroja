from django import forms

from pengobatan.models import JadwalPraktekInfo, PengobatanInfo, PoliInfo
from guidelines.models import Guideline

class UbahProfilForm(forms.Form):
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

class VerifikasiForm(forms.Form):
    verifikasi = forms.CharField()

class BerobatForm(forms.Form):
    berobat = forms.CharField()

class SelesaiForm(forms.Form):
    selesai = forms.CharField()

class PoliForm(forms.ModelForm):
    class Meta():
        model = PoliInfo
        fields = '__all__'

class JadwalForm(forms.ModelForm):
    class Meta():
        model = JadwalPraktekInfo
        fields = '__all__'

class PetunjukForm(forms.ModelForm):
    class Meta():
        model = Guideline
        fields = '__all__'

class PengobatanForm(forms.ModelForm):
    class Meta():
        model = PengobatanInfo
        fields = ['obat', 'dosis', 'aturan', 'catatan']

class PenolakanForm(forms.ModelForm):
    class Meta():
        model = PengobatanInfo
        fields = ['pesan_penolakan']

