"""
equipment_analyzer.py – Analizador de equipo de gimnasio mediante Gemini Structured Outputs.

Arquitectura funcional:
    - Funciones puras: validar_imagen, build_response_schema,
      build_equipment_catalog_prompt, armar_request,
      parsear_y_filtrar_respuesta, equipment_ids_only.
    - Frontera de red (única función con E/S): analyze_gym_image.

No lee archivos, ni variables de entorno, ni contiene listas de equipo o
parámetros técnicos hardcodeados. Todo entra por argumento desde la frontera.
"""

from __future__ import annotations

from dataclasses import dataclass
import io
from typing import Any, Literal

from google import genai
from google.genai import types
from PIL import Image
from pydantic import BaseModel, Field, create_model

from src.catalog.loader import detectable_ids
from src.config.settings import GeminiSettings
from src.models.catalog import EquipmentVocabularyItem


CalidadFotoType = Literal["buena", "regular", "mala"]


# ──────────────────────────────────────────────
# 1. Esquema de salida tipado y esquema dinámico
# ──────────────────────────────────────────────
class EquipoDetectado(BaseModel):
    """Un equipo individual del vocabulario detectado en la imagen."""

    equipo_id: str = Field(
        description="Identificador exacto del equipo perteneciente al vocabulario detectable."
    )
    confianza_0_a_1: float = Field(
        ge=0.0,
        le=1.0,
        description="Confianza real de la detección, de 0.0 a 1.0.",
    )
    justificacion_visual: str = Field(
        description="Evidencia visual específica: qué se ve y dónde en la imagen."
    )


class AnalisisEquipoResponse(BaseModel):
    """Respuesta completa del análisis de equipo en una foto de gimnasio."""

    equipos_detectados: list[EquipoDetectado] = Field(
        default_factory=list,
        description="Lista de equipos del vocabulario identificados visualmente.",
    )
    resumen: str = Field(
        default="",
        description="Resumen breve del entorno observado.",
    )
    no_identificado: list[str] = Field(
        default_factory=list,
        description="Descripciones breves de equipo visible que no corresponde a ningún id del vocabulario.",
    )
    personas_visibles: int = Field(
        default=0,
        ge=0,
        description="Cantidad de personas visibles en la foto.",
    )
    calidad_foto: CalidadFotoType = Field(
        default="buena",
        description="Calidad visual de la foto: 'buena', 'regular' o 'mala'.",
    )
    texto_visible: list[str] = Field(
        default_factory=list,
        description="Lista de textos legibles en máquinas o carteles.",
    )


@dataclass(frozen=True)
class GeminiRequestPayload:
    """Estructura inmutable con los parámetros listos para enviar al SDK de Gemini."""

    model: str
    contents: list[Any]
    config: types.GenerateContentConfig
    response_schema: type[BaseModel]


def build_response_schema(
    vocabulario: tuple[EquipmentVocabularyItem, ...],
) -> type[BaseModel]:
    """
    Función pura: construye un esquema Pydantic dinámico restringido
    exclusivamente a los IDs detectables del vocabulario recibido.
    """
    ids_detectables = detectable_ids(vocabulario)
    if not ids_detectables:
        raise ValueError("El vocabulario no contiene ningún equipo detectable.")

    dynamic_equipo_id = Literal[ids_detectables]  # type: ignore[valid-type]

    dynamic_equipo_detectado = create_model(
        "EquipoDetectado",
        equipo_id=(
            dynamic_equipo_id,
            Field(
                description="Identificador exacto del equipo; debe pertenecer al vocabulario detectable."
            ),
        ),
        confianza_0_a_1=(
            float,
            Field(
                ge=0.0,
                le=1.0,
                description="Confianza real de la detección, de 0.0 a 1.0.",
            ),
        ),
        justificacion_visual=(
            str,
            Field(
                description="Evidencia visual específica: qué se ve y dónde en la imagen."
            ),
        ),
    )

    return create_model(
        "AnalisisEquipoResponse",
        equipos_detectados=(
            list[dynamic_equipo_detectado],  # type: ignore[valid-type]
            Field(
                default_factory=list,
                description="Lista de equipos del vocabulario identificados visualmente.",
            ),
        ),
        resumen=(
            str,
            Field(
                default="",
                description="Resumen breve del entorno observado.",
            ),
        ),
        no_identificado=(
            list[str],
            Field(
                default_factory=list,
                description="Descripciones breves de equipo visible que no corresponde a ningún id del vocabulario.",
            ),
        ),
        personas_visibles=(
            int,
            Field(
                default=0,
                ge=0,
                description="Cantidad de personas visibles en la foto.",
            ),
        ),
        calidad_foto=(
            CalidadFotoType,
            Field(
                default="buena",
                description="Calidad visual de la foto: 'buena', 'regular' o 'mala'.",
            ),
        ),
        texto_visible=(
            list[str],
            Field(
                default_factory=list,
                description="Lista de textos legibles en máquinas o carteles.",
            ),
        ),
    )


