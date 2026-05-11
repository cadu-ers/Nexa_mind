from sqlalchemy.orm import Session
from ..models.material import Material
import uuid
import os

def criar_material(
    db: Session,
    disciplina_id: uuid.UUID,
    titulo: str,
    tipo_arquivo: str,
    caminho_arquivo: str,
    tamanho_bytes: int = None,
    paginas: int = None,
    idioma: str = "pt"
):
    material = Material(
        disciplina_id=disciplina_id,
        titulo=titulo,
        tipo_arquivo=tipo_arquivo,
        caminho_arquivo=caminho_arquivo,
        tamanho_bytes=tamanho_bytes,
        paginas=paginas,
        idioma=idioma,
        processado=False
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return material

def listar_materiais(db: Session, disciplina_id: uuid.UUID):
    return db.query(Material).filter(Material.disciplina_id == disciplina_id).all()

def buscar_material(db: Session, material_id: uuid.UUID):
    return db.query(Material).filter(Material.id == material_id).first()

def marcar_como_processado(db: Session, material_id: uuid.UUID):
    material = buscar_material(db, material_id)
    if not material:
        return None
    material.processado = True
    db.commit()
    db.refresh(material)
    return material

def deletar_material(db: Session, material_id: uuid.UUID):
    material = buscar_material(db, material_id)
    if not material:
        return False
    # Remove o arquivo físico do servidor também
    if os.path.exists(material.caminho_arquivo):
        os.remove(material.caminho_arquivo)
    db.delete(material)
    db.commit()
    return True