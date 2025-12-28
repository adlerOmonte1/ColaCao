from rest_framework import generics
from  rest_framework.permissions import AllowAny
from .models import *
from . serializers import *
from rest_framework import viewsets,status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer

from .permissions import *
from django.db import transaction # <--- Importante para la "Race Condition"
from django.shortcuts import get_object_or_404,render
from rest_framework.response import Response
from rest_framework.decorators import action
# Create your views here.

class RegisterView(generics.CreateAPIView): 
    #createApiView es un proceso de POST ya definido, como recibir-validar-guardar
    queryset = Usuario.objects.all()
    permission_classes = [AllowAny] #cualquiera puede registrarse
    serializer_class = RegisterSerializer 

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UsuarioViewset(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer

class RolesViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class ColaViewSet(viewsets.ModelViewSet):
    queryset = Cola.objects.all()
    serializer_class = ColaSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    def get_serializer_class(self):
        if self.action == 'create':
            return TicketCreateSerializer
        return TicketReadSerializer
    
    #DECORADOR se usa cuando la vista es una funcion extra(no un CRUD)
    #Detail = False, es asi porq no se necesita un ID espec. para llamar
    #Se crea una URL (/llamar_siguiente/)
    @action(detail=False, methods=['post'])
    def llamar_siguiente(self, request):
        #identifica al cajero logueado (django mismo, no angular)
        usuario_actual = request.user
        try:
            escritorio = Escritorio.objects.get(usuario=usuario_actual)
        except Escritorio.DoesNotExist:
            return Response(
                {"error":"No tienes un escritorio asignado"},
                status=status.HTTP_400_BAD_REQUEST
            )
        colas_que_atiende = escritorio.colas_que_atiende.all()
        
        with transaction.atomic():
            candidato = Ticket.objects.select_for_update().filter(
                #filtro de q sea mi "COLA" y este pendiente
                cola__in = colas_que_atiende,
                estado = Ticket.Estados.PENDIENTE
            ).order_by(
                #ordena por prioridad y luego llegada
                'prioridad',
                'fecha_creacion'
            ).first() # toma al primero

            #si no hay nadie esperando
            if not candidato:
                return Response(
                    {"mensaje":"No hay tickets pendientes en tus colas"}
                )
            
            candidato.escritorio_asignado = escritorio
            candidato.estado = Ticket.Estados.LLAMANDO
            candidato.save()
            serializers = TicketReadSerializer(candidato)

            return Response(serializers.data, status=status.HTTP_200_OK)

class EscritorioViewSet(viewsets.ModelViewSet):
    queryset = Escritorio.objects.all()
    serializer_class = EscritorioSerializer
    permission_classes = [EsRolAdministrador]