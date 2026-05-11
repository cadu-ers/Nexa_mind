from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ..dependencies import get_db
from ..schemas.flashcards import FlashcardCreate, FlashcardResposta, FlashcardResponse
from ..services.flashcard import criar_flashcard, listar_flashcards, listar_para_revisar, registrar_resposta, deletar_flashcard

router = APIRouter()

@router.post("/flashcards", response_model=FlashcardResponse, status_code=201)
def criar(material_id: UUID, flashcard: FlashcardCreate, db: Session = Depends(get_db)):
    return criar_flashcard(db, material_id, flashcard.pergunta, flashcard.resposta, flashcard.nivel_dificuldade)

@router.get("/flashcards", response_model=list[FlashcardResponse])
def listar(material_id: UUID, db: Session = Depends(get_db)):
    return listar_flashcards(db, material_id)

@router.get("/flashcards/revisar", response_model=list[FlashcardResponse])
def revisar(material_id: UUID, db: Session = Depends(get_db)):
    return listar_para_revisar(db, material_id)

@router.post("/flashcards/{flashcard_id}/resposta", response_model=FlashcardResponse)
def responder(flashcard_id: UUID, dados: FlashcardResposta, db: Session = Depends(get_db)):
    flashcard = registrar_resposta(db, flashcard_id, dados.acertou)
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard não encontrado")
    return flashcard

@router.delete("/flashcards/{flashcard_id}", status_code=204)
def deletar(flashcard_id: UUID, db: Session = Depends(get_db)):
    sucesso = deletar_flashcard(db, flashcard_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Flashcard não encontrado")