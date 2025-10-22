from django.db import models
from django.conf import settings

class Paciente(models.Model):
    nome = models.CharField(max_length=150)
    data_nascimento = models.DateField(null=True, blank=True)
    responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='pacientes')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Terapeuta(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    conselho = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Terapeuta: {self.usuario.get_full_name() or self.usuario.username}"

class Familiar(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Familiar: {self.usuario.get_full_name() or self.usuario.username}"
