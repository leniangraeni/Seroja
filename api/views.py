from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from accounts.models import PasienInfo
from guidelines.models import Guideline
from api.serializers import GuidelineSerializer, UserSerializer, PasienSerializer

# Create your views here.
@api_view(['GET'])
def guideline_view(request):
    if request.method == 'GET':
        guide = Guideline.objects.all()
        guide_serializer = GuidelineSerializer(guide, many=True)
        return JsonResponse(guide_serializer.data, safe=False)

@api_view(['GET'])
def pasien_view(request):
    permission_classes = (IsAuthenticated, )
    if request.method == 'GET':
        pasien = PasienInfo.objects.all()
        pasien_serializer = PasienSerializer(pasien, many=True)
        return JsonResponse(pasien_serializer.data, safe=False)

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        pasien_serializer = PasienSerializer(data=request.data)
        if user_serializer.is_valid() and pasien_serializer.is_valid():
            user = user_serializer.save(tipe=1)
            pasien = pasien_serializer.save(user=user)

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        print(user_serializer.errors)
        return Response(user_serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def status_pendaftaran(request):
    if request.method == "GET":
        pasien = PasienInfo.objects.get(user=request.user)
        status = {
            'verifikasi': pasien.sudah_verifikasi,
            'ditangani' : pasien.sudah_ditangani,
            'berobat'   : pasien.sudah_berobat,
            'ditolak'   : pasien.ditolak,
            }
        return JsonResponse(status, safe=False)
