from sqlalchemy.orm import Session
from ..models.resumo import Resumo
import uuid

def salvar_resumo(db: Session, material_id: uuid.UUID, conteudo: str):
    resumo = Resumo(
        material_id=material_id,
        conteudo=conteudo
    )
    db.add(resumo)
    db.commit()
    db.refresh(resumo)
    return resumo

def buscar_resumo(db: Session, material_id: uuid.UUID):
    return db.query(Resumo).filter(
        Resumo.material_id == material_id
    ).first()

def atualizar_resumo(db: Session, material_id: uuid.UUID, novo_conteudo: str):
    resumo = buscar_resumo(db, material_id)
    if not resumo:
        return salvar_resumo(db, material_id, novo_conteudo)
    resumo.conteudo = novo_conteudo
    db.commit()
    db.refresh(resumo)
    return resumo

def deletar_resumo(db: Session, material_id: uuid.UUID):
    resumo = buscar_resumo(db, material_id)
    if not resumo:
        return False
    db.delete(resumo)
    db.commit()
    return True