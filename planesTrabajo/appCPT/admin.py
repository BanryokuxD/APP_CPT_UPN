from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.admin.widgets import AdminIntegerFieldWidget
from .models import Usuario, Departamento, Facultad, Rol

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Usuario

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # Campos adicionales que deseas mostrar en el formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Información personalizada', {'fields': ('cedula', 'departamento', 'facultad', 'rol')}),
    )

    # Lista de desplegable personalizada para los campos relacionados
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "departamento":
            kwargs["queryset"] = Departamento.objects.all()
        elif db_field.name == "facultad":
            kwargs["queryset"] = Facultad.objects.all()
        elif db_field.name == "rol":
            kwargs["queryset"] = Rol.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Personalizar la representación de los campos ForeignKey en la vista de detalle
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "departamento" and isinstance(field.widget, AdminIntegerFieldWidget):
            field.widget = admin.widgets.AdminTextInputWidget()
        elif db_field.name == "facultad" and isinstance(field.widget, AdminIntegerFieldWidget):
            field.widget = admin.widgets.AdminTextInputWidget()
        elif db_field.name == "rol" and isinstance(field.widget, AdminIntegerFieldWidget):
            field.widget = admin.widgets.AdminTextInputWidget()
        return field

admin.site.register(Usuario, CustomUserAdmin)
