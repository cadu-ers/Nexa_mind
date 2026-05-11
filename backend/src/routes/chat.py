from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ..dependencies import get_db
from ..schemas.chat import SessaoCreate, SessaoTituloUpdate, MensagemCreate, MensagemResponse, SessaoResponse
from ..services.chat import criar_sessao, listar_sessoes, buscar_sessao, atualizar_titulo, deletar_sessao
from ..services.mensagem import salvar_mensagem, listar_mensagens

router = APIRouter()

# --- Sessões ---

@router.post("/sessoes", response_model=SessaoResponse, status_code=201)
def criar(usuario_id: UUID, sessao: SessaoCreate, db: Session = Depends(get_db)):
    return criar_sessao(db, usuario_id, sessao.disciplina_id, sessao.titulo)

@router.get("/sessoes", response_model=list[SessaoResponse])
def listar(usuario_id: UUID, db: Session = Depends(get_db)):
    return listar_sessoes(db, usuario_id)

@router.get("/sessoes/{sessao_id}", response_model=SessaoResponse)
def buscar(sessao_id: UUID, usuario_id: UUID, db: Session = Depends(get_db)):
    sessao = buscar_sessao(db, sessao_id, usuario_id)
    if not sessao:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    return sessao

@router.patch("/sessoes/{sessao_id}/titulo", response_model=SessaoResponse)
def atualizar(sessao_id: UUID, usuario_id: UUID, dados: SessaoTituloUpdate, db: Session = Depends(get_db)):
    sessao = atualizar_titulo(db, sessao_id, usuario_id, dados.titulo)
    if not sessao:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    return sessao

@router.delete("/sessoes/{sessao_id}", status_code=204)
def deletar(sessao_id: UUID, usuario_id: UUID, db: Session = Depends(get_db)):
    sucesso = deletar_sessao(db, sessao_id, usuario_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

# --- Mensagens ---

@router.post("/sessoes/{sessao_id}/mensagens", response_model=MensagemResponse, status_code=201)
def enviar_mensagem(sessao_id: UUID, mensagem: MensagemCreate, db: Session = Depends(get_db)):
    return salvar_mensagem(db, sessao_id, "usuario", mensagem.conteudo)

@router.get("/sessoes/{sessao_id}/mensagens", response_model=list[MensagemResponse])
def listar_mensagens_sessao(sessao_id: UUID, db: Session = Depends(get_db)):
    return listar_mensagens(db, sessao_id)