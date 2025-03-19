from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Libro, Prestamo, Estado

# Personalizar la visualización de Usuario en el admin
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'dni', 'first_name', 'last_name', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('dni',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('dni',)}),
    )

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Libro)
admin.site.register(Prestamo)
admin.site.register(Estado)
