from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ..dependencies import get_db
from ..schemas.disciplina import DisciplinaCreate, DisciplinaUpdate, DisciplinaResponse
from ..services.disciplina import criar_disciplina, listar_disciplinas, buscar_disciplina, atualizar_disciplina, deletar_disciplina

router = APIRouter()

@router.post("/disciplinas", response_model=DisciplinaResponse, status_code=201)
def criar(disciplina: DisciplinaCreate, usuario_id: UUID, db: Session = Depends(get_db)):
    return criar_disciplina(db, usuario_id, disciplina.nome, disciplina.semestre, disciplina.professor, disciplina.cor, disciplina.descricao)

@router.get("/disciplinas", response_model=list[DisciplinaResponse])
def listar(usuario_id: UUID, db: Session = Depends(get_db)):
    return listar_disciplinas(db, usuario_id)

@router.get("/disciplinas/{disciplina_id}", response_model=DisciplinaResponse)
def buscar(disciplina_id: UUID, usuario_id: UUID, db: Session = Depends(get_db)):
    disciplina = buscar_disciplina(db, disciplina_id, usuario_id)
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return disciplina

@router.put("/disciplinas/{disciplina_id}", response_model=DisciplinaResponse)
def atualizar(disciplina_id: UUID, usuario_id: UUID, dados: DisciplinaUpdate, db: Session = Depends(get_db)):
    disciplina = atualizar_disciplina(db, disciplina_id, usuario_id, **dados.model_dump(exclude_none=True))
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return disciplina

@router.delete("/disciplinas/{disciplina_id}", status_code=204)
def deletar(disciplina_id: UUID, usuario_id: UUID, db: Session = Depends(get_db)):
    sucesso = deletar_disciplina(db, disciplina_id, usuario_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")