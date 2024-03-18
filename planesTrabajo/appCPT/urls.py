
from django.urls import path
from . import views
from .views import academic_management, contrasena
from .views import custom_logout


urlpatterns = [
    path('start/', views.starpAPP, name='start'),  # URL para la vista starpAPP o página de inicio
    path('modulo-docente/', views.modTeacher, name='mod_teacher'), # La URL '/modulo-docente/' redirigirá a la vista modTeacher
    path('obtener_detalles_curso/', views.tu_vista_ajax, name='obtener_detalles_curso'),
    path('signin/', views.signin, name='signin'),
    path('cambiar-contrasena/', contrasena, name='cambiar_contrasena'),
    path('logout/', custom_logout, name='logout'),
    path('academic_management/', academic_management, name='academic_management'),
    path('registro_usuario/', views.academic_management, name='registro_usuario'),
    path('generar-reporte-pdf/', views.generar_reporte_pdf, name='generar_reporte_pdf'),
    
]
