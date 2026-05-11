from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class FlashcardCreate(BaseModel):
    pergunta: str = Field(min_length=1)
    resposta: str = Field(min_length=1)
    nivel_dificuldade: Optional[str] = "medio"

    model_config = ConfigDict(extra="forbid")

class FlashcardResposta(BaseModel):
    acertou: bool

    model_config = ConfigDict(extra="forbid")

class FlashcardResponse(BaseModel):
    id: UUID
    material_id: UUID
    pergunta: str
    resposta: str
    nivel_dificuldade: str
    acertos: int
    erros: int
    ultima_revisao: Optional[datetime] = None
    proxima_revisao: Optional[datetime] = None
    gerado_em: datetime

    model_config = ConfigDict(from_attributes=True)