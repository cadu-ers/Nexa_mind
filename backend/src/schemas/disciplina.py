from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class DisciplinaCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=200)
    semestre: Optional[str] = Field(None, max_length=20)
    professor: Optional[str] = Field(None, max_length=150)
    cor: Optional[str] = Field(None, max_length=7)
    descricao: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

class DisciplinaUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=200)
    semestre: Optional[str] = Field(None, max_length=20)
    professor: Optional[str] = Field(None, max_length=150)
    cor: Optional[str] = Field(None, max_length=7)
    descricao: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

class DisciplinaResponse(BaseModel):
    id: UUID
    usuario_id: UUID
    nome: str
    semestre: Optional[str] = None
    professor: Optional[str] = None
    cor: Optional[str] = None
    descricao: Optional[str] = None
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)