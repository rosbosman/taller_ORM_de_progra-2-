from pathlib import Path

from sqlalchemy import CheckConstraint, ForeignKey, String, create_engine, event
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
RUTA_DB = Path(__file__).with_name("reservas.db")     

engine = create_engine(f"sqlite:///{RUTA_DB}")
@event.listens_for(engine, "connect")
def activar_claves_foraneas(dbapi_conn,_record):
     #SQLite no valida claves foraneas por defecto: se activa en cada conexion
    dbapi_conn.execute("PRAGMA foreign_keys=ON")

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class Sala(Base):
    __tablename__ = "salas"
    __table_args__ = (CheckConstraint("capacidad > 0", name="ck_sala_capacidad"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    capacidad: Mapped[int] = mapped_column(nullable=False)
    disponible: Mapped[bool] = mapped_column(default=True, nullable=False)

    
    reservas: Mapped[list["Reserva"]] = relationship(
        back_populates="sala", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Sala(id={self.id}, nombre={self.nombre!r}, capacidad={self.capacidad})"

class Reserva(Base):
    __tablename__ = "reservas"

    id: Mapped[int] = mapped_column(primary_key=True)
    estudiante: Mapped[str] = mapped_column(String(100), nullable=False)
    sala_id: Mapped[int] = mapped_column(ForeignKey("salas.id"), nullable=False)
    fecha: Mapped[str] = mapped_column(String(10), nullable=False) 

   
    sala: Mapped["Sala"] = relationship(back_populates="reservas")

    def __repr__(self) -> str:
        return f"Reserva(id={self.id}, estudiante={self.estudiante!r}, sala_id={self.sala_id}, fecha={self.fecha})"

def crear_tablas():
     #Crea las tablas en la base de datos
    Base.metadata.create_all(engine)




    