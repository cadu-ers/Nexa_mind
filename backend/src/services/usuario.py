from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..models.user import Usuario
import uuid

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def criar_usuario(
    db: Session,
    nome: str,
    email: str,
    senha: str,
    data_nascimento=None,
    curso=None,
    instituicao=None
):
    senha_hash = pwd.hash(senha)
    usuario = Usuario(
        nome=nome,
        email=email,
        senha_hash=senha_hash,
        data_nascimento=data_nascimento,
        curso=curso,
        instituicao=instituicao
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def buscar_usuario(db: Session, usuario_id: uuid.UUID):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def atualizar_usuario(db: Session, usuario_id: uuid.UUID, **dados):
    usuario = buscar_usuario(db, usuario_id)
    if not usuario:
        return None
    for campo, valor in dados.items():
        setattr(usuario, campo, valor)
    db.commit()
    db.refresh(usuario)
    return usuario

def deletar_usuario(db: Session, usuario_id: uuid.UUID):
    usuario = buscar_usuario(db, usuario_id)
    if not usuario:
        return False
    db.delete(usuario)
    db.commit()
    return True