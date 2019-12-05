# Fungsi autentikasi Django
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

# Fungsi untuk API Management
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.views import APIView

# Memasukan model dan serialiazer
from guidelines.models import Guideline
from pengobatan.models import JadwalPraktekInfo, PengobatanInfo, PasienInfo
from api.serializers import GuidelineSerializer, UserSerializer, PasienSerializer, JadwalSerializer, PengobatanSerializer, IdSerializer, PengobatanFullSerializer

from datetime import datetime, timedelta, time

def waktu_hari_ini():
    mulai = datetime.now().date()
    akhir = mulai + timedelta(1)
    waktu_mulai = datetime.combine(mulai, time())
    waktu_akhir = datetime.combine(akhir, time())
    return waktu_mulai, waktu_akhir

# Create your views here.
# API ROOT
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'guideline' : reverse('guideline_response', request=request, format=format),
    })

# API untuk menampilkan Guideline
@api_view(['GET'])
def guideline_response(request):
    if request.method == 'GET':
        guideline = Guideline.objects.latest('id')
        serializer = GuidelineSerializer(guideline)
        return Response(serializer.data)

# API untuk mendaftarkan diri
@api_view(['POST'])
def pasien_register(request):
    if request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        pasien_serializer = PasienSerializer(data=request.data)
        if user_serializer.is_valid() and pasien_serializer.is_valid():
            user_data = user_serializer.save()
            user_data.set_password(user_data.password)
            user_data.save()

            pasien_data = pasien_serializer.save()
            pasien_data.user = user_data
            pasien_data.save()

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            if not user_serializer.is_valid():
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(pasien_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API untuk login
@csrf_exempt
@api_view(['POST'])
def pasien_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response(
                        {'error':'Username dan Password harus diisi'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
    else:
        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                            {'error':'Username atau Password salah'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
        else:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                            {'token':token.key},
                            status=status.HTTP_200_OK
                        )

@api_view(['GET','POST'])
@permission_classes((IsAuthenticated,))
def daftar_pengobatan(request):
    if request.method == "GET":
        jadwal = JadwalPraktekInfo.objects.all()
        jadwal_serializer = JadwalSerializer(jadwal, many=True)
        return Response(jadwal_serializer.data)
    elif request.method == "POST":
        pengobatan_serializer = PengobatanSerializer(data=request.data)
        if pengobatan_serializer.is_valid():
            pengobatan_data = pengobatan_serializer.save()
            pengobatan_data.dokter = pengobatan_serializer.validated_data['jadwal'].dokter
            pengobatan_data.save()

            return Response(pengobatan_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(pengobatan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def status_pasien(request):
    awal, akhir = waktu_hari_ini()
    if request.method == "POST":
        id_serializer = IdSerializer(data=request.data)
        if id_serializer.is_valid():
            pengobatan = PengobatanInfo.objects.get(id=id)
            serialize_pengobatan = PengobatanFullSerializer(pengobatan)
            return Response(serialize_pengobatan.data, status=status.HTTP_200_OK)
        else:
            return Response(id_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
