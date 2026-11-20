"""Punto de entrada de Software FJ: menú y demostración de diez operaciones."""

from clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from sistema import SistemaGestion
from excepciones import SoftwareFJError, DatosInvalidosError
from logs import registrar_evento, registrar_error


def cargar_datos_demo(sistema):
    """Ejecuta más de diez operaciones para demostrar el funcionamiento."""
    print("\n========== DEMOSTRACIÓN DE SOFTWARE FJ ==========")

    # Operación 1: registro de cliente válido.
    try:
        sistema.registrar_cliente(
            Cliente("1001", "Carlos Pérez", "carlos@gmail.com", "3001234567")
        )
        print("1. Cliente Carlos registrado correctamente.")
    except SoftwareFJError as error:
        print(f"1. Error controlado: {error}")

    # Operación 2: registro inválido.
    try:
        sistema.registrar_cliente(
            Cliente("1002", "María López", "correo-invalido", "3007654321")
        )
    except SoftwareFJError as error:
        registrar_error(f"Prueba de cliente inválido: {error}")
        print(f"2. Cliente inválido detectado correctamente: {error}")

    # Operación 3: segundo cliente válido.
    try:
        sistema.registrar_cliente(
            Cliente("1003", "Ana Gómez", "ana@gmail.com", "3105556677")
        )
        print("3. Cliente Ana registrado correctamente.")
    except SoftwareFJError as error:
        print(f"3. Error controlado: {error}")

    # Operación 4: crear servicio de sala.
    try:
        sistema.agregar_servicio(
            ReservaSala("S01", "Sala de reuniones", 50000, 12)
        )
        print("4. Servicio de sala creado correctamente.")
    except SoftwareFJError as error:
        print(f"4. Error controlado: {error}")

    # Operación 5: intento de crear servicio inválido.
    try:
        sistema.agregar_servicio(
            ReservaSala("S02", "Sala inválida", -1000, 10)
        )
    except SoftwareFJError as error:
        registrar_error(f"Prueba de servicio inválido: {error}")
        print(f"5. Servicio inválido detectado correctamente: {error}")

    # Operación 6: crear servicio de alquiler de equipos.
    try:
        sistema.agregar_servicio(
            AlquilerEquipo("E01", "Proyector", 80000, 4)
        )
        print("6. Servicio de alquiler de equipos creado correctamente.")
    except SoftwareFJError as error:
        print(f"6. Error controlado: {error}")

    # Operación adicional: crear servicio de asesoría.
    try:
        sistema.agregar_servicio(
            AsesoriaEspecializada("A01", "Asesoría informática", 120000, "Tecnología")
        )
        print("Servicio de asesoría creado correctamente.")
    except SoftwareFJError as error:
        print(f"Error controlado: {error}")

    # Operación 7: crear reserva válida.
    try:
        reserva1 = sistema.crear_reserva("R001", "1001", "S01", 2, impuesto=19)
        print(f"7. Reserva creada: {reserva1}")
    except SoftwareFJError as error:
        print(f"7. Error controlado: {error}")

    # Operación 8: intentar crear reserva con duración negativa.
    try:
        sistema.crear_reserva("R002", "1001", "E01", -3)
    except SoftwareFJError as error:
        registrar_error(f"Prueba de reserva con duración inválida: {error}")
        print(f"8. Reserva inválida detectada correctamente: {error}")

    # Operación 9: confirmar reserva.
    try:
        total = sistema.buscar_reserva("R001").confirmar()
        print(f"9. Reserva confirmada. Total: ${total:.2f}")
    except SoftwareFJError as error:
        print(f"9. Error controlado: {error}")

    # Operación 10: procesar reserva.
    try:
        mensaje = sistema.buscar_reserva("R001").procesar()
        print(f"10. {mensaje}")
    except (SoftwareFJError, RuntimeError) as error:
        print(f"10. Error controlado: {error}")

    # Prueba adicional: cancelar dos veces para demostrar control de estado.
    try:
        reserva2 = sistema.crear_reserva("R003", "1003", "A01", 1)
        reserva2.cancelar()
        print("Prueba adicional: reserva cancelada.")
        reserva2.cancelar()
    except SoftwareFJError as error:
        registrar_error(f"Prueba de cancelación repetida: {error}")
        print(f"Prueba adicional: cancelación repetida controlada: {error}")

    print("\n========== RESUMEN DE RESERVAS ==========")
    for reserva in sistema.listar_reservas():
        print(reserva)
    print("\nLos eventos y errores se guardaron en registro_sistema.log.")
    print("========== FIN DE LA DEMOSTRACIÓN ==========\n")


