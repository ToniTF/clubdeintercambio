from django.db import migrations

def crear_estados_iniciales(apps, schema_editor):
    Estado = apps.get_model('libros', 'Estado')
    estados = [
        'Solicitado',
        'Aceptado',
        'Cancelado',
        'Devuelto'
    ]
    for estado in estados:
        Estado.objects.create(descripcion=estado)

class Migration(migrations.Migration):
    dependencies = [
        ('libros', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_estados_iniciales),
    ]