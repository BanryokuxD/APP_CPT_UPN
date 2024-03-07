from django.contrib.auth.models import AbstractUser
from django.db import models


class ActividadDocente(models.Model):
    curso = models.ForeignKey('Curso', models.DO_NOTHING)
    periodo_academico = models.ForeignKey('PeriodoAcademico', models.DO_NOTHING)
    nivel = models.ForeignKey('Nivel', models.DO_NOTHING)
    id = models.AutoField(primary_key=True)
    numero_estudiantes = models.IntegerField()
    profesor = models.ForeignKey('Profesor', models.DO_NOTHING)
    proyecto_curricular = models.ForeignKey('ProyectoCurricular', models.DO_NOTHING)
    horas_curso = models.IntegerField()
    tutorias_estudiantes_horas = models.IntegerField()
    preparacion_horas = models.IntegerField()
    evaluacion_horas = models.IntegerField()
    centro_costos = models.ForeignKey('CentroCostos', models.DO_NOTHING)

class ActividadExtension(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    periodo_academico = models.ForeignKey('PeriodoAcademico', models.DO_NOTHING)
    centro_costos = models.ForeignKey('CentroCostos', models.DO_NOTHING)
    coidgo = models.IntegerField()
    horas_semanales = models.IntegerField(db_column='horas_semanales')  # Field renamed to remove unsuitable characters.
    profesor = models.ForeignKey('Profesor', models.DO_NOTHING)

class ActividadGestion(models.Model):
    id = models.AutoField(primary_key=True)
    actividad_gestion = models.IntegerField()
    periodo_academico = models.ForeignKey('PeriodoAcademico', models.DO_NOTHING)
    centro_costos = models.ForeignKey('CentroCostos', models.DO_NOTHING)
    profesor = models.ForeignKey('Profesor', models.DO_NOTHING)
    horas_semana = models.IntegerField()

class ActividadInvestigativa(models.Model):
    id = models.AutoField(primary_key=True)
    tipo_actividad_investigativa = models.CharField(max_length=100)
    funcion = models.CharField(max_length=45)
    acta_facultad = models.CharField(max_length=15)
    titulo_proyecto = models.CharField(max_length=200)
    nivel = models.ForeignKey('Nivel', models.DO_NOTHING)
    periodo_academico = models.ForeignKey('PeriodoAcademico', models.DO_NOTHING)
    proyecto_curricular = models.ForeignKey('ProyectoCurricular', models.DO_NOTHING)
    centro_costos = models.ForeignKey('CentroCostos', models.DO_NOTHING)
    horas_semanales = models.IntegerField()
    profesor = models.ForeignKey('Profesor', models.DO_NOTHING)

class CentroCostos(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45)

class Curso(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    codigo = models.IntegerField()
    numero_horas = models.DecimalField(max_digits=20, decimal_places=0)
    nivel = models.CharField(max_length=45)
    proyecto_curricular = models.CharField(max_length=45)
    grupo = models.IntegerField()
    semestre = models.IntegerField()
    estado = models.IntegerField()
    horario = models.CharField(max_length=90)
    departamento = models.ForeignKey('Departamento', models.DO_NOTHING)

class Departamento(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45)

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'appcpt_departamento'

class Facultad(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45)

class Nivel(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45)

class PeriodoAcademico(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()

class Profesor(models.Model):
    id = models.IntegerField(primary_key=True)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)  # Ajusta aquí
    vinculacion = models.ForeignKey('Vinculacion', models.DO_NOTHING)
    dedicacion = models.IntegerField(blank=True, null=True)

class ProyectoCurricular(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45)

class Rol(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45)

class Usuario(AbstractUser):
    cedula = models.CharField(max_length=45)
    departamento = models.ForeignKey('Departamento', models.DO_NOTHING, null=True)
    facultad = models.ForeignKey('Facultad', models.DO_NOTHING)
    rol = models.ForeignKey('Rol', models.DO_NOTHING)
    
class Vinculacion(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45)
