from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from uuid import UUID
from datetime import datetime

class ResumoCreate(BaseModel):
    conteudo: str = Field(min_length=1)

    model_config = ConfigDict(extra="forbid")

class ResumoResponse(BaseModel):
    id: UUID
    material_id: UUID
    conteudo: str
    gerado_em: datetime

    model_config = ConfigDict(from_attributes=True)