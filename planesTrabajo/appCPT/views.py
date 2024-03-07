from telnetlib import AUTHENTICATION
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from appCPT.forms import ActividadDocenteForm, ActividadExtensionForm, ActividadGestionForm, ActividadInvestigativaForm, Curso, UserProfileForm
from appCPT.models import ActividadDocente, ActividadExtension, ActividadGestion, ActividadInvestigativa, Profesor, Usuario
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
from .forms import UserProfileForm, UsuarioForm
from .forms import CambioContrasenaForm
from appCPT.models import PeriodoAcademico
from django.db.models import Sum
from django.contrib.auth import logout



def tu_vista_ajax(request): 
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        curso_id = request.GET.get('curso_id')
        if curso_id:
            curso = Curso.objects.get(pk=curso_id)
            detalles_curso = {
                'codigo': curso.codigo,
                'horario': curso.horario,
                'grupo': curso.grupo,
                'numero_horas': curso.numero_horas
            }
            return JsonResponse(detalles_curso)
    return JsonResponse({}, status=400)


def starpAPP(request): 
    return render(request, 'appCPT/starpAPP.html')




@login_required(login_url='/signin/')
def modTeacher(request):
    usuario = request.user
    profesor = get_object_or_404(Profesor, usuario=usuario)
    actividades_docentes = ActividadDocente.objects.filter(profesor=profesor)

    actividad_docente_form = ActividadDocenteForm(initial={'profesor': profesor})
    actividad_investigativa_form = ActividadInvestigativaForm()
    actividad_gestion_form = ActividadGestionForm()
    actividad_extension_form = ActividadExtensionForm()

    periodos_academicos = PeriodoAcademico.objects.all()
    selected_periodo_academico = request.POST.get('periodo_academico', '')

    total_horas_acumuladas = 0  # Inicializamos la variable

    if selected_periodo_academico:
        # Filtrar actividades docentes por período académico
        actividades_docentes = actividades_docentes.filter(periodo_academico__id=selected_periodo_academico)
        
        # Filtrar actividades investigativas por período académico
        actividades_investigativas = ActividadInvestigativa.objects.filter(
            profesor=profesor, periodo_academico__id=selected_periodo_academico
        )

        # Filtrar actividades de gestión por período académico
        actividades_gestion = ActividadGestion.objects.filter(
            profesor=profesor, periodo_academico__id=selected_periodo_academico
        )

        # Filtrar actividades de extensión por período académico
        actividades_extension = ActividadExtension.objects.filter(
            profesor=profesor, periodo_academico__id=selected_periodo_academico
        )

        # Calcular total de horas de actividades docentes
        total_horas = actividades_docentes.aggregate(
            total_horas=Sum('horas_curso') + Sum('tutorias_estudiantes_horas') + Sum('preparacion_horas') + Sum('evaluacion_horas')
        )['total_horas']

        # Calcular total de horas investigativas
        total_horas_investigativas = actividades_investigativas.aggregate(
            total_horas_investigativas=Sum('horas_semanales')
        )['total_horas_investigativas']

        # Calcular total de horas de actividades de gestión
        total_horas_gestion = actividades_gestion.aggregate(
            total_horas_gestion=Sum('actividad_gestion')
        )['total_horas_gestion']

        # Calcular total de horas de actividades de extensión
        total_horas_extension = actividades_extension.aggregate(
            total_horas_extension=Sum('horas_semanales')
        )['total_horas_extension']

        # Calcular total de horas acumuladas
        total_horas_acumuladas += (
            total_horas or 0
        ) + (
            total_horas_investigativas or 0
        ) + (
            total_horas_gestion or 0
        ) + (
            total_horas_extension or 0
        )

    else:
        actividades_investigativas = ActividadInvestigativa.objects.filter(profesor=profesor)
        actividades_gestion = ActividadGestion.objects.filter(profesor=profesor)
        actividades_extension = ActividadExtension.objects.filter(profesor=profesor)
        total_horas = None
        total_horas_investigativas = None
        total_horas_gestion = None
        total_horas_extension = None

    if request.method == 'POST':
        if 'actividad_docente_submit' in request.POST:
            actividad_docente_form = ActividadDocenteForm(request.POST)
            if actividad_docente_form.is_valid():
                actividad_docente = actividad_docente_form.save(commit=False)
                actividad_docente.profesor = profesor
                actividad_docente.save()
                return redirect('nombre_de_la_url')
        elif 'actividad_investigativa_submit' in request.POST:
            actividad_investigativa_form = ActividadInvestigativaForm(request.POST)
            if actividad_investigativa_form.is_valid():
                actividad_investigativa = actividad_investigativa_form.save(commit=False)
                actividad_investigativa.profesor = profesor
                actividad_investigativa.save()
                return redirect('nombre_de_la_url')
        elif 'actividad_gestion_submit' in request.POST:
            actividad_gestion_form = ActividadGestionForm(request.POST)
            if actividad_gestion_form.is_valid():
                actividad_gestion = actividad_gestion_form.save(commit=False)
                actividad_gestion.profesor = profesor
                actividad_gestion.save()
                return redirect('nombre_de_la_url')
        elif 'actividad_extension_submit' in request.POST:
            actividad_extension_form = ActividadExtensionForm(request.POST)
            if actividad_extension_form.is_valid():
                actividad_extension = actividad_extension_form.save(commit=False)
                actividad_extension.profesor = profesor
                actividad_extension.save()
                return redirect('nombre_de_la_url')

    return render(request, 'appCPT/modTeacher.html', {
        'actividades_docentes': actividades_docentes,
        'actividades_investigativas': actividades_investigativas,
        'actividades_gestion': actividades_gestion,
        'actividades_extension': actividades_extension,
        'periodos_academicos': periodos_academicos,
        'total_horas': total_horas,
        'total_horas_investigativas': total_horas_investigativas,
        'total_horas_gestion': total_horas_gestion,
        'total_horas_extension': total_horas_extension,
        'selected_periodo_academico': selected_periodo_academico,
        'actividad_docente_form': actividad_docente_form,
        'actividad_investigativa_form': actividad_investigativa_form,
        'actividad_gestion_form': actividad_gestion_form,
        'actividad_extension_form': actividad_extension_form,
        'profesor': profesor,
        'total_horas_acumuladas': total_horas_acumuladas,
    })


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Iniciar sesión manualmente
            login(request, user)
            
            # Redireccionar según el rol_id del usuario
            if user.rol_id == 3:
                return redirect('http://localhost:8000/modulo-docente/')
            elif user.rol_id == 2:
                return redirect('http://localhost:8000/academic_management/')
            else:
                # Si el usuario no tiene un rol válido, puedes redirigirlo a una página de error
                return redirect('ruta_a_pagina_de_error')
        else:
            # Si las credenciales son incorrectas, mostrar un mensaje de error
            error_message = "Credenciales incorrectas. Inténtalo de nuevo."
            return render(request, 'appCPT/signin.html', {'error': error_message})

    return render(request, 'appCPT/signin.html')



