from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Terapeuta:
    id: int
    nome: str
    email: str
    ativo: bool = True

@dataclass
class Familiar:
    id: int
    nome: str
    email: str
    ativo: bool = True

@dataclass
class Paciente:
    id: int
    nome: str
    terapeuta_id: Optional[int] = None
    familiares_ids: List[int] = field(default_factory=list)
    ativo: bool = True
