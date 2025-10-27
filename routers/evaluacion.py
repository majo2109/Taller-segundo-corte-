from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Evaluacion
from db import get_session

router = APIRouter(prefix="/evaluacion", tags=["Evaluacion"])

@router.post("/")
def crear_evaluacion(evaluacion: Evaluacion, session: Session = Depends(get_session)):
    session.add(evaluacion)
    session.commit()
    session.refresh(evaluacion)
    return evaluacion

@router.get("/")
def listar_evaluacion(session: Session = Depends(get_session)):
    return session.exec(select(Evaluacion).where(Evaluacion.estado == True)).all()

@router.delete("/{evaluacion_id}")
def eliminar_evaluacion(evaluacion_id: int, session: Session = Depends(get_session)):
    evaluacion = session.get(Evaluacion, evaluacion_id)
    if not evaluacion:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    evaluacion.estado = False
    session.add(evaluacion)
    session.commit()
    return {"mensaje": "Evaluación eliminada (borrado lógico)"}