def profile(request):
    user_profile_form = UserProfileForm(instance=request.user)

    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST, instance=request.user)
        if user_profile_form.is_valid():
            user_profile_form.save()

    vinculacion = None
    if hasattr(request.user, 'profesor'):
        vinculacion = request.user.profesor.vinculacion.descripcion if request.user.profesor.vinculacion else None

@login_required
def contrasena(request):
    if request.method == 'POST':
        form = CambioContrasenaForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # Puedes redirigir a donde desees después de cambiar la contraseña
            return redirect('http://localhost:8000/modulo-docente/')
    else:
        form = CambioContrasenaForm(request.user)
    
    return render(request, 'appCPT/contrasena.html', {'form': form})

def custom_logout(request):
   
    return redirect('http://localhost:8000/start/#')

def custom_logout(request):
    logout(request)
    return redirect('http://localhost:8000/start/#')

from django.shortcuts import render, redirect, get_object_or_404
from .forms import CursoForm
from .models import Curso
from django.contrib.auth.decorators import login_required
from .forms import UsuarioForm
from .models import Usuario

from django.shortcuts import render, redirect, get_object_or_404
from .forms import CursoForm, UsuarioForm
from .models import Curso, Usuario
from django.contrib.auth.decorators import login_required

@login_required(login_url='/signin/')
def academic_management(request, curso_id=None):
    curso_form = CursoForm()
    usuario_form = UsuarioForm()
    cursos_registrados = Curso.objects.all()
    usuarios_registrados = Usuario.objects.all()

    if request.method == 'POST':
        if 'curso_id' in request.POST:
            curso_id = request.POST.get('curso_id')
            if curso_id:  
                # Edición de un curso existente
                curso_instance = get_object_or_404(Curso, pk=curso_id)
                curso_form = CursoForm(request.POST, instance=curso_instance)
            else:  
                # Agregar un nuevo curso
                curso_form = CursoForm(request.POST)
            
            if curso_form.is_valid():
                curso_form.save()
                return redirect('inicio')
            else:
                # Se ha producido un error al crear o editar el curso
                context = {
                    'curso_form': curso_form,
                    'cursos_registrados': Curso.objects.all(),
                    'curso_instance': curso_instance, # Se agrega la variable curso_instance
                }
                return render(request, 'appCPT/modAcademicManagement.html', context)
        else:
            usuario_form = UsuarioForm(request.POST)
            if usuario_form.is_valid():
                usuario_form.save()
                return redirect('academic_management')

    else:
        curso_id = request.GET.get('curso_id')
        if curso_id:  
            # Edición de un curso existente
            curso_instance = get_object_or_404(Curso, pk=curso_id)
            curso_form = CursoForm(instance=curso_instance)
        else:  
            # Agregar un nuevo curso
            curso_instance = Curso() # Crea una instancia vacía
            curso_form = CursoForm(instance=curso_instance)

    context = {
        'curso_form': curso_form,
        'cursos_registrados': cursos_registrados,
        'curso_instance': curso_instance, # Se agrega la variable curso_instance
        'usuario_form': usuario_form,
        'usuarios_registrados': usuarios_registrados,
    }
    return render(request, 'appCPT/modAcademicManagement.html', context)

    


