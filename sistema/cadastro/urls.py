from django.urls import path
from .views import listar_pacientes

urlpatterns = [
    path('pacientes/', listar_pacientes, name='listar_pacientes'),
]
