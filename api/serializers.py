# Fungsi untuk parsing data API
from rest_framework import serializers

# Memasukan model yang akan digunakan
from guidelines.models import Guideline
from accounts.models import SerojaUser, PasienInfo

class GuidelineSerializer(serializers.ModelSerializer):
    class Meta():
        model = Guideline
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = SerojaUser
        fields = ['username', 'password']

class PasienSerializer(serializers.ModelSerializer):
    class Meta():
        model = PasienInfo
        fields = [
            'nama', 'tempat_lahir', 'tanggal_lahir', 'jenis_kelamin',
            'nomor_telepon', 'alamat', 'nomor_bpjs',
            'rekam_medik',
        ]
