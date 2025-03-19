from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Usuario, Libro, Prestamo, Estado
from .forms import RegistroUsuarioForm, LibroForm

def home(request):
    # Vista para la página principal, mostrará los libros disponibles
    libros = Libro.objects.all()
    return render(request, 'libros/home.html', {'libros': libros})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('libros:home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'libros/login.html')

def logout_view(request):
    logout(request)
    return redirect('libros:home')

# Completa esta función
def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido al Club de Intercambio de Libros.')
            return redirect('libros:home')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'libros/registro.html', {'form': form})

@login_required
def mis_libros(request):
    libros = Libro.objects.filter(usuario=request.user)
    return render(request, 'libros/mis_libros.html', {'libros': libros})

@login_required
def nuevo_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            libro = form.save(commit=False)
            libro.usuario = request.user
            libro.save()
            messages.success(request, 'Libro añadido correctamente')
            return redirect('libros:mis_libros')
    else:
        form = LibroForm()
    
    return render(request, 'libros/libro_form.html', {
        'form': form, 
        'titulo': 'Nuevo Libro'
    })

@login_required
def detalle_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    # Verificar si el usuario actual puede solicitar este libro
    puede_solicitar = (
        request.user.is_authenticated and 
        libro.usuario != request.user and 
        not Prestamo.objects.filter(
            libro=libro,
            usuario=request.user,
            estado__descripcion__in=['Solicitado', 'Aceptado']
        ).exists()
    )
    
    return render(request, 'libros/detalle_libro.html', {
        'libro': libro,
        'puede_solicitar': puede_solicitar
    })

@login_required
def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    # Verificar que el usuario sea el propietario del libro
    if libro.usuario != request.user:
        messages.error(request, 'No tienes permiso para editar este libro')
        return redirect('libros:home')
    
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Libro actualizado correctamente')
            return redirect('libros:detalle_libro', libro_id=libro.id)
    else:
        form = LibroForm(instance=libro)
    
    return render(request, 'libros/libro_form.html', {
        'form': form, 
        'titulo': 'Editar Libro'
    })

@login_required
def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    # Verificar que el usuario sea el propietario del libro
    if libro.usuario != request.user:
        messages.error(request, 'No tienes permiso para eliminar este libro')
        return redirect('libros:home')
    
    if request.method == 'POST':
        libro.delete()
        messages.success(request, 'Libro eliminado correctamente')
        return redirect('libros:mis_libros')
    
    return render(request, 'libros/confirmar_eliminar.html', {'libro': libro})

@login_required
def mis_prestamos(request):
    # Obtener los préstamos que el usuario ha solicitado a otros
    prestamos_solicitados = Prestamo.objects.filter(usuario=request.user)
    
    # Obtener los préstamos que otros han solicitado al usuario
    prestamos_recibidos = Prestamo.objects.filter(libro__usuario=request.user)
    
    return render(request, 'libros/mis_prestamos.html', {
        'prestamos_solicitados': prestamos_solicitados,
        'prestamos_recibidos': prestamos_recibidos
    })

@login_required
def solicitar_prestamo(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    
    # Verificar que el usuario no sea el propietario del libro
    if libro.usuario == request.user:
        messages.error(request, 'No puedes solicitar tu propio libro')
        return redirect('libros:detalle_libro', libro_id=libro.id)
    
    # Verificar si ya existe una solicitud activa
    if Prestamo.objects.filter(
        libro=libro,
        usuario=request.user,
        estado__descripcion__in=['Solicitado', 'Aceptado']
    ).exists():
        messages.error(request, 'Ya tienes una solicitud activa para este libro')
        return redirect('libros:detalle_libro', libro_id=libro.id)
    
    # Crear la solicitud de préstamo
    estado_solicitado = Estado.objects.get(descripcion='Solicitado')
    Prestamo.objects.create(
        libro=libro,
        usuario=request.user,
        estado=estado_solicitado
    )
    
    messages.success(request, 'Solicitud de préstamo enviada correctamente')
    return redirect('libros:mis_prestamos')

@login_required
def aceptar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    
    # Verificar que el usuario sea el propietario del libro
    if prestamo.libro.usuario != request.user:
        messages.error(request, 'No tienes permiso para aceptar este préstamo')
        return redirect('libros:mis_prestamos')
    
    # Verificar que el préstamo esté en estado 'Solicitado'
    if prestamo.estado.descripcion != 'Solicitado':
        messages.error(request, 'Este préstamo no puede ser aceptado')
        return redirect('libros:mis_prestamos')
    
    # Actualizar el estado del préstamo
    estado_aceptado = Estado.objects.get(descripcion='Aceptado')
    prestamo.estado = estado_aceptado
    prestamo.save()
    
    messages.success(request, 'Préstamo aceptado correctamente')
    return redirect('libros:mis_prestamos')

@login_required
def cancelar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    
    # Verificar que el usuario sea el propietario del libro o quien solicitó el préstamo
    if prestamo.libro.usuario != request.user and prestamo.usuario != request.user:
        messages.error(request, 'No tienes permiso para cancelar este préstamo')
        return redirect('libros:mis_prestamos')
    
    # Verificar que el préstamo esté en estado 'Solicitado' o 'Aceptado'
    if prestamo.estado.descripcion not in ['Solicitado', 'Aceptado']:
        messages.error(request, 'Este préstamo no puede ser cancelado')
        return redirect('libros:mis_prestamos')
    
    # Actualizar el estado del préstamo
    estado_cancelado = Estado.objects.get(descripcion='Cancelado')
    prestamo.estado = estado_cancelado
    prestamo.save()
    
    messages.success(request, 'Préstamo cancelado correctamente')
    return redirect('libros:mis_prestamos')

@login_required
def devolver_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    
    # Verificar que el usuario sea el propietario del libro
    if prestamo.libro.usuario != request.user:
        messages.error(request, 'No tienes permiso para marcar este préstamo como devuelto')
        return redirect('libros:mis_prestamos')
    
    # Verificar que el préstamo esté en estado 'Aceptado'
    if prestamo.estado.descripcion != 'Aceptado':
        messages.error(request, 'Este préstamo no puede ser marcado como devuelto')
        return redirect('libros:mis_prestamos')
    
    # Actualizar el estado del préstamo
    estado_devuelto = Estado.objects.get(descripcion='Devuelto')
    prestamo.estado = estado_devuelto
    prestamo.fecha_devolucion = timezone.now()
    prestamo.save()
    
    messages.success(request, 'Libro marcado como devuelto correctamente')
    return redirect('libros:mis_prestamos')
