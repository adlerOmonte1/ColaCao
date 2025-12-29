
from django.contrib import admin
from django.urls import path,include
from login.views import RegisterView,MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers
from login import views
router = routers.DefaultRouter()
router.register('usuarios', views.UsuarioViewset)
router.register('tickets',views.TicketViewSet)
router.register('colas',views.ColaViewSet)
router.register('roles',views.RolesViewSet)
router.register('escritorios',views.EscritorioViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    #EDPOINTS

    path('api/auth/register/',RegisterView.as_view(), name='auth_register'),
    path('api/auth/login/',MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]
