from django.db import models


class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

class Usuario(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    usuario = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    contraseña = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    edad = models.IntegerField(blank=True, null=True)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    sexo = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    edad = models.IntegerField(blank=True, null=True)
    sexo = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

class EstadoAmbulancia(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

class Ambulancia(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    patente = models.CharField(max_length=10, unique=True)
    conductor = models.CharField(max_length=100)
    estado = models.ForeignKey(EstadoAmbulancia, on_delete=models.PROTECT)

class FichaClinica(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ambulancia = models.ForeignKey(Ambulancia, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    estado_conciencia = models.CharField(max_length=50, blank=True, null=True)
    estado_pupilas = models.CharField(max_length=50, blank=True, null=True)
    alergias = models.CharField(max_length=100, blank=True, null=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    presion_arterial = models.CharField(max_length=10, blank=True, null=True)
    frecuencia_cardiaca = models.PositiveIntegerField(blank=True, null=True)
    frecuencia_respiratoria = models.PositiveIntegerField(blank=True, null=True)
    saturacion_oxigeno = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    nivel_glucosa = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sintomas = models.TextField(blank=True, null=True)
    lesiones_visibles = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    archivo_clinico = models.FileField(upload_to='fichas/', blank=True, null=True)

class Auditoria(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    accion = models.CharField(max_length=255)
    tabla = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
