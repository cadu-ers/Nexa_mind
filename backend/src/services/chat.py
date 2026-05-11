from sqlalchemy.orm import Session
from ..models.chat import SessaoChat
import uuid

def criar_sessao(db: Session, usuario_id: uuid.UUID, disciplina_id: uuid.UUID = None, titulo: str = None):
    sessao = SessaoChat(
        usuario_id=usuario_id,
        disciplina_id=disciplina_id,
        titulo=titulo
    )
    db.add(sessao)
    db.commit()
    db.refresh(sessao)
    return sessao

def listar_sessoes(db: Session, usuario_id: uuid.UUID):
    return db.query(SessaoChat).filter(
        SessaoChat.usuario_id == usuario_id
    ).order_by(SessaoChat.iniciado_em.desc()).all()

def buscar_sessao(db: Session, sessao_id: uuid.UUID, usuario_id: uuid.UUID):
    return db.query(SessaoChat).filter(
        SessaoChat.id == sessao_id,
        SessaoChat.usuario_id == usuario_id
    ).first()

def atualizar_titulo(db: Session, sessao_id: uuid.UUID, usuario_id: uuid.UUID, titulo: str):
    sessao = buscar_sessao(db, sessao_id, usuario_id)
    if not sessao:
        return None
    sessao.titulo = titulo
    db.commit()
    db.refresh(sessao)
    return sessao

def deletar_sessao(db: Session, sessao_id: uuid.UUID, usuario_id: uuid.UUID):
    sessao = buscar_sessao(db, sessao_id, usuario_id)
    if not sessao:
        return False
    db.delete(sessao)
    db.commit()
    return True