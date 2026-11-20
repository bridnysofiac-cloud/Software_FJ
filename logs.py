"""Configuración centralizada del registro de eventos y errores."""

import logging
from pathlib import Path

RUTA_LOG = Path(__file__).resolve().parent / "registro_sistema.log"


def obtener_logger():
    """Devuelve un logger configurado para guardar información en un archivo."""
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.INFO)

    # Evita agregar varios manejadores si el módulo se importa más de una vez.
    if not logger.handlers:
        manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        manejador.setFormatter(formato)
        logger.addHandler(manejador)

    return logger


logger = obtener_logger()


def registrar_evento(mensaje):
    """Registra una operación normal del sistema."""
    logger.info(mensaje)


def registrar_error(mensaje):
    """Registra un error controlado."""
    logger.error(mensaje)


def registrar_excepcion(mensaje):
    """Registra la excepción junto con su información técnica."""
    logger.exception(mensaje)
