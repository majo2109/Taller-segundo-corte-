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

@router.put("/{entrenador_id}")
def actualizar_entrenador(entrenador_id: int, entrenador_actualizado: Entrenador, session: Session = Depends(get_session)):
    entrenador = session.get(Entrenador, entrenador_id)
    if not entrenador or not entrenador.estado:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")

    # Actualizar los campos del entrenador existente con los datos del body
    entrenador.nombre = entrenador_actualizado.nombre
    entrenador.apellido = entrenador_actualizado.apellido
    # Asume que Entrenador tiene más campos, actualiza aquí los que correspondan
    # Ejemplo: entrenador.especialidad = entrenador_actualizado.especialidad
    
    session.add(entrenador)
    session.commit()
    session.refresh(entrenador)
    return entrenador

@router.delete("/{entrenador_id}")
def eliminar_entrenador(entrenador_id: int, session: Session = Depends(get_session)):
    entrenador = session.get(Entrenador, entrenador_id)
    if not entrenador:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    entrenador.estado = False
    session.add(entrenador)
    session.commit()
    return {"mensaje": "Entrenador eliminado (borrado lógico)"}