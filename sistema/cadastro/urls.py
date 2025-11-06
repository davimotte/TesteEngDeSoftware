from django.urls import path
from . import views

urlpatterns = [
    path("familiares", views.criar_familiar, name="familiares-criar"),
    path("terapeutas", views.criar_terapeuta, name="terapeutas-criar"),
    path("pacientes", views.criar_paciente, name="pacientes-criar"),
    path("clinicas", views.criar_clinica, name="clinicas-criar"),
    path("usuarios/<int:id_usuario>/consentimento", views.registrar_consentimento, name="usuarios-consentimento"),
]

