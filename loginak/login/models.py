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
    
