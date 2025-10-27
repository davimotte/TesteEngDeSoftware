from typing import Optional
from .entidades import Terapeuta, Paciente, Familiar
from .portas import ITerapeutasRepo, IPacientesRepo, IFamiliaresRepo
from .erros import RecursoNaoEncontrado, RegraNegocioErro, ConflitoUnico

class CadastroServico:
    def __init__(self, terapeutas: ITerapeutasRepo, pacientes: IPacientesRepo, familiares: IFamiliaresRepo):
        self.terapeutas = terapeutas
        self.pacientes = pacientes
        self.familiares = familiares

    # --- Terapeuta ---
    def criar_terapeuta(self, nome: str, email: str) -> Terapeuta:
        if self.terapeutas.existe_email(email):
            raise ConflitoUnico("E-mail de terapeuta já cadastrado.")
        novo = Terapeuta(id=0, nome=nome, email=email)
        return self.terapeutas.criar(novo)

    def editar_terapeuta(self, id_: int, nome: Optional[str]=None, email: Optional[str]=None, ativo: Optional[bool]=None) -> Terapeuta:
        t = self.terapeutas.obter(id_)
        if email and self.terapeutas.existe_email(email, ignorar_id=id_):
            raise ConflitoUnico("E-mail de terapeuta já cadastrado.")
        if nome is not None: t.nome = nome
        if email is not None: t.email = email
        if ativo is not None: t.ativo = ativo
        return self.terapeutas.atualizar(t)

    def excluir_terapeuta(self, id_: int) -> None:
        # Regra: não excluir se houver paciente ativo vinculado
        pacientes = [p for p in self.pacientes.listar() if p.terapeuta_id == id_ and p.ativo]
        if pacientes:
            raise RegraNegocioErro("Não é possível excluir terapeuta com pacientes ativos vinculados.")
        self.terapeutas.excluir(id_)

    # --- Paciente ---
    def criar_paciente(self, nome: str, terapeuta_id: Optional[int]=None) -> Paciente:
        if terapeuta_id is not None:
            _ = self.terapeutas.obter(terapeuta_id)  # valida existência
        novo = Paciente(id=0, nome=nome, terapeuta_id=terapeuta_id)
        return self.pacientes.criar(novo)

    def editar_paciente(self, id_: int, nome: Optional[str]=None, ativo: Optional[bool]=None) -> Paciente:
        p = self.pacientes.obter(id_)
        if nome is not None: p.nome = nome
        if ativo is not None: p.ativo = ativo
        return self.pacientes.atualizar(p)

    def transferir_paciente(self, paciente_id: int, novo_terapeuta_id: int) -> Paciente:
        p = self.pacientes.obter(paciente_id)
        _ = self.terapeutas.obter(novo_terapeuta_id)  # valida existência
        p.terapeuta_id = novo_terapeuta_id
        return self.pacientes.atualizar(p)

    # --- Familiar ---
    def criar_familiar(self, nome: str, email: str) -> Familiar:
        if self.familiares.existe_email(email):
            raise ConflitoUnico("E-mail de familiar já cadastrado.")
        novo = Familiar(id=0, nome=nome, email=email)
        return self.familiares.criar(novo)

    def editar_familiar(self, id_: int, nome: Optional[str]=None, email: Optional[str]=None, ativo: Optional[bool]=None) -> Familiar:
        f = self.familiares.obter(id_)
        if email and self.familiares.existe_email(email, ignorar_id=id_):
            raise ConflitoUnico("E-mail de familiar já cadastrado.")
        if nome is not None: f.nome = nome
        if email is not None: f.email = email
        if ativo is not None: f.ativo = ativo
        return self.familiares.atualizar(f)
