from django.contrib import admin
from .models import Paciente, Terapeuta, Familiar

admin.site.register(Paciente)
admin.site.register(Terapeuta)
admin.site.register(Familiar)
