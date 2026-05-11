from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class MaterialCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=300)
    tipo_arquivo: str
    caminho_arquivo: str
    tamanho_bytes: Optional[int] = None
    paginas: Optional[int] = None
    idioma: str = "pt"

    model_config = ConfigDict(extra="forbid")

class MaterialResponse(BaseModel):
    id: UUID
    disciplina_id: UUID
    titulo: str
    tipo_arquivo: str
    caminho_arquivo: str
    tamanho_bytes: Optional[int] = None
    paginas: Optional[int] = None
    idioma: str
    processado: bool
    data_upload: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)