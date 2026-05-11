from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ..dependencies import get_db
from ..schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from ..services.user_service import criar_usuario, buscar_usuario, atualizar_usuario, deletar_usuario

router = APIRouter()

@router.post("/usuarios", response_model=UsuarioResponse, status_code=201)
def criar(user: UsuarioCreate, db: Session = Depends(get_db)):
    return criar_usuario(db, user.nome, user.email, user.senha, user.data_nascimento, user.curso, user.instituicao)

@router.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def buscar(usuario_id: UUID, db: Session = Depends(get_db)):
    usuario = buscar_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def atualizar(usuario_id: UUID, dados: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = atualizar_usuario(db, usuario_id, **dados.model_dump(exclude_none=True))
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.delete("/usuarios/{usuario_id}", status_code=204)
def deletar(usuario_id: UUID, db: Session = Depends(get_db)):
    sucesso = deletar_usuario(db, usuario_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")