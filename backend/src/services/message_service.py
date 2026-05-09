from sqlalchemy.orm import Session
from ..models.message import MensagemChat
import uuid

def salvar_mensagem(db: Session, sessao_id: uuid.UUID, papel: str, conteudo: str):
    mensagem = MensagemChat(
        sessao_id=sessao_id,
        papel=papel,
        conteudo=conteudo
    )
    db.add(mensagem)
    db.commit()
    db.refresh(mensagem)
    return mensagem

def listar_mensagens(db: Session, sessao_id: uuid.UUID):
    return db.query(MensagemChat).filter(
        MensagemChat.sessao_id == sessao_id
    ).order_by(MensagemChat.enviado_em.asc()).all()

def buscar_historico_para_ia(db: Session, sessao_id: uuid.UUID, limite: int = 20):
    """Retorna as últimas mensagens formatadas para enviar à IA."""
    mensagens = db.query(MensagemChat).filter(
        MensagemChat.sessao_id == sessao_id
    ).order_by(MensagemChat.enviado_em.desc()).limit(limite).all()

    return [
        {"role": papel_para_role(m.papel), "content": m.conteudo}
        for m in reversed(mensagens)
    ]

def papel_para_role(papel: str) -> str:
    mapa = {
        "usuario": "user",
        "assistente": "assistant",
        "sistema": "system"
    }
    return mapa.get(papel, "user")