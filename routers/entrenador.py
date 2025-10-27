from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Entrenador
from db import get_session

router = APIRouter(prefix="/entrenadores", tags=["Entrenadores"])

@router.post("/")
def crear_entrenador(entrenador: Entrenador, session: Session = Depends(get_session)):
    session.add(entrenador)
    session.commit()
    session.refresh(entrenador)
    return entrenador

@router.get("/")
def listar_entrenadores(session: Session = Depends(get_session)):
    return session.exec(select(Entrenador).where(Entrenador.estado == True)).all()

@router.delete("/{entrenador_id}")
def eliminar_entrenador(entrenador_id: int, session: Session = Depends(get_session)):
    entrenador = session.get(Entrenador, entrenador_id)
    if not entrenador:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    entrenador.estado = False
    session.add(entrenador)
    session.commit()
    return {"mensaje": "Entrenador eliminado (borrado lógico)"}
