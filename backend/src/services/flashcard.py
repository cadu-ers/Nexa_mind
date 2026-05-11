from sqlalchemy.orm import Session
from ..models.flashcard import Flashcard
import uuid
from datetime import datetime, timedelta

def _calcular_proxima_revisao(acertos: int, erros: int) -> datetime:
    if erros > acertos:
        dias = 1
    elif acertos <= 2:
        dias = 3
    elif acertos <= 5:
        dias = 7
    else:
        dias = 14
    return datetime.utcnow() + timedelta(days=dias)

def criar_flashcard(db: Session, material_id: uuid.UUID, pergunta: str, resposta: str, nivel_dificuldade: str = "medio"):
    flashcard = Flashcard(
        material_id=material_id,
        pergunta=pergunta,
        resposta=resposta,
        nivel_dificuldade=nivel_dificuldade,
        proxima_revisao=datetime.utcnow() + timedelta(days=1)
    )
    db.add(flashcard)
    db.commit()
    db.refresh(flashcard)
    return flashcard

def listar_flashcards(db: Session, material_id: uuid.UUID):
    return db.query(Flashcard).filter(Flashcard.material_id == material_id).all()

def listar_para_revisar(db: Session, material_id: uuid.UUID):
    return db.query(Flashcard).filter(
        Flashcard.material_id == material_id,
        Flashcard.proxima_revisao <= datetime.utcnow()
    ).all()

def registrar_resposta(db: Session, flashcard_id: uuid.UUID, acertou: bool):
    flashcard = db.query(Flashcard).filter(Flashcard.id == flashcard_id).first()
    if not flashcard:
        return None

    if acertou:
        flashcard.acertos += 1
    else:
        flashcard.erros += 1

    flashcard.ultima_revisao = datetime.utcnow()
    flashcard.proxima_revisao = _calcular_proxima_revisao(flashcard.acertos, flashcard.erros)

    db.commit()
    db.refresh(flashcard)
    return flashcard

def deletar_flashcard(db: Session, flashcard_id: uuid.UUID):
    flashcard = db.query(Flashcard).filter(Flashcard.id == flashcard_id).first()
    if not flashcard:
        return False
    db.delete(flashcard)
    db.commit()
    return True