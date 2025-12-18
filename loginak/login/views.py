from django.shortcuts import render
from rest_framework import generics
from  rest_framework.permissions import AllowAny
from .models import Usuario
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer
# Create your views here.

class RegisterView(generics.CreateAPIView): 
    #createApiView es un proceso de POST ya definido, como recibir-validar-guardar
    queryset = Usuario.objects.all()
    permission_classes = [AllowAny] #cualquiera puede registrarse
    serializer_class = RegisterSerializer 

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
