from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Usuario)
admin.site.register(Rol)
admin.site.register(Escritorio)
admin.site.register(Ticket)
admin.site.register(Cola)