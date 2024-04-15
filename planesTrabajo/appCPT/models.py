from django.db import models
from django.contrib.auth.models import AbstractUser

class CentroCostos(models.Model):
    descripcion = models.CharField(max_length=45)

class PeriodoAcademico(models.Model):
    descripcion = models.CharField(max_length=45)
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()

class Departamento(models.Model):
    descripcion = models.CharField(max_length=45)

class Facultad(models.Model):
    descripcion = models.CharField(max_length=45)

class Rol(models.Model):
    descripcion = models.CharField(max_length=45)

class Usuario(AbstractUser):
    cedula = models.CharField(max_length=45)
    departamento = models.ForeignKey(Departamento, on_delete=models.DO_NOTHING, null=True)
    facultad = models.ForeignKey(Facultad, on_delete=models.DO_NOTHING)
    rol = models.ForeignKey(Rol, on_delete=models.DO_NOTHING)

class Vinculacion(models.Model):
    descripcion = models.CharField(max_length=45)

class Profesor(models.Model):
    dedicacion = models.IntegerField(null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    vinculacion = models.ForeignKey(Vinculacion, on_delete=models.DO_NOTHING)

class ProyectoCurricular(models.Model):
    descripcion = models.CharField(max_length=45)

class Curso(models.Model):
    nombre = models.CharField(max_length=45)
    codigo = models.IntegerField()
    numero_horas = models.DecimalField(max_digits=20, decimal_places=0)
    nivel = models.CharField(max_length=45)
    proyecto_curricular = models.ForeignKey(ProyectoCurricular, on_delete=models.DO_NOTHING)
    grupo = models.IntegerField()
    semestre = models.IntegerField()
    estado = models.IntegerField()
    horario = models.CharField(max_length=90)
    departamento = models.ForeignKey(Departamento, on_delete=models.DO_NOTHING)

class Nivel(models.Model):
    descripcion = models.CharField(max_length=45)

class ActividadDocente(models.Model):
    numero_estudiantes = models.IntegerField()
    horas_curso = models.IntegerField()
    tutorias_estudiantes_horas = models.IntegerField()
    preparacion_horas = models.IntegerField()
    evaluacion_horas = models.IntegerField()
    centro_costos = models.ForeignKey(CentroCostos, on_delete=models.DO_NOTHING)
    curso = models.ForeignKey(Curso, on_delete=models.DO_NOTHING)
    nivel = models.ForeignKey(Nivel, on_delete=models.DO_NOTHING)
    periodo_academico = models.ForeignKey(PeriodoAcademico, on_delete=models.DO_NOTHING)
    profesor = models.ForeignKey(Profesor, on_delete=models.DO_NOTHING)
    proyecto_curricular = models.ForeignKey(ProyectoCurricular, on_delete=models.DO_NOTHING)

class ActividadExtension(models.Model):
    titulo = models.CharField(max_length=100)
    codigo = models.IntegerField()
    horas_semanales = models.IntegerField()
    centro_costos = models.ForeignKey(CentroCostos, on_delete=models.DO_NOTHING)
    periodo_academico = models.ForeignKey(PeriodoAcademico, on_delete=models.DO_NOTHING)
    profesor = models.ForeignKey(Profesor, on_delete=models.DO_NOTHING)

class ActividadGestion(models.Model):
    actividad_gestion = models.IntegerField()
    horas_semana = models.IntegerField()
    centro_costos = models.ForeignKey(CentroCostos, on_delete=models.DO_NOTHING)
    periodo_academico = models.ForeignKey(PeriodoAcademico, on_delete=models.DO_NOTHING)
    profesor = models.ForeignKey(Profesor, on_delete=models.DO_NOTHING)

class ActividadInvestigativa(models.Model):
    tipo_actividad_investigativa = models.CharField(max_length=100)
    funcion = models.CharField(max_length=45)
    acta_facultad = models.CharField(max_length=15)
    titulo_proyecto = models.CharField(max_length=200)
    horas_semanales = models.IntegerField()
    centro_costos = models.ForeignKey(CentroCostos, on_delete=models.DO_NOTHING)
    nivel = models.ForeignKey(Nivel, on_delete=models.DO_NOTHING)
    periodo_academico = models.ForeignKey(PeriodoAcademico, on_delete=models.DO_NOTHING)
    profesor = models.ForeignKey(Profesor, on_delete=models.DO_NOTHING)
    proyecto_curricular = models.ForeignKey(ProyectoCurricular, on_delete=models.DO_NOTHING)
