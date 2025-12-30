from rest_framework import serializers
from .models import *
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class UserSerializer(serializers.ModelSerializer):
    nombre_rol = serializers.CharField(source='rol.nombre', read_only=True)
    class Meta:
        model = Usuario
        fields = ['id','email','username','first_name','last_name','rol','nombre_rol']

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id','nombre','descripcion']

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
        fields = ['email','password','username']

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

class ColaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cola
        fields = ['id','nombre','codigo_cola','descripcion']

class TicketCreateSerializer(serializers.ModelSerializer):
    codigo = serializers.CharField(read_only = True)
    fecha_creacion = serializers.DateTimeField(read_only = True)
    class Meta:
        model = Ticket
        fields = ['cola','prioridad','nombre_cliente','codigo','fecha_creacion']

    # Esta función se ejecuta cuando haces .save().
    # validated_data trae: { 'cola': <ObjetoCola>, 'prioridad': 'NORMAL' }
    def create(self, validated_data):
        #sacamos la cola q elijio el usuario
        cola_seleccionada = validated_data['cola']
        #filta y cuenta de solo tickets de esa cola
        cantidad_existente = Ticket.objects.filter(cola=cola_seleccionada).count()
        #se opera para obtener el orden del ticket creado
        nuevo_numero = cantidad_existente +1
        #se genera el "codigo de la cola"
        codigo_generado = f"{cola_seleccionada.codigo_cola}-{nuevo_numero:03d}"
        validated_data['codigo'] = codigo_generado
        return super().create(validated_data)
    
class TicketReadSerializer(serializers.ModelSerializer):
    nombre_cola = serializers.CharField(source='cola.nombre', read_only = True) #read_only => solo lee, no modifica
    #codigo_cola = serializers.CharField(source='cola.codigo_cola', read_only = True )
    tiempo_espera= serializers.SerializerMethodField() # SerializerMethodField dice que se va a calcular (campos q no esten en la BD)
    class Meta:
        model = Ticket
        fields = ['id','codigo','nombre_cola','nombre_cliente','prioridad','estado','tiempo_espera','fecha_fin']
    def get_tiempo_espera(self, obj):
        #si el ticket termino, tiene fecha_fin, si no tiene se usa la hora actual(timezone.now())
        fin = obj.fecha_fin if obj.fecha_fin else timezone.now()
        #resta fechas
        delta = fin - obj.fecha_creacion
        return f"{int(delta.total_seconds() // 60)} min"
    

class AsignacionTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields =['id','estado','escritorio_asignado']
    def validate(self, data):
        if self.instance.estado != Ticket.Estados.PENDIENTE:
            raise serializers.ValidationError('Este ticket ya esta siendo atendido o finalizo')
        return data
    def update(self, instance, validated_data):
        instance.estado = Ticket.Estados.LLAMANDO
        instance.fecha_llamada = timezone.now()
        instance.save()
        return instance
    


class EscritorioWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escritorio
        fields = '__all__'

class EscritorioReadSerializer(serializers.ModelSerializer):
    colas_info = ColaSerializer(source='colas_que_atiende',many=True, read_only = True)
    usuario = UserSerializer(read_only=True) #obtener todos los datos en json "POSTMAN"
    colas_que_atiende = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Cola.objects.all()
    )
    #cola = ColaSerializer(read_only=True)
    class Meta:
        model = Escritorio
        fields = ['id','usuario','numero_ventanilla','colas_que_atiende','colas_info']
