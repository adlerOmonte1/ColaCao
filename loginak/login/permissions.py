from rest_framework import permissions
class EsRolAdministrador(permissions.BasePermission):
    """
    Permiso custom para verificar si el usuario tiene el Rol 'Administrador'
    basado en tu modelo personalizado.
    """
    def has_permission(self, request, view):
        #verifica q este logueado
        if not request.user or not request.user.is_authenticated:
            return False
        #verifica que tenga rol asignado
        if not request.user.rol:
            return False
        #Verifica el nombre de rol
        return request.user.rol.nombre == 'Administrador'