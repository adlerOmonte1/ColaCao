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

from django.db.models import Case, When, Value, IntegerField # <--- Importar esto
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
        ticket_en_curso = Ticket.objects.filter(
            escritorio_asignado=escritorio,
            estado__in=[Ticket.Estados.LLAMANDO, Ticket.Estados.ATENCION]
        ).first()
        if ticket_en_curso:
            return Response(
                {"error":"No puedes llamar a otro, tienes un ticket pendiente",
                    "ticket_pendiente":{
                        "id":ticket_en_curso.id,
                        "codigo":ticket_en_curso.codigo,
                        "estado":ticket_en_curso.estado
                    }
                }, status= status.HTTP_400_BAD_REQUEST
            )

        colas_que_atiende = escritorio.colas_que_atiende.all()
        
        with transaction.atomic():
            candidato = Ticket.objects.select_for_update().filter(
                #filtro de q sea mi "COLA" y este pendiente
                cola__in = colas_que_atiende,
                estado = Ticket.Estados.PENDIENTE
            ).annotate(
                # Aquí creamos una columna virtual "ranking_prioridad"
                # VIP = 1 (El más importante)
                # PREFERENCIAL = 2
                # NORMAL = 3
                ranking_prioridad=
                Case(
                    When(prioridad =Ticket.Prioridades.VIP, then= Value(1)),
                    When(prioridad=Ticket.Prioridades.PREFERENCIAL, then=Value(2)),
                    default=Value(3),
                    output_field=IntegerField(),
                )
            ).order_by(
                #ordena por prioridad y luego llegada
                'ranking_prioridad',
                'fecha_creacion'
            ).first() # toma al primero

            #si no hay nadie esperando
            if not candidato:
                return Response(
                    {"mensaje":"No hay tickets pendientes en tus colas"}
                )
            
            candidato.escritorio_asignado = escritorio
            candidato.fecha_llamada=timezone.now()
            candidato.estado = Ticket.Estados.LLAMANDO
            candidato.save()
            serializers = TicketReadSerializer(candidato)

            return Response(serializers.data, status=status.HTTP_200_OK)
    @action(detail=True, methods=['post'])
    def finalizar(self, request, pk=None):
        #obtener ticket:
        ticket = self.get_object()
        usuario_actual= request.user

        if not ticket.escritorio_asignado or ticket.escritorio_asignado.usuario != usuario_actual:
            return Response(
                {"error":"No puedes finalizar un ticket de otra ventanilla"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        #SOLO SE puede finalizar el ticket que esta en "llamando"
        if ticket.estado not in [Ticket.Estados.LLAMANDO, Ticket.Estados.ATENCION]:
            return Response(
                {"error":"Este ticket ya fue finalizado o aun esta pendiente"},
                status= status.HTTP_403_FORBIDDEN
            )
        #SI TODO ESTA BIEN
        ticket.estado = Ticket.Estados.FINALIZADO
        ticket.fecha_fin = timezone.now()
        ticket.save()
        serializers = TicketReadSerializer(ticket)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def no_show(self, request, pk=None):
        ticket = self.get_object()
        usuario_actual = request.user

        if not ticket.escritorio_asignado or ticket.escritorio_asignado.usuario != usuario_actual:
            return Response(
                {"error":"Este ticket no es tuyo"},
                status=status.HTTP_403_FORBIDDEN
            )
        ticket.estado = Ticket.Estados.NO_SHOW
        ticket.fecha_fin  = timezone.now()
        ticket.save()
        return Response(
            {"mensaje":"Ticket marcado como No se PRESENTO"},
            status=status.HTTP_200_OK
        )




class EscritorioViewSet(viewsets.ModelViewSet):
    queryset = Escritorio.objects.all()
    #permission_classes = [EsRolAdministrador]
    # ESTA ES LA CLAVE MÁGICA ⬇
    def get_serializer_class(self):
        # Si la petición es GET (listar o ver uno), usa el detallado
        if self.action in ['list', 'retrieve']:
            return EscritorioReadSerializer
        
        # Si la petición es POST, PUT o PATCH, usa el de escritura
        return EscritorioWriteSerializer