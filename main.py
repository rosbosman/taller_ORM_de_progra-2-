from modelo import crear_tablas
from operaciones import(
    cancelar_reserva,
    consultar_reserva,
    consultar_salas,
    insertar_salas,
    registrar_reserva,
)

mensaje = """
===== RESERVAS DE SALAS =====
1.registrar salas
2.consultar_salas
3.registrar_reserva
4.consultar_reservas
5.cancelar_reserva
0.salir
"""
def leer_entero(mensaje:str) ->int|None:

  try:
    return int(input(mensaje).strip())
  except ValueError:
    print("ERROR desbes ingresar un numero entero")
  return None


def opcion_registrar_sala() -> None:
    nombre = input("Nombre de la sala: ")
    capacidad = leer_entero("Capacidad: ")
    if capacidad is None:
        return
    nueva_id = insertar_salas(nombre, capacidad)
    print(f"Sala registrada con ID {nueva_id}.")

def opcion_registrar_reserva() -> None:
    estudiante = input("Nombre del estudiante: ")
    sala_id = leer_entero("ID de la sala: ")
    if sala_id is None:
        return
    fecha = input("Fecha (AAAA-MM-DD): ").strip()
    nueva_id = registrar_reserva(estudiante, sala_id, fecha)
    print(f"Reserva registrada con ID {nueva_id}.")

def opcion_cancelar_reserva() -> None:
    id_reserva = leer_entero("ID de la reserva a cancelar: ")
    if id_reserva is None:
        return
    cancelar_reserva(id_reserva)
    print("Reserva cancelada. La sala quedó disponible.")

acciones = {
    "1": opcion_registrar_sala,
    "2": consultar_salas,
    "3": opcion_registrar_reserva,
    "4": consultar_reserva,
    "5": opcion_cancelar_reserva,
    "0": exit,
}
def main() -> None:
    crear_tablas()
    while True:
        print(mensaje)
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "0":
            print("Hasta luego.")
            break
        accion = acciones.get(opcion)
        if accion is None:
            print("Opción no válida. Elija una opción del menú.")
            continue
        try:
            accion()
        except ValueError as error:  # solicitudes rechazadas por las validaciones
            print(f"Operación rechazada: {error}")


if __name__ == "__main__":
    main()


