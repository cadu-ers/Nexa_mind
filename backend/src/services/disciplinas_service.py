from sqlalchemy.orm import Session
from ..models.disciplina import Disciplina
import uuid

def criar_disciplina(db: Session, usuario_id: uuid.UUID, nome: str, semestre=None, professor=None, cor=None, descricao=None):
    disciplina = Disciplina(
        usuario_id=usuario_id,
        nome=nome,
        semestre=semestre,
        professor=professor,
        cor=cor,
        descricao=descricao
    )
    db.add(disciplina)
    db.commit()
    db.refresh(disciplina)
    return disciplina

def listar_disciplinas(db: Session, usuario_id: uuid.UUID):
    return db.query(Disciplina).filter(Disciplina.usuario_id == usuario_id).all()

def buscar_disciplina(db: Session, disciplina_id: uuid.UUID, usuario_id: uuid.UUID):
    return db.query(Disciplina).filter(
        Disciplina.id == disciplina_id,
        Disciplina.usuario_id == usuario_id
    ).first()

def atualizar_disciplina(db: Session, disciplina_id: uuid.UUID, usuario_id: uuid.UUID, **dados):
    disciplina = buscar_disciplina(db, disciplina_id, usuario_id)
    if not disciplina:
        return None
    for campo, valor in dados.items():
        setattr(disciplina, campo, valor)
    db.commit()
    db.refresh(disciplina)
    return disciplina

def deletar_disciplina(db: Session, disciplina_id: uuid.UUID, usuario_id: uuid.UUID):
    disciplina = buscar_disciplina(db, disciplina_id, usuario_id)
    if not disciplina:
        return False
    db.delete(disciplina)
    db.commit()
    return True