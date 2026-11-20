"""Modelo y validaciones de los clientes."""

import re
from entidades import Entidad
from excepciones import DatosInvalidosError


class Cliente(Entidad):
    """Cliente con encapsulación de sus datos personales."""

    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion, nombre)
        self.__correo = correo
        self.__telefono = telefono
        self.validar()

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def validar(self):
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", str(self.__correo).strip()):
            raise DatosInvalidosError("El correo electrónico no tiene un formato válido.")
        if not str(self.__telefono).strip():
            raise DatosInvalidosError("El teléfono del cliente es obligatorio.")
        if not str(self.__telefono).strip().replace("+", "").replace("-", "").replace(" ", "").isdigit():
            raise DatosInvalidosError("El teléfono solo debe contener números, espacios, + o -.")
        if len(str(self.__telefono).strip()) < 7:
            raise DatosInvalidosError("El teléfono debe contener al menos 7 dígitos.")
        return True

    def __str__(self):
        return (
            f"Cliente [ID: {self.identificador}, Nombre: {self.nombre}, "
            f"Correo: {self.__correo}, Teléfono: {self.__telefono}]"
        )