def mostrar_menu():
    print("""
========= SOFTWARE FJ =========
1. Registrar cliente
2. Registrar servicio
3. Listar clientes
4. Listar servicios
5. Crear reserva
6. Confirmar reserva
7. Cancelar reserva
8. Procesar reserva
9. Listar reservas
10. Ejecutar demostración de pruebas
0. Salir
""")


def ejecutar_menu():
    sistema = SistemaGestion()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                cliente = Cliente(
                    input("Identificación: "),
                    input("Nombre completo: "),
                    input("Correo electrónico: "),
                    input("Teléfono: ")
                )
                sistema.registrar_cliente(cliente)
                print("Cliente registrado correctamente.")

            elif opcion == "2":
                print("Tipo: 1. Sala  2. Equipo  3. Asesoría")
                tipo = input("Seleccione el tipo: ").strip()
                codigo = input("Código del servicio: ")
                nombre = input("Nombre del servicio: ")
                precio = float(input("Precio base: "))

                if tipo == "1":
                    capacidad = int(input("Capacidad de la sala: "))
                    servicio = ReservaSala(codigo, nombre, precio, capacidad)
                elif tipo == "2":
                    unidades = int(input("Unidades disponibles: "))
                    servicio = AlquilerEquipo(codigo, nombre, precio, unidades)
                elif tipo == "3":
                    especialidad = input("Especialidad: ")
                    servicio = AsesoriaEspecializada(
                        codigo, nombre, precio, especialidad
                    )
                else:
                    raise DatosInvalidosError("Tipo de servicio no reconocido.")

                sistema.agregar_servicio(servicio)
                print("Servicio registrado correctamente.")

            elif opcion == "3":
                for cliente in sistema.listar_clientes():
                    print(cliente)

            elif opcion == "4":
                for servicio in sistema.listar_servicios():
                    print(servicio.describir())

            elif opcion == "5":
                codigo = input("Código de reserva: ")
                identificacion = input("Identificación del cliente: ")
                codigo_servicio = input("Código del servicio: ")
                duracion = float(input("Duración (horas, días o sesiones): "))
                impuesto = float(input("Impuesto (%) [0 si no aplica]: ") or 0)
                descuento = float(input("Descuento (%) [0 si no aplica]: ") or 0)
                reserva = sistema.crear_reserva(
                    codigo, identificacion, codigo_servicio,
                    duracion, impuesto, descuento
                )
                print(f"Reserva creada: {reserva}")

            elif opcion == "6":
                codigo = input("Código de reserva: ")
                total = sistema.buscar_reserva(codigo).confirmar()
                print(f"Reserva confirmada. Total: ${total:.2f}")

            elif opcion == "7":
                codigo = input("Código de reserva: ")
                sistema.buscar_reserva(codigo).cancelar()
                print("Reserva cancelada correctamente.")

            elif opcion == "8":
                codigo = input("Código de reserva: ")
                print(sistema.buscar_reserva(codigo).procesar())

            elif opcion == "9":
                for reserva in sistema.listar_reservas():
                    print(reserva)

            elif opcion == "10":
                cargar_datos_demo(sistema)

            elif opcion == "0":
                registrar_evento("El usuario cerró el sistema.")
                print("Gracias por utilizar Software FJ.")
                break

            else:
                raise DatosInvalidosError("Seleccione una opción del menú entre 0 y 10.")

        except (SoftwareFJError, ValueError) as error:
            registrar_error(f"Error controlado en el menú: {error}")
            print(f"Atención: {error}")
        except Exception as error:
            registrar_error(f"Error inesperado en el menú: {error}")
            print("Ocurrió un error inesperado. El sistema continuará funcionando.")


if __name__ == "__main__":
    print("Bienvenido al Sistema Integral de Gestión de Software FJ.")
    print("Escriba DEMO como argumento para ejecutar las pruebas automáticamente.")
    import sys
    if len(sys.argv) > 1 and sys.argv[1].upper() == "DEMO":
        cargar_datos_demo(SistemaGestion())
    else:
        ejecutar_menu()
