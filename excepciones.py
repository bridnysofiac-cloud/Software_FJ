"""Excepciones personalizadas del sistema Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base para los errores controlados de la aplicación."""


class DatosInvalidosError(SoftwareFJError):
    """Se produce cuando un dato no cumple las validaciones."""


class ClienteNoEncontradoError(SoftwareFJError):
    """Se produce cuando no existe el cliente solicitado."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Se produce cuando un servicio no está disponible."""


class ReservaNoEncontradaError(SoftwareFJError):
    """Se produce cuando no existe la reserva solicitada."""


class EstadoReservaError(SoftwareFJError):
    """Se produce cuando una operación no corresponde al estado de la reserva."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Se produce cuando se intenta realizar una operación no permitida."""
