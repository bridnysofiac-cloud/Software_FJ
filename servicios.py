"""Clase abstracta Servicio y sus tres especializaciones."""

from abc import abstractmethod
from entidades import Entidad
from excepciones import DatosInvalidosError, ServicioNoDisponibleError


class Servicio(Entidad):
    """Define la estructura común de los servicios de Software FJ."""

    def __init__(self, codigo, nombre, precio_base, disponible=True):
        super().__init__(codigo, nombre)
        self._precio_base = self._validar_numero_positivo(precio_base, "El precio base")
        self._disponible = bool(disponible)

    @staticmethod
    def _validar_numero_positivo(valor, etiqueta):
        try:
            numero = float(valor)
        except (TypeError, ValueError) as error:
            raise DatosInvalidosError(f"{etiqueta} debe ser un número.") from error
        if numero <= 0:
            raise DatosInvalidosError(f"{etiqueta} debe ser mayor que cero.")
        return numero

    @property
    def precio_base(self):
        return self._precio_base

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, disponible):
        self._disponible = bool(disponible)

    def validar(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.nombre}' no está disponible."
            )
        return True

    def _aplicar_impuesto_descuento(self, subtotal, impuesto=0, descuento=0):
        """Simula sobrecarga mediante parámetros opcionales de impuesto y descuento."""
        impuesto = float(impuesto)
        descuento = float(descuento)
        if not 0 <= impuesto <= 100:
            raise DatosInvalidosError("El impuesto debe estar entre 0 y 100.")
        if not 0 <= descuento <= 100:
            raise DatosInvalidosError("El descuento debe estar entre 0 y 100.")
        total_con_impuesto = subtotal * (1 + impuesto / 100)
        return round(total_con_impuesto * (1 - descuento / 100), 2)

    @abstractmethod
    def calcular_costo(self, cantidad=1, impuesto=0, descuento=0):
        """Calcula el costo según el tipo de servicio."""
        raise NotImplementedError

    @abstractmethod
    def describir(self):
        """Devuelve una descripción del servicio."""
        raise NotImplementedError


class ReservaSala(Servicio):
    """Servicio de alquiler de salas, cobrado por hora."""

    def __init__(self, codigo, nombre, precio_por_hora, capacidad, disponible=True):
        super().__init__(codigo, nombre, precio_por_hora, disponible)
        if int(capacidad) <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser mayor que cero.")
        self.capacidad = int(capacidad)

    def calcular_costo(self, cantidad=1, impuesto=0, descuento=0):
        horas = self._validar_numero_positivo(cantidad, "La cantidad de horas")
        subtotal = self.precio_base * horas
        return self._aplicar_impuesto_descuento(subtotal, impuesto, descuento)

    def describir(self):
        return (
            f"Sala '{self.nombre}': ${self.precio_base:.2f} por hora; "
            f"capacidad máxima: {self.capacidad} personas."
        )


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos, cobrado por día."""

    def __init__(self, codigo, nombre, precio_por_dia, unidades_disponibles, disponible=True):
        super().__init__(codigo, nombre, precio_por_dia, disponible)
        if int(unidades_disponibles) <= 0:
            raise DatosInvalidosError("Las unidades disponibles deben ser mayores que cero.")
        self.unidades_disponibles = int(unidades_disponibles)

    def calcular_costo(self, cantidad=1, impuesto=0, descuento=0):
        dias = self._validar_numero_positivo(cantidad, "La cantidad de días")
        subtotal = self.precio_base * dias
        return self._aplicar_impuesto_descuento(subtotal, impuesto, descuento)

    def describir(self):
        return (
            f"Equipo '{self.nombre}': ${self.precio_base:.2f} por día; "
            f"unidades disponibles: {self.unidades_disponibles}."
        )


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría, cobrado por sesión."""

    def __init__(self, codigo, nombre, precio_por_sesion, especialidad, disponible=True):
        super().__init__(codigo, nombre, precio_por_sesion, disponible)
        if not str(especialidad).strip():
            raise DatosInvalidosError("La especialidad de la asesoría es obligatoria.")
        self.especialidad = str(especialidad).strip()

    def calcular_costo(self, cantidad=1, impuesto=0, descuento=0):
        sesiones = self._validar_numero_positivo(cantidad, "La cantidad de sesiones")
        subtotal = self.precio_base * sesiones
        return self._aplicar_impuesto_descuento(subtotal, impuesto, descuento)

    def describir(self):
        return (
            f"Asesoría '{self.nombre}': ${self.precio_base:.2f} por sesión; "
            f"especialidad: {self.especialidad}."
        )
