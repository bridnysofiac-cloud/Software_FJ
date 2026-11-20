"""Gestión de reservas, estados y procesamiento controlado."""

from datetime import datetime
from excepciones import (
    DatosInvalidosError,
    EstadoReservaError,
    ServicioNoDisponibleError,
)
from logs import registrar_evento, registrar_error


class Reserva:
    """Relaciona un cliente con un servicio, una duración y un estado."""

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")

    def __init__(self, codigo, cliente, servicio, duracion, impuesto=0, descuento=0):
        if cliente is None:
            raise DatosInvalidosError("La reserva requiere un cliente.")
        if servicio is None:
            raise DatosInvalidosError("La reserva requiere un servicio.")
        try:
            duracion = float(duracion)
        except (TypeError, ValueError) as error:
            raise DatosInvalidosError("La duración debe ser numérica.") from error
        if duracion <= 0:
            raise DatosInvalidosError("La duración debe ser mayor que cero.")

        self.codigo = str(codigo).strip()
        if not self.codigo:
            raise DatosInvalidosError("El código de reserva es obligatorio.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.impuesto = float(impuesto)
        self.descuento = float(descuento)
        self.estado = "PENDIENTE"
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.costo = None
        registrar_evento(f"Reserva {self.codigo} creada en estado PENDIENTE.")

    def calcular_total(self):
        """Calcula el costo aplicando polimorfismo según el servicio recibido."""
        self.servicio.validar()
        return self.servicio.calcular_costo(
            self.duracion, self.impuesto, self.descuento
        )

    def confirmar(self):
        if self.estado != "PENDIENTE":
            raise EstadoReservaError(
                f"No se puede confirmar la reserva {self.codigo}: "
                f"su estado actual es {self.estado}."
            )
        self.servicio.validar()
        self.costo = self.calcular_total()
        self.estado = "CONFIRMADA"
        registrar_evento(
            f"Reserva {self.codigo} confirmada. Total: ${self.costo:.2f}."
        )
        return self.costo

    def cancelar(self):
        if self.estado == "CANCELADA":
            raise EstadoReservaError(f"La reserva {self.codigo} ya está cancelada.")
        if self.estado == "PROCESADA":
            raise EstadoReservaError(
                f"No se puede cancelar la reserva {self.codigo} porque ya fue procesada."
            )
        self.estado = "CANCELADA"
        registrar_evento(f"Reserva {self.codigo} cancelada.")
        return True

    def procesar(self):
        """Procesa una reserva confirmada; encadena errores inesperados."""
        try:
            if self.estado != "CONFIRMADA":
                raise EstadoReservaError(
                    "Solo se pueden procesar reservas previamente confirmadas."
                )
            self.servicio.validar()
            if self.costo is None:
                self.costo = self.calcular_total()
        except ServicioNoDisponibleError as error:
            registrar_error(f"Error al procesar reserva {self.codigo}: {error}")
            raise EstadoReservaError(
                "No fue posible procesar la reserva porque el servicio no está disponible."
            ) from error
        except Exception as error:
            registrar_error(f"Error inesperado al procesar reserva {self.codigo}: {error}")
            raise RuntimeError(
                f"Fallo controlado durante el procesamiento de la reserva {self.codigo}."
            ) from error
        else:
            self.estado = "PROCESADA"
            registrar_evento(f"Reserva {self.codigo} procesada correctamente.")
            return f"Reserva {self.codigo} procesada. Total: ${self.costo:.2f}"
        finally:
            registrar_evento(f"Finalizó el intento de procesamiento de reserva {self.codigo}.")

    def __str__(self):
        costo = f"${self.costo:.2f}" if self.costo is not None else "Pendiente de cálculo"
        return (
            f"Reserva {self.codigo} | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Duración: {self.duracion} | "
            f"Estado: {self.estado} | Costo: {costo}"
        )
