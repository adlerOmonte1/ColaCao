from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    #El AbstracUser ya tiene la logica "encriptar", "grupos", "permisos"
    #Se hace el cambio para que la validacion sea por email.
    email = models.EmailField(unique=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True,blank=True) #protect => no se borra si hay usuario usandolo
    #telefono = models.CharField(max_length=9)
    #dni = models.Charfield(max_length=8)
    USERNAME_FIELD = 'email' # por defecto esta el username, pero esto hace el cambio
    REQUIRED_FIELDS = ["username", "first_name","last_name"]
    def __str__(self):
        nombre_rol = self.rol.nombre if self.rol else "sin rol"
        return f"{self.username} : {nombre_rol}"
    
# PROYECTO DE COLACAO
class Cola(models.Model):
    nombre = models.CharField(max_length=100)
    codigo_letra = models.CharField(max_length=10, unique= True)
    descripcion = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.nombre}:{self.codigo_letra}"

class Escritorio(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    numero_ventanilla = models.CharField(max_length=100)
    colas_que_atiende = models.ManyToManyField(Cola,related_name="escritorios")
    def __str__(self):
        return f"{self.numero_ventanilla}:{self.usuario.username}"


class Ticket(models.Model):
    class Estados(models.TextChoices):
        PENDIENTE = 'PENDIENTE','pendiente'
        LLAMANDO = 'LLAMANDO','llamando'
        ATENCION = 'ATENCION','atencion'
        FINALIZADO = 'FINALIZADO','finalizado'
        NO_SHOW = 'NO_SHOW','no se presento'
    class Prioridades(models.TextChoices):
        NORMAL = 'NORMAL','normal'
        PREFERENCIAL = 'PREFERENCIAL','preferencial'
        VIP = 'VIP','vip'
    codigo = models.CharField(max_length=10)
    cola = models.ForeignKey(Cola, on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=20,
        choices=Estados.choices,
        default=Estados.PENDIENTE,
        db_index=True
    )
    prioridad = models.CharField(
        max_length=20,
        choices=Prioridades.choices,
        default=Prioridades.NORMAL
    )
    escritorio_asignado = models.ForeignKey(
        Escritorio, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name="tickets_asignados"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True) #hora llegada
    fecha_llamada = models.DateTimeField(null=True, blank=True) #hora cuando le llaman
    fecha_fin = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.codigo}:{self.estado}"
    