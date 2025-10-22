from django.http import JsonResponse
from .models import Paciente

def listar_pacientes(request):
    data = list(Paciente.objects.values('id','nome','data_nascimento','responsavel_id','criado_em'))
    return JsonResponse(data, safe=False)
