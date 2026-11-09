from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from modelo import Reserva, Sala, SessionLocal

def insertar_salas(nombre: str, capacidad: int) -> int:
    #Registra una sala nueva (disponible=True). Devuelve el id asignada
    nombre = (nombre or "").strip()
    if not nombre:
        raise ValueError("El nombre de la sala no puede estar vacío.")
    if len(nombre) > 100:
        raise ValueError("El nombre de la sala no puede superar los 100 caracteres.")
    if capacidad <= 0:
        raise ValueError("La capacidad debe ser mayor que cero.")

    with SessionLocal.begin() as session: 
        sala = Sala(nombre=nombre, capacidad=capacidad)  
        session.add(sala)
        session.flush()  
        nueva_id = sala.id
    return nueva_id

def consultar_salas() -> list[tuple]:
    #Muestra todas las salas y devuelve [(id, nombre, capacidad, disponible), ...].
    with SessionLocal() as session:
        salas = session.scalars(select(Sala).order_by(Sala.id)).all()
        filas = [(s.id, s.nombre, s.capacidad, s.disponible) for s in salas]

    if not filas:
        print("No hay salas registradas.")
        return filas

    print(f"{'ID':<4} {'NOMBRE':<25} {'CAPACIDAD':<10} DISPONIBLE")
    for id_, nombre, capacidad, disponible in filas:
        print(f"{id_:<4} {nombre:<25} {capacidad:<10} {'Sí' if disponible else 'No'}")
    return filas

def registrar_reserva(estudiante: str, sala_id: int, fecha: str) -> int:
    # Crea la reserva y marca la sala como no disponible, en una transacción
    estudiante = (estudiante or "").strip()
    if not estudiante:
        raise ValueError("El nombre del estudiante no puede estar vacío.")
    if len(estudiante) > 100:
        raise ValueError("El nombre del estudiante no puede superar los 100 caracteres.")
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except (TypeError, ValueError):
        raise ValueError("La fecha debe tener el formato AAAA-MM-DD (ej: 2026-11-15).")

    with SessionLocal.begin() as session:
        sala = session.get(Sala, sala_id)  
        if sala is None:
            raise ValueError(f"La sala con ID {sala_id} no existe.")
        if not sala.disponible:
            raise ValueError(f"La sala '{sala.nombre}' no está disponible.")

        reserva = Reserva(estudiante=estudiante, sala=sala, fecha=fecha)
        session.add(reserva)
        sala.disponible = False  
        session.flush()
        nueva_id = reserva.id
    return nueva_id

def consultar_reserva() -> list[tuple]:
   
    with SessionLocal() as session:
        consulta = (
            select(Reserva)
            .options(joinedload(Reserva.sala)) 
            .order_by(Reserva.id)
        )
        reservas = session.scalars(consulta).all()
        filas = [(r.id, r.estudiante, r.sala.nombre, r.fecha) for r in reservas]

    if not filas:
        print("No hay reservas registradas.")
        return filas

    print(f"{'ID':<4} {'ESTUDIANTE':<25} {'SALA':<25} FECHA")
    for id_, estudiante, sala, fecha in filas:
        print(f"{id_:<4} {estudiante:<25} {sala:<25} {fecha}")
    return filas

def cancelar_reserva(id_reserva: int) -> None:
    
    with SessionLocal.begin() as session:
        reserva = session.get(Reserva, id_reserva)
        if reserva is None:
            raise ValueError(f"La reserva con ID {id_reserva} no existe.")

        reserva.sala.disponible = True  
        session.delete(reserva)