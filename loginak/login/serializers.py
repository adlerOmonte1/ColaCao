from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id','email','username','first_name','last_name','rol']

# POR INVESTIGAR
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token =  super().get_token(user)
        if user.rol:
            token['rol'] = user.rol.nombre
        else:
            token['rol']='invitado'
        token['username'] = user.username
        return token
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.rol:
            data['rol']=self.user.rol.nombre
        else:
            data['rol'] ='invitado'
        data['nombre'] = self.user.first_name
        data['user_id']= self.user.id
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Usuario
        fields = ['email','password','username','first_name']

    def create(self, validated_data):

        user = Usuario.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username= validated_data.get('username',''),
            first_name = validated_data.get('first_name','')
        )
        return user