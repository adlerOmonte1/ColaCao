from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class UserSerializer(serializers.ModelSerializer):
    nombre_rol = serializers.CharField(source='rol.nombre', read_only=True)
    class Meta:
        model = Usuario
        fields = ['id','email','username','first_name','last_name','rol','nombre_rol']

# Funcion de SimpleJWT, el proceso de Login (verificacion)
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    #Obtiene los datos del usuario e encripta toda la info
    def get_token(cls, user):
        token =  super().get_token(user)
        if user.rol:
            token['rol'] = user.rol.nombre
        else:
            token['rol']='invitado'
        token['username'] = user.username
        return token
    #El simpleJWT entrega refresh y access, pero se agrega rol,nombre,user
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.rol:
            data['rol']=self.user.rol.nombre
        else:
            data['rol'] ='invitado'
        data['nombre'] = self.user.username
        data['user_id']= self.user.id
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Usuario
        fields = ['email','password','username','first_name']

    def create(self, validated_data):
        username_final = validated_data.get('username')
        if not username_final:
            username_final = validated_data['email']

        user = Usuario.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username= username_final,
            first_name = validated_data.get('first_name',''),
            last_name = validated_data.get('last_name','')
        )
        try:
            rol_cliente = Rol.objects.get(nombre='cliente')
            user.rol = rol_cliente
            user.save()
        except Rol.DoesNotExist:
            pass
        return user