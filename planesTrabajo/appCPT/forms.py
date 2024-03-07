from django import forms
from .models import ActividadDocente, ActividadExtension, ActividadGestion, ActividadInvestigativa, Curso, Nivel, CentroCostos, PeriodoAcademico, ProyectoCurricular
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario
from appCPT import models
from .models import Curso

class ActividadDocenteForm(forms.ModelForm):
    
    numero_estudiantes = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 41)],
                                           label='Número de Estudiantes',
                                           widget=forms.Select(attrs={'class': 'form-control'}))
    
    tutorias_estudiantes_horas = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 3)],
                                           label='Tutoría a estudiantes/Horas',
                                           widget=forms.Select(attrs={'class': 'form-control'}))
    preparacion_horas = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 3)],
                                           label='Preparación, actualización, sistematización e innovación de clases/Horas',
                                           widget=forms.Select(attrs={'class': 'form-control'}))
    evaluacion_horas = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 3)],
                                           label='Evaluación de actividades/Horas',
                                           widget=forms.Select(attrs={'class': 'form-control'}))
    
    
    def __init__(self, *args, **kwargs):
        super(ActividadDocenteForm, self).__init__(*args, **kwargs)
        self.fields['curso'].label_from_instance = lambda obj: obj.nombre
        self.fields['nivel'].label_from_instance = lambda obj: obj.descripcion
        self.fields['centro_costos'].label_from_instance = lambda obj: obj.descripcion
        self.fields['proyecto_curricular'].label_from_instance = lambda obj: obj.descripcion
        self.fields['periodo_academico'].label_from_instance = lambda obj: obj.descripcion

        self.fields['curso'].queryset = Curso.objects.filter(estado=1)

        

        instance = kwargs.get('instance')
        if instance:
            self.initial['curso'] = instance.curso.id if instance.curso else None
            self.initial['nivel'] = instance.nivel.id if instance.nivel else None
            self.initial['centro_costos'] = instance.centro_costos.id if instance.centro_costos else None
            self.initial['proyecto_curricular'] = instance.proyecto_curricular.id if instance.proyecto_curricular else None
            self.initial['periodo_academico'] = instance.periodo_academico.id if instance.periodo_academico else None

        curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        empty_label="Seleccionar"
    )

    nivel = forms.ModelChoiceField(
        queryset=Nivel.objects.all(),
        empty_label="Seleccionar"
    )


    proyecto_curricular = forms.ModelChoiceField(
        queryset=ProyectoCurricular.objects.all(),
        empty_label="Seleccionar"
    )

    centro_costos = forms.ModelChoiceField(
        queryset=CentroCostos.objects.all(),
        empty_label="Seleccionar"
    )   

    periodo_academico = forms.ModelChoiceField(
        queryset=PeriodoAcademico.objects.all(),
        empty_label="Seleccionar"
    ) 

    horas_curso = forms.IntegerField(
        label='Horas del curso',
        required=False  # Ajusta esto según tus requisitos
    )

    def save(self, commit=True):
        # Llama al método save del formulario padre
        actividad_docente = super(ActividadDocenteForm, self).save(commit=False)

        # Tu lógica para cambiar el estado del curso a 0
        curso = actividad_docente.curso
        curso.estado = 0
        curso.save()

        if commit:
            actividad_docente.save()

        return actividad_docente


    class Meta:
        model = ActividadDocente
        exclude = ['id','profesor']  # Excluyendo campos que no queremos que se muestren en el formulario


          

class ActividadInvestigativaForm(forms.ModelForm):


    FUNCION_CHOICES = [
        ('N/A', 'No aplica'),
        ('Asesor o asistente', 'Asesor o asistentel'),
        ('Asesor o asistente', 'Asesor o asistente'),
        ('Asesor o asistente', 'Asesor o asistente'),
    ]

    TIPO_ACTIVIDAD_CHOICES = [
        ('Dirección de trabajos de grado', 'Dirección de trabajos de grado'),
        ('proyecto_investigacion', 'Proyecto de investigación'),
        ('actividades_extension', 'Actividades de extensión'),
    ]

    funcion = forms.ChoiceField(choices=FUNCION_CHOICES, label='Función', widget=forms.Select(attrs={'class': 'form-control'}))
    tipo_actividad_investigativa = forms.ChoiceField(choices=TIPO_ACTIVIDAD_CHOICES, label='Tipo de actividad investigativa', widget=forms.Select(attrs={'class': 'form-control'}))
    
    def __init__(self, *args, **kwargs):
        super(ActividadInvestigativaForm, self).__init__(*args, **kwargs)
        self.fields['nivel'].label_from_instance = lambda obj: obj.descripcion
        self.fields['centro_costos'].label_from_instance = lambda obj: obj.descripcion
        self.fields['proyecto_curricular'].label_from_instance = lambda obj: obj.descripcion
        self.fields['periodo_academico'].label_from_instance = lambda obj: obj.descripcion

        instance = kwargs.get('instance')
        if instance:
            self.initial['nivel'] = instance.nivel.id if instance.nivel else None
            self.initial['centro_costos'] = instance.centro_costos.id if instance.centro_costos else None
            self.initial['proyecto_curricular'] = instance.proyecto_curricular.id if instance.proyecto_curricular else None
            self.initial['periodo_academico'] = instance.periodo_academico.id if instance.periodo_academico else None

    nivel = forms.ModelChoiceField(
        queryset=Nivel.objects.all(),
        empty_label="Seleccionar"
    )

    proyecto_curricular = forms.ModelChoiceField(
        queryset=ProyectoCurricular.objects.all(),
        empty_label="Seleccionar"
    )

    periodo_academico = forms.ModelChoiceField(
        queryset=PeriodoAcademico.objects.all(),
        empty_label="Seleccionar"
    ) 

    centro_costos = forms.ModelChoiceField(
        queryset=CentroCostos.objects.all(),
        empty_label="Seleccionar"
    ) 


    class Meta:
        model = ActividadInvestigativa
        exclude = ['id','profesor']


class ActividadGestionForm(forms.ModelForm):
    

    def __init__(self, *args, **kwargs):
        super(ActividadGestionForm, self).__init__(*args, **kwargs)
        self.fields['centro_costos'].label_from_instance = lambda obj: obj.descripcion
        self.fields['periodo_academico'].label_from_instance = lambda obj: obj.descripcion
        

        instance = kwargs.get('instance')
        if instance:
            self.initial['centro_costos'] = instance.centro_costos.id if instance.centro_costos else None
            self.initial['periodo_academico'] = instance.periodo_academico.id if instance.periodo_academico else None
           
    periodo_academico = forms.ModelChoiceField(
        queryset=PeriodoAcademico.objects.all(),
        empty_label="Seleccionar"
    ) 

    centro_costos = forms.ModelChoiceField(
        queryset=CentroCostos.objects.all(),
        empty_label="Seleccionar"
    ) 

    class Meta:
        model = ActividadGestion
        exclude = ['id','profesor'] 

class ActividadExtensionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ActividadExtensionForm, self).__init__(*args, **kwargs)
        self.fields['centro_costos'].label_from_instance = lambda obj: obj.descripcion
        self.fields['periodo_academico'].label_from_instance = lambda obj: obj.descripcion
        

        instance = kwargs.get('instance')
        if instance:
            self.initial['centro_costos'] = instance.centro_costos.id if instance.centro_costos else None
            self.initial['periodo_academico'] = instance.periodo_academico.id if instance.periodo_academico else None
    
    periodo_academico = forms.ModelChoiceField(
        queryset=PeriodoAcademico.objects.all(),
        empty_label="Seleccionar"
    ) 

    centro_costos = forms.ModelChoiceField(
        queryset=CentroCostos.objects.all(),
        empty_label="Seleccionar"
    )         

    class Meta:
        model = ActividadExtension
        exclude = ['id','profesor'] 


class UserProfileForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email', 'cedula', 'departamento', 'facultad', 'rol')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza la presentación de los campos si es necesario
        # Ejemplo: self.fields['cedula'].label = 'Número de cédula'



from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext as _

class CambioContrasenaForm(PasswordChangeForm):
    class Meta:
        model = Usuario

    old_password = forms.CharField(
        label=_('Contraseña actual'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
        error_messages={
            'password_incorrect': _('La contraseña actual es incorrecta. Vuelve a intentarlo.'),
        },
    )
    new_password1 = forms.CharField(
        label=_('Nueva contraseña'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=_(
            "Tu contraseña no puede ser demasiado similar a tu otra información personal.<br>"
            "Tu contraseña debe contener al menos 8 caracteres.<br>"
            "Tu contraseña no puede ser una contraseña común.<br>"
            "Tu contraseña no puede ser completamente numérica."
        ),
    )
    new_password2 = forms.CharField(
        label=_('Confirmar nueva contraseña'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        error_messages={
            'password_mismatch': _('Las nuevas contraseñas no coinciden. Vuelve a intentarlo.'),
            'password_too_short': _('La nueva contraseña debe contener al menos 8 caracteres.'),
            'password_common': _('La nueva contraseña no puede ser una contraseña común.'),
            'password_entirely_numeric': _('La nueva contraseña no puede ser completamente numérica.'),
        },
    )

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre', 'codigo', 'numero_horas', 'nivel', 'proyecto_curricular', 'grupo', 'semestre', 'estado', 'horario', 'departamento']



from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'cedula', 'departamento', 'facultad', 'rol']
