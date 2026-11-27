"""
Configuración inmutable de Gemini Vision y carga desde la frontera de entorno.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

_DEFAULT_ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


@dataclass(frozen=True)
class GeminiSettings:
    """Parámetros inmutables de configuración para el analizador de visión."""

    modelo: str
    temperatura: float = 0.2
    max_image_bytes: int = 20 * 1024 * 1024
    mime_types_validos: tuple[str, ...] = (
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/heic",
        "image/heif",
    )
    umbral_alto: float = 0.7  # pendiente de calibrar con el spike
    umbral_bajo: float = 0.5  # pendiente de calibrar con el spike


def load_settings(env_path: Path | str | None = _DEFAULT_ENV_PATH) -> GeminiSettings:
    """
    Función de frontera que lee GEMINI_MODEL del entorno (y opcionalmente .env)
    y construye un GeminiSettings inmutable.
    """
    if env_path is not None:
        load_dotenv(env_path)

    modelo = os.getenv("GEMINI_MODEL", "").strip()
    if not modelo:
        raise ValueError(
            "Falta la variable de entorno GEMINI_MODEL. "
            "Configúrala en .env o en el entorno antes de iniciar."
        )

    return GeminiSettings(modelo=modelo)
