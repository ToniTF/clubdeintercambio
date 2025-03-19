from django.urls import path
from . import views

app_name = 'libros'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    
    # URLs para libros
    path('mis-libros/', views.mis_libros, name='mis_libros'),
    path('libro/nuevo/', views.nuevo_libro, name='nuevo_libro'),
    path('libro/<int:libro_id>/', views.detalle_libro, name='detalle_libro'),
    path('libro/<int:libro_id>/editar/', views.editar_libro, name='editar_libro'),
    path('libro/<int:libro_id>/eliminar/', views.eliminar_libro, name='eliminar_libro'),
    
    # URLs para préstamos
    path('mis-prestamos/', views.mis_prestamos, name='mis_prestamos'),
    path('libro/<int:libro_id>/solicitar/', views.solicitar_prestamo, name='solicitar_prestamo'),
    path('prestamo/<int:prestamo_id>/aceptar/', views.aceptar_prestamo, name='aceptar_prestamo'),
    path('prestamo/<int:prestamo_id>/cancelar/', views.cancelar_prestamo, name='cancelar_prestamo'),
    path('prestamo/<int:prestamo_id>/devolver/', views.devolver_prestamo, name='devolver_prestamo'),
]