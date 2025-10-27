from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Deportista
from db import get_session

router = APIRouter(prefix="/deportistas", tags=["Deportistas"])

@router.post("/")
def crear_deportista(deportista: Deportista, session: Session = Depends(get_session)):
    session.add(deportista)
    session.commit()
    session.refresh(deportista)
    return deportista

@router.get("/")
def listar_deportistas(session: Session = Depends(get_session)):
    return session.exec(select(Deportista).where(Deportista.estado == True)).all()

@router.get("/{deportista_id}")
def obtener_deportista(deportista_id: int, session: Session = Depends(get_session)):
    deportista = session.get(Deportista, deportista_id)
    if not deportista or not deportista.estado:
        raise HTTPException(status_code=404, detail="Deportista no encontrado")
    return deportista

@router.put("/{deportista_id}")
def actualizar_deportista(deportista_id: int, deportista_actualizado: Deportista, session: Session = Depends(get_session)):
    deportista = session.get(Deportista, deportista_id)
    if not deportista or not deportista.estado:
        raise HTTPException(status_code=404, detail="Deportista no encontrado")

    # Actualizar los campos del deportista existente con los datos del body
    deportista.nombre = deportista_actualizado.nombre
    deportista.apellido = deportista_actualizado.apellido
    # Asume que Deportista tiene más campos, actualiza aquí los que correspondan
    # Ejemplo: deportista.otro_campo = deportista_actualizado.otro_campo
    
    session.add(deportista)
    session.commit()
    session.refresh(deportista)
    return deportista

@router.delete("/{deportista_id}")
def eliminar_deportista(deportista_id: int, session: Session = Depends(get_session)):
    deportista = session.get(Deportista, deportista_id)
    if not deportista:
        raise HTTPException(status_code=404, detail="No existe el deportista")
    deportista.estado = False
    session.add(deportista)
    session.commit()
    return {"mensaje": "Deportista eliminado (borrado lógico)"}