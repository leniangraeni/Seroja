# Fungis serializer untuk transformasi data
from rest_framework import serializers

# Memasukan model
from guidelines.models import Guideline
from accounts.models import SerojaUser, PasienInfo
from pengobatan.models import JadwalPraktekInfo, PengobatanInfo

# Serializers
class GuidelineSerializer(serializers.ModelSerializer):
    class Meta():
        model = Guideline
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = SerojaUser
        fields = ('username', 'password', 'tipe')

class PasienSerializer(serializers.ModelSerializer):
    class Meta():
        model = PasienInfo
        fields = ('nama', 'nomor_bpjs', 'bpjs', 'rekam_medik', 'profil')

class JadwalSerializer(serializers.ModelSerializer):
    class Meta():
        model = JadwalPraktekInfo
        fields = '__all__'

class PengobatanSerializer(serializers.ModelSerializer):
    class Meta():
        model = PengobatanInfo
        fields = ('pasien', 'jadwal', 'keluhan', 'rujukan')

class IdSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=10)

class PengobatanFullSerializer(serializers.ModelSerializer):
    class Meta():
        model = PengobatanInfo
        fields = '__all__'
