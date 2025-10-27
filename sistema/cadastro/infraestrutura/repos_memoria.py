from typing import Dict, List, Optional
from ..dominio.portas import ITerapeutasRepo, IPacientesRepo, IFamiliaresRepo
from ..dominio.entidades import Terapeuta, Paciente, Familiar
from ..dominio.erros import RecursoNaoEncontrado

class _BaseRepoMemoria:
    def __init__(self):
        self._db: Dict[int, object] = {}
        self._seq = 1

    def _next_id(self) -> int:
        v = self._seq
        self._seq += 1
        return v

    def _get(self, id_: int):
        if id_ not in self._db:
            raise RecursoNaoEncontrado("ID não encontrado.")
        return self._db[id_]

class TerapeutasRepoMemoria(_BaseRepoMemoria, ITerapeutasRepo):
    def criar(self, t: Terapeuta) -> Terapeuta:
        t.id = self._next_id()
        self._db[t.id] = t
        return t
    def obter(self, id_: int) -> Terapeuta:
        return self._get(id_)
    def listar(self) -> List[Terapeuta]:
        return list(self._db.values())
    def atualizar(self, t: Terapeuta) -> Terapeuta:
        self._db[t.id] = t
        return t
    def excluir(self, id_: int) -> None:
        _ = self._get(id_)
        del self._db[id_]
    def existe_email(self, email: str, ignorar_id: Optional[int]=None) -> bool:
        for obj in self._db.values():
            if obj.email.lower() == email.lower() and obj.id != (ignorar_id or 0):
                return True
        return False

class PacientesRepoMemoria(_BaseRepoMemoria, IPacientesRepo):
    def criar(self, p: Paciente) -> Paciente:
        p.id = self._next_id()
        self._db[p.id] = p
        return p
    def obter(self, id_: int) -> Paciente:
        return self._get(id_)
    def listar(self) -> List[Paciente]:
        return list(self._db.values())
    def atualizar(self, p: Paciente) -> Paciente:
        self._db[p.id] = p
        return p
    def excluir(self, id_: int) -> None:
        _ = self._get(id_)
        del self._db[id_]

class FamiliaresRepoMemoria(_BaseRepoMemoria, IFamiliaresRepo):
    def criar(self, f: Familiar) -> Familiar:
        f.id = self._next_id()
        self._db[f.id] = f
        return f
    def obter(self, id_: int) -> Familiar:
        return self._get(id_)
    def listar(self) -> List[Familiar]:
        return list(self._db.values())
    def atualizar(self, f: Familiar) -> Familiar:
        self._db[f.id] = f
        return f
    def excluir(self, id_: int) -> None:
        _ = self._get(id_)
        del self._db[id_]
    def existe_email(self, email: str, ignorar_id: Optional[int]=None) -> bool:
        for obj in self._db.values():
            if obj.email.lower() == email.lower() and obj.id != (ignorar_id or 0):
                return True
        return False
