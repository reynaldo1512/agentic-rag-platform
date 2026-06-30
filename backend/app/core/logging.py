"""
Configuración centralizada de logging para la aplicación.
"""

import logging
import sys

from app.core.config import get_settings


def configure_logging() -> None:
    """
    Configura el logging raíz de la aplicación según `LOG_LEVEL`.

    Se invoca una única vez durante el arranque de la aplicación
    (ver `app.main`).
    """
    settings = get_settings()

    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )
