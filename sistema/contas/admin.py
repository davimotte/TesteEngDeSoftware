# contas/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Clinica, Terapeuta, Familiar, AdministradorClinica, Paciente

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'tipo', 'is_staff', 'ativo')
    list_filter = ('tipo', 'is_staff', 'is_superuser', 'ativo')  # ✅ Use 'ativo' em vez de 'is_active'
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'cpf', 'telefone')}),
        ('Permissões', {'fields': ('tipo', 'ativo', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined', 'data_cadastro')}),
    )

# Registre outros modelos se necessário
admin.site.register(Clinica)
admin.site.register(Terapeuta)
admin.site.register(Familiar)
admin.site.register(AdministradorClinica)
admin.site.register(Paciente)