"""Capa de administración: listas internas y operaciones del sistema."""

from excepciones import (
    ClienteNoEncontradoError,
    DatosInvalidosError,
    ReservaNoEncontradaError,
    ServicioNoDisponibleError,
)
from logs import registrar_evento, registrar_error
from reservas import Reserva


class SistemaGestion:
    """Administra clientes, servicios y reservas usando listas en memoria."""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        if any(c.identificador == cliente.identificador for c in self.clientes):
            raise DatosInvalidosError(
                f"Ya existe un cliente con identificación {cliente.identificador}."
            )
        self.clientes.append(cliente)
        registrar_evento(f"Cliente {cliente.identificador} registrado correctamente.")
        return cliente

    def buscar_cliente(self, identificacion):
        for cliente in self.clientes:
            if cliente.identificador == str(identificacion):
                return cliente
        raise ClienteNoEncontradoError(
            f"No se encontró el cliente con identificación {identificacion}."
        )

    def agregar_servicio(self, servicio):
        if any(s.identificador == servicio.identificador for s in self.servicios):
            raise DatosInvalidosError(
                f"Ya existe un servicio con código {servicio.identificador}."
            )
        self.servicios.append(servicio)
        registrar_evento(f"Servicio {servicio.identificador} agregado correctamente.")
        return servicio

    def buscar_servicio(self, codigo):
        for servicio in self.servicios:
            if servicio.identificador == str(codigo):
                return servicio
        raise ServicioNoDisponibleError(f"No existe el servicio con código {codigo}.")

    def crear_reserva(self, codigo, identificacion_cliente, codigo_servicio,
                      duracion, impuesto=0, descuento=0):
        cliente = self.buscar_cliente(identificacion_cliente)
        servicio = self.buscar_servicio(codigo_servicio)
        servicio.validar()
        if any(r.codigo == str(codigo) for r in self.reservas):
            raise DatosInvalidosError(f"Ya existe la reserva con código {codigo}.")
        reserva = Reserva(
            codigo, cliente, servicio, duracion, impuesto=impuesto, descuento=descuento
        )
        self.reservas.append(reserva)
        registrar_evento(f"Reserva {codigo} agregada al sistema.")
        return reserva

    def buscar_reserva(self, codigo):
        for reserva in self.reservas:
            if reserva.codigo == str(codigo):
                return reserva
        raise ReservaNoEncontradaError(f"No se encontró la reserva {codigo}.")

    def listar_clientes(self):
        return list(self.clientes)

    def listar_servicios(self):
        return list(self.servicios)

    def listar_reservas(self):
        return list(self.reservas)
