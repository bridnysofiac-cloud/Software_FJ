"""Modelo y validaciones de los clientes."""

import re
from entidades import Entidad
from excepciones import DatosInvalidosError


class Cliente(Entidad):
    """Cliente con encapsulación de sus datos personales."""

    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion, nombre)
        self.__correo = str(correo).strip()
        self.__telefono = str(telefono).strip()
        self.validar()

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def validar(self):
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", self.__correo):
            raise DatosInvalidosError("El correo electrónico no tiene un formato válido.")
        if not self.__telefono:
            raise DatosInvalidosError("El teléfono del cliente es obligatorio.")
        if not re.fullmatch(r"[0-9+\-\s]+", self.__telefono):
            raise DatosInvalidosError("El teléfono solo debe contener números, espacios, + o -.")
        cantidad_digitos = sum(caracter.isdigit() for caracter in self.__telefono)
        if cantidad_digitos < 7:
            raise DatosInvalidosError("El teléfono debe contener al menos 7 dígitos.")
        return True

    def __str__(self):
        return (
            f"Cliente [ID: {self.identificador}, Nombre: {self.nombre}, "
            f"Correo: {self.__correo}, Teléfono: {self.__telefono}]"
        )