# ──────────────────────────────────────────────
# 2. Funciones puras de validación, armado de request y parseo
# ──────────────────────────────────────────────
def validar_imagen(
    image_bytes: bytes,
    mime_type: str,
    settings: GeminiSettings,
) -> None:
    """Función pura: valida tamaño, MIME type e integridad de bytes de la imagen."""
    if not image_bytes:
        raise ValueError("La imagen está vacía (0 bytes).")

    if len(image_bytes) > settings.max_image_bytes:
        raise ValueError(
            f"La imagen pesa {len(image_bytes) / 1024 / 1024:.1f} MB, "
            f"el máximo es {settings.max_image_bytes / 1024 / 1024:.0f} MB."
        )

    if mime_type not in settings.mime_types_validos:
        raise ValueError(
            f"MIME type '{mime_type}' no soportado. Usa uno de: {settings.mime_types_validos}"
        )

    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.verify()
    except Exception as exc:
        raise ValueError(f"La imagen está corrupta o no es válida: {exc}") from exc


def build_equipment_catalog_prompt(
    vocabulario: tuple[EquipmentVocabularyItem, ...],
) -> str:
    """
    Función pura: formatea las definiciones visuales de los equipos detectables
    para inyectarlas en las instrucciones del sistema.
    """
    lineas = ["VOCABULARIO DE EQUIPOS DETECTABLES (usa únicamente estos IDs):"]
    for item in vocabulario:
        if item.detectable:
            lineas.append(f"- {item.id} ({item.nombre_es}): {item.descripcion_visual}")
    return "\n".join(lineas)


def armar_request(
    image_bytes: bytes,
    mime_type: str,
    settings: GeminiSettings,
    vocabulario: tuple[EquipmentVocabularyItem, ...],
    system_prompt: str,
    user_prompt: str,
) -> GeminiRequestPayload:
    """
    Función pura: construye la solicitud y configuración estructurada para Gemini
    sin herramientas, búsqueda, pensamiento extendido ni contexto largo.
    """
    schema = build_response_schema(vocabulario)
    catalogo_texto = build_equipment_catalog_prompt(vocabulario)
    full_system_instruction = f"{system_prompt.strip()}\n\n{catalogo_texto}"

    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
    config = types.GenerateContentConfig(
        system_instruction=full_system_instruction,
        response_mime_type="application/json",
        response_schema=schema,
        temperature=settings.temperatura,
    )
    return GeminiRequestPayload(
        model=settings.modelo,
        contents=[user_prompt.strip(), image_part],
        config=config,
        response_schema=schema,
    )


def parsear_y_filtrar_respuesta(
    raw_text: str | None,
    parsed_response: Any,
    vocabulario: tuple[EquipmentVocabularyItem, ...],
) -> AnalisisEquipoResponse:
    """
    Función pura: valida la respuesta del modelo contra el esquema dinámico del
    vocabulario y la normaliza a AnalisisEquipoResponse, filtrando IDs no permitidos.
    """
    schema = build_response_schema(vocabulario)
    valid_ids = set(detectable_ids(vocabulario))

    if parsed_response is not None:
        if isinstance(parsed_response, BaseModel):
            raw_dict = parsed_response.model_dump()
        elif isinstance(parsed_response, dict):
            raw_dict = parsed_response
        else:
            raise RuntimeError(
                f"Tipo de respuesta parseada no soportado: {type(parsed_response).__name__}"
            )
        validated = schema.model_validate(raw_dict)
    else:
        text = raw_text or ""
        try:
            validated = schema.model_validate_json(text)
        except Exception as exc:
            raise RuntimeError(
                f"Gemini no devolvió una respuesta estructurada válida. "
                f"Texto crudo: {text[:500]}"
            ) from exc

    normalized = AnalisisEquipoResponse.model_validate(validated.model_dump())
    equipos_filtrados = [
        eq for eq in normalized.equipos_detectados if eq.equipo_id in valid_ids
    ]
    return normalized.model_copy(update={"equipos_detectados": equipos_filtrados})


def equipment_ids_only(result: AnalisisEquipoResponse) -> list[str]:
    """Función pura: extrae solo los IDs de equipo detectados."""
    return [eq.equipo_id for eq in result.equipos_detectados]


# ──────────────────────────────────────────────
# 3. Única función de frontera con llamada de red
# ──────────────────────────────────────────────
def analyze_gym_image(
    image_bytes: bytes,
    mime_type: str,
    *,
    settings: GeminiSettings,
    vocabulario: tuple[EquipmentVocabularyItem, ...],
    system_prompt: str,
    user_prompt: str,
    api_key: str,
) -> AnalisisEquipoResponse:
    """
    Frontera de red: valida la imagen, envía la solicitud a la API de Gemini
    con salida estructurada y devuelve el resultado validado.

    Raises:
        ValueError: si falta api_key, el vocabulario es inválido o la imagen no pasa validación.
        RuntimeError: si la llamada a Gemini o el parseo de la respuesta fallan.
    """
    if not api_key:
        raise ValueError(
            "No se proporcionó GEMINI_API_KEY para llamar al analizador de visión."
        )

    validar_imagen(image_bytes, mime_type, settings)
    payload = armar_request(
        image_bytes=image_bytes,
        mime_type=mime_type,
        settings=settings,
        vocabulario=vocabulario,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=payload.model,
            contents=payload.contents,
            config=payload.config,
        )
    except Exception as exc:
        raise RuntimeError(
            f"Error al llamar a Gemini ({payload.model}): {exc}"
        ) from exc

    return parsear_y_filtrar_respuesta(
        raw_text=getattr(response, "text", None),
        parsed_response=getattr(response, "parsed", None),
        vocabulario=vocabulario,
    )
