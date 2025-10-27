from functools import wraps
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..dominio.servicos import CadastroServico
from ..infraestrutura.repos_memoria import (
    TerapeutasRepoMemoria, PacientesRepoMemoria, FamiliaresRepoMemoria
)

from .serializers import (
    TerapeutaInSerializer, TerapeutaOutSerializer,
    PacienteInSerializer, PacienteOutSerializer,
    FamiliarInSerializer, FamiliarOutSerializer,
    TransferenciaInSerializer
)
from .permissions import IsAdminClinica
from ..dominio.erros import RecursoNaoEncontrado, ConflitoUnico, RegraNegocioErro

# >>> Se um dia usar ORM real:
try:
    from contas.models import Usuario as UsuarioORM
    from contas.models import Familiar as FamiliarORM
    from contas.models import Terapeuta as TerapeutaORM
except Exception:
    UsuarioORM = FamiliarORM = TerapeutaORM = None

_ter_repo = TerapeutasRepoMemoria()
_pac_repo = PacientesRepoMemoria()
_fam_repo = FamiliaresRepoMemoria()
_serv = CadastroServico(_ter_repo, _pac_repo, _fam_repo)

def _handle_exceptions(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except RecursoNaoEncontrado as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ConflitoUnico as e:
            return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)
        except RegraNegocioErro as e:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return wrapper


class TerapeutaViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminClinica]

    @_handle_exceptions
    def list(self, request):
        objs = _ter_repo.listar()
        data = TerapeutaOutSerializer(objs, many=True).data
        return Response(data)

    @_handle_exceptions
    def retrieve(self, request, pk=None):
        obj = _ter_repo.obter(int(pk))
        return Response(TerapeutaOutSerializer(obj).data)

    @_handle_exceptions
    def create(self, request):
        s = TerapeutaInSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        obj = _serv.criar_terapeuta(**s.validated_data)
        return Response(TerapeutaOutSerializer(obj).data, status=status.HTTP_201_CREATED)

    @_handle_exceptions
    def partial_update(self, request, pk=None):
        payload = {k: v for k, v in request.data.items() if k in {"nome", "email", "ativo"}}
        obj = _serv.editar_terapeuta(int(pk), **payload)
        return Response(TerapeutaOutSerializer(obj).data)

    @_handle_exceptions
    def destroy(self, request, pk=None):
        _serv.excluir_terapeuta(int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)

class PacienteViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminClinica]

    @_handle_exceptions
    def list(self, request):
        objs = _pac_repo.listar()
        return Response(PacienteOutSerializer(objs, many=True).data)

    @_handle_exceptions
    def retrieve(self, request, pk=None):
        obj = _pac_repo.obter(int(pk))
        return Response(PacienteOutSerializer(obj).data)

    @_handle_exceptions
    def create(self, request):
        s = PacienteInSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        obj = _serv.criar_paciente(**s.validated_data)
        return Response(PacienteOutSerializer(obj).data, status=status.HTTP_201_CREATED)

    @_handle_exceptions
    def partial_update(self, request, pk=None):
        payload = {k: v for k, v in request.data.items() if k in {"nome", "ativo"}}
        obj = _serv.editar_paciente(int(pk), **payload)
        return Response(PacienteOutSerializer(obj).data)

    @_handle_exceptions
    def destroy(self, request, pk=None):
        _pac_repo.excluir(int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    @_handle_exceptions
    def transferencias(self, request, pk=None):
        s = TransferenciaInSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        obj = _serv.transferir_paciente(int(pk), s.validated_data["novo_terapeuta_id"])
        return Response(PacienteOutSerializer(obj).data, status=status.HTTP_200_OK)

class FamiliarViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminClinica]

    @_handle_exceptions
    def list(self, request):
        objs = _fam_repo.listar()
        return Response(FamiliarOutSerializer(objs, many=True).data)

    @_handle_exceptions
    def retrieve(self, request, pk=None):
        obj = _fam_repo.obter(int(pk))
        return Response(FamiliarOutSerializer(obj).data)

    @_handle_exceptions
    def create(self, request):
        s = FamiliarInSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        obj = _serv.criar_familiar(**s.validated_data)
        return Response(FamiliarOutSerializer(obj).data, status=status.HTTP_201_CREATED)

    @_handle_exceptions
    def partial_update(self, request, pk=None):
        payload = {k: v for k, v in request.data.items() if k in {"nome", "email", "ativo"}}
        obj = _serv.editar_familiar(int(pk), **payload)
        return Response(FamiliarOutSerializer(obj).data)

    @_handle_exceptions
    def destroy(self, request, pk=None):
        _fam_repo.excluir(int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)
