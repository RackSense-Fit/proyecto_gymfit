"""
equipment_analyzer.py – Analizador de equipo de gimnasio mediante Gemini Structured Outputs.

Módulo desacoplado que recibe bytes de imagen y devuelve una lista tipada
de equipos detectados (restringidos a los 12 IDs válidos de GymFit).

Dependencias:
    google-genai >= 3.3.0
    pydantic     (viene con google-genai)
    pillow       >= 13.0
    python-dotenv >= 1.2

Uso:
    from src.vision.equipment_analyzer import analyze_gym_image
    resultado = analyze_gym_image(image_bytes, mime_type="image/jpeg")
    for eq in resultado.equipos_detectados:
        print(eq.equipo_id, eq.confianza_0_a_1, eq.justificacion_visual)
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from pydantic import BaseModel, Field
import io


# ──────────────────────────────────────────────
# 1. Cargar variables de entorno
# ──────────────────────────────────────────────
_ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(_ENV_PATH)

_API_KEY = os.getenv("GEMINI_API_KEY", "")
_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")


# ──────────────────────────────────────────────
# 2. IDs válidos de equipo (Tabla B)
# ──────────────────────────────────────────────
EQUIPO_IDS = (
    "mancuernas",
    "banco_plano",
    "banco_inclinado",
    "barra",
    "barra_dominadas",
    "polea",
    "maquina_pecho",
    "maquina_remo",
    "maquina_prensa",
    "maquina_extensiones",
    "maquina_curl_femoral",
    "peso_corporal",
)

EquipoIdType = Literal[
    "mancuernas",
    "banco_plano",
    "banco_inclinado",
    "barra",
    "barra_dominadas",
    "polea",
    "maquina_pecho",
    "maquina_remo",
    "maquina_prensa",
    "maquina_extensiones",
    "maquina_curl_femoral",
    "peso_corporal",
]


# ──────────────────────────────────────────────
# 3. Esquemas Pydantic (Structured Outputs)
# ──────────────────────────────────────────────
class EquipoDetectado(BaseModel):
    """Un equipo individual detectado en la imagen."""
    equipo_id: EquipoIdType = Field(
        description="Identificador exacto del equipo, debe ser uno de los 12 válidos."
    )
    confianza_0_a_1: float = Field(
        ge=0.0, le=1.0,
        description="Confianza de la detección, de 0.0 (nada seguro) a 1.0 (totalmente seguro)."
    )
    justificacion_visual: str = Field(
        description="Breve explicación de qué se ve en la imagen que justifica la detección."
    )


class AnalisisEquipoResponse(BaseModel):
    """Respuesta completa del análisis de equipo en una foto de gimnasio."""
    equipos_detectados: list[EquipoDetectado] = Field(
        default_factory=list,
        description="Lista de equipos identificados visualmente en la imagen."
    )
    resumen: str = Field(
        default="",
        description="Resumen breve del entorno observado (ej. 'Área de peso libre con banco y mancuernas')."
    )


# ──────────────────────────────────────────────
# 4. Prompt del sistema
# ──────────────────────────────────────────────
_SYSTEM_PROMPT = """\
Eres un experto en equipamiento de gimnasio. Tu tarea es analizar la foto que
el usuario te envía e identificar TODO el equipo de gimnasio visible.

REGLAS ESTRICTAS:
1. Solo puedes reportar equipos cuyo ID esté en esta lista:
   mancuernas, banco_plano, banco_inclinado, barra, barra_dominadas, polea,
   maquina_pecho, maquina_remo, maquina_prensa, maquina_extensiones,
   maquina_curl_femoral, peso_corporal.

2. "peso_corporal" solo se reporta si NO hay ningún otro equipo visible
   (es decir, la persona solo puede entrenar con su cuerpo).

3. Si hay un banco ajustable que puede ponerse plano o inclinado, repórtalo
   como "banco_plano" Y "banco_inclinado" con una nota en la justificación.

4. Si ves equipo que no encaja en ningún ID, IGNÓRALO. No lo inventes.

5. Asigna la confianza honestamente:
   - 0.9-1.0 → Se ve claramente, sin ambigüedad.
   - 0.7-0.89 → Probablemente es ese equipo, pero la vista es parcial.
   - 0.5-0.69 → Podría ser, pero hay incertidumbre.
   - <0.5 → No lo reportes, la incertidumbre es demasiado alta.

6. En "justificacion_visual", describe brevemente QUÉ ves (forma, color,
   ubicación en la imagen) que te lleva a esa conclusión.

7. En "resumen", describe en 1-2 oraciones el entorno general de la foto.

