from django import forms

from pengobatan.models import JadwalPraktekInfo
from guidelines.models import Guideline

class VerifikasiForm(forms.Form):
    verifikasi = forms.CharField()
    tolak      = forms.CharField()

class JadwalForm(forms.ModelForm):
    class Meta():
        model = JadwalPraktekInfo
        fields = '__all__'

class PetunjukForm(forms.ModelForm):
    class Meta():
        model = Guideline
        fields = '__all__'
