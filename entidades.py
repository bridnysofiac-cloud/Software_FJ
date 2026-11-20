"""Clase abstracta general para las entidades del sistema."""

from abc import ABC, abstractmethod
from excepciones import DatosInvalidosError


class Entidad(ABC):
    """Representa una entidad general identificada dentro de Software FJ."""

    def __init__(self, identificador, nombre):
        identificador = str(identificador).strip()
        nombre = str(nombre).strip()

        if not identificador:
            raise DatosInvalidosError("El identificador no puede estar vacío.")
        if not nombre:
            raise DatosInvalidosError("El nombre no puede estar vacío.")

        self._identificador = identificador
        self._nombre = nombre

    @property
    def identificador(self):
        return self._identificador

    @property
    def nombre(self):
        return self._nombre

    @abstractmethod
    def validar(self):
        """Cada entidad concreta debe implementar sus propias validaciones."""
        raise NotImplementedError