8. Responde SOLO con el JSON estructurado, sin texto adicional.
"""

_USER_PROMPT = """\
Analiza esta foto de gimnasio y lista todo el equipo visible.
"""


# ──────────────────────────────────────────────
# 5. Validación de imagen
# ──────────────────────────────────────────────
_MIME_TYPES_VALIDOS = {"image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"}
_MAX_BYTES = 20 * 1024 * 1024  # 20 MB — límite de Gemini por archivo inline


def _validar_imagen(image_bytes: bytes, mime_type: str) -> None:
    """Valida tamaño y formato de la imagen antes de enviarla al API."""
    if not image_bytes:
        raise ValueError("La imagen está vacía (0 bytes).")

    if len(image_bytes) > _MAX_BYTES:
        raise ValueError(
            f"La imagen pesa {len(image_bytes) / 1024 / 1024:.1f} MB, "
            f"el máximo es {_MAX_BYTES / 1024 / 1024:.0f} MB."
        )

    if mime_type not in _MIME_TYPES_VALIDOS:
        raise ValueError(
            f"MIME type '{mime_type}' no soportado. Usa uno de: {_MIME_TYPES_VALIDOS}"
        )

    # Verificar que Pillow puede abrir la imagen (integridad)
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.verify()
    except Exception as exc:
        raise ValueError(f"La imagen está corrupta o no es válida: {exc}") from exc


# ──────────────────────────────────────────────
# 6. Función principal (pura en lógica, efecto solo al llamar al API)
# ──────────────────────────────────────────────
def analyze_gym_image(
    image_bytes: bytes,
    mime_type: str = "image/jpeg",
    *,
    api_key: str | None = None,
    model: str | None = None,
) -> AnalisisEquipoResponse:
    """
    Analiza una imagen de gimnasio y devuelve los equipos detectados.

    Args:
        image_bytes: Contenido binario de la imagen.
        mime_type:   Tipo MIME de la imagen (por defecto "image/jpeg").
        api_key:     Clave de API de Gemini. Si no se pasa, se lee del .env.
        model:       Nombre del modelo Gemini. Si no se pasa, se lee del .env.

    Returns:
        AnalisisEquipoResponse con la lista de equipos y un resumen.

    Raises:
        ValueError: si la imagen es inválida o falta la API key.
        RuntimeError: si el API de Gemini falla.
    """
    # Resolver credenciales
    key = api_key if api_key is not None else (os.getenv("GEMINI_API_KEY") or _API_KEY)
    if not key:
        raise ValueError(
            "No se encontró GEMINI_API_KEY. "
            "Configúrala en el archivo .env o pásala como argumento."
        )
    model_name = model or os.getenv("GEMINI_MODEL") or _MODEL

    # Validar la imagen
    _validar_imagen(image_bytes, mime_type)

    # Crear cliente
    client = genai.Client(api_key=key)

    # Construir la parte de imagen
    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

    # Llamar al modelo con Structured Outputs
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=[
                _USER_PROMPT,
                image_part,
            ],
            config=types.GenerateContentConfig(
                system_instruction=_SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=AnalisisEquipoResponse,
                temperature=0.2,  # Baja para consistencia en detección
            ),
        )
    except Exception as exc:
        raise RuntimeError(
            f"Error al llamar a Gemini ({model_name}): {exc}"
        ) from exc

    # Parsear la respuesta estructurada
    parsed = response.parsed
    if parsed is None:
        # Fallback: intentar parsear manualmente el texto
        raw_text = response.text or ""
        try:
            parsed = AnalisisEquipoResponse.model_validate_json(raw_text)
        except Exception:
            raise RuntimeError(
                f"Gemini no devolvió una respuesta estructurada válida. "
                f"Texto crudo: {raw_text[:500]}"
            )

    return parsed


# ──────────────────────────────────────────────
# 7. Utilidades auxiliares
# ──────────────────────────────────────────────
def analyze_gym_image_from_file(
    file_path: str | Path,
    *,
    api_key: str | None = None,
    model: str | None = None,
) -> AnalisisEquipoResponse:
    """
    Conveniencia: carga una imagen desde un archivo y la analiza.

    Args:
        file_path: Ruta al archivo de imagen.
        api_key:   Clave de API (opcional, se lee del .env).
        model:     Modelo Gemini (opcional, se lee del .env).

    Returns:
        AnalisisEquipoResponse con los equipos detectados.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró la imagen: {path}")

    # Determinar MIME type por extensión
    ext_to_mime = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".heic": "image/heic",
        ".heif": "image/heif",
    }
    mime = ext_to_mime.get(path.suffix.lower())
    if mime is None:
        raise ValueError(f"Extensión '{path.suffix}' no soportada.")

    image_bytes = path.read_bytes()
    return analyze_gym_image(image_bytes, mime, api_key=api_key, model=model)


def equipment_ids_only(result: AnalisisEquipoResponse) -> list[str]:
    """
    Extrae solo los IDs de equipo (sin confianza ni justificación).
    Útil para pasar directo al generador de rutinas.
    """
    return [eq.equipo_id for eq in result.equipos_detectados]


# ──────────────────────────────────────────────
# 8. Ejecución directa (script de prueba rápida)
# ──────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python -m src.vision.equipment_analyzer <ruta_imagen>")
        print("  Ej: python -m src.vision.equipment_analyzer foto_gym.jpg")
        sys.exit(1)

    ruta = sys.argv[1]
    print(f"📷 Analizando imagen: {ruta}")
    print(f"🤖 Modelo: {_MODEL}")
    print()

    try:
        resultado = analyze_gym_image_from_file(ruta)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    print(f"📝 Resumen: {resultado.resumen}")
    print(f"🏋️ Equipos detectados ({len(resultado.equipos_detectados)}):")
    print()

    for eq in resultado.equipos_detectados:
        barra = "█" * int(eq.confianza_0_a_1 * 20)
        espacios = "░" * (20 - int(eq.confianza_0_a_1 * 20))
        print(f"  {eq.equipo_id:<25} [{barra}{espacios}] {eq.confianza_0_a_1:.0%}")
        print(f"  {'':25} └─ {eq.justificacion_visual}")
        print()

    print(f"✅ IDs para el generador: {equipment_ids_only(resultado)}")
