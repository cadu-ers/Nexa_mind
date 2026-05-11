from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ..dependencies import get_db
from ..schemas.material import MaterialCreate, MaterialResponse
from ..services.material import criar_material, listar_materiais, buscar_material, marcar_como_processado, deletar_material

router = APIRouter()

@router.post("/materiais", response_model=MaterialResponse, status_code=201)
def criar(disciplina_id: UUID, material: MaterialCreate, db: Session = Depends(get_db)):
    return criar_material(
        db,
        disciplina_id,
        material.titulo,
        material.tipo_arquivo,
        material.caminho_arquivo,
        material.tamanho_bytes,
        material.paginas,
        material.idioma
    )

@router.get("/materiais", response_model=list[MaterialResponse])
def listar(disciplina_id: UUID, db: Session = Depends(get_db)):
    return listar_materiais(db, disciplina_id)

@router.get("/materiais/{material_id}", response_model=MaterialResponse)
def buscar(material_id: UUID, db: Session = Depends(get_db)):
    material = buscar_material(db, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    return material

@router.patch("/materiais/{material_id}/processado", response_model=MaterialResponse)
def processar(material_id: UUID, db: Session = Depends(get_db)):
    material = marcar_como_processado(db, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    return material

@router.delete("/materiais/{material_id}", status_code=204)
def deletar(material_id: UUID, db: Session = Depends(get_db)):
    sucesso = deletar_material(db, material_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Material não encontrado")