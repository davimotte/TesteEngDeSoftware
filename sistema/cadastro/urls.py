from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import TerapeutaViewSet, PacienteViewSet, FamiliarViewSet

router = DefaultRouter()
router.register(r"terapeutas", TerapeutaViewSet, basename="terapeuta")
router.register(r"pacientes", PacienteViewSet, basename="paciente")
router.register(r"familiares", FamiliarViewSet, basename="familiar")

urlpatterns = [
    path("", include(router.urls)),
]
