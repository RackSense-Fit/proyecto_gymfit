"""
Esquemas Pydantic para validación y serialización de solicitudes y respuestas de la API.
Garantiza el tipado estricto entre el cliente (móvil/web) y el núcleo funcional en Python.

NOTA: Pydantic V2 deprecó el argumento `example=` en Field().
      Se usa `json_schema_extra={"example": ...}` como reemplazo oficial.
"""
from typing import Any
from pydantic import BaseModel, Field
from src.models.enums import (
    DifficultyPerceptionEnum,
    GoalEnum,
    LevelEnum,
    SexEnum,
    UnforeseenTypeEnum,
)


class ProfileCreateRequest(BaseModel):
    """Solicitud de creación o actualización de perfil de usuario."""
    nombre: str = Field(..., min_length=1, json_schema_extra={"example": "Carlos Mendoza"})
    sexo: SexEnum = Field(..., json_schema_extra={"example": SexEnum.MASCULINO})
    peso_kg: float = Field(..., gt=0, json_schema_extra={"example": 76.0})
    altura_cm: float = Field(..., gt=0, json_schema_extra={"example": 178.0})
    objetivo: GoalEnum = Field(..., json_schema_extra={"example": GoalEnum.GANAR_MUSCULO})
    nivel: LevelEnum = Field(..., json_schema_extra={"example": LevelEnum.PRINCIPIANTE})
    dias_disponibles: int = Field(..., ge=1, le=7, json_schema_extra={"example": 3})


class EquipmentRegisterRequest(BaseModel):
    """Solicitud para registrar el inventario de equipo disponible en el gimnasio."""
    equipo: list[str] = Field(..., json_schema_extra={"example": ["mancuernas", "banco_plano", "barra_dominadas"]})


class SessionStartRequest(BaseModel):
    """Solicitud para iniciar una sesión de entrenamiento."""
    dia_numero: int = Field(..., ge=1, le=7, json_schema_extra={"example": 1})
    fecha: str | None = Field(default=None, json_schema_extra={"example": "2026-09-20"})
    hora_inicio: str | None = Field(default=None, json_schema_extra={"example": "14:00:00"})


class SetRecordRequest(BaseModel):
    """Solicitud para registrar una serie completada con peso, reps y cronómetro de descanso."""
    id_sesion: str = Field(..., json_schema_extra={"example": "sesion_001"})
    ejercicio_id: str = Field(..., json_schema_extra={"example": "press_plano_mancuernas"})
    numero_serie: int = Field(..., ge=1, json_schema_extra={"example": 1})
    peso_kg: float = Field(..., ge=0, json_schema_extra={"example": 12.0})
    repeticiones: int = Field(..., ge=1, json_schema_extra={"example": 12})
    descanso_segundos_real: int = Field(..., ge=0, json_schema_extra={"example": 90})


class SessionFinishRequest(BaseModel):
    """Solicitud para finalizar la sesión del día."""
    id_sesion: str = Field(..., json_schema_extra={"example": "sesion_001"})
    hora_fin: str | None = Field(default=None, json_schema_extra={"example": "14:48:00"})
    duracion_total_segundos: int = Field(..., ge=1, json_schema_extra={"example": 2880})


class ReportDiscomfortRequest(BaseModel):
    """Solicitud para reportar dolor o molestia articular."""
    zona_articular: str = Field(..., json_schema_extra={"example": "hombro"})
    intensidad_1_a_10: int = Field(..., ge=1, le=10, json_schema_extra={"example": 6})
    ejercicio_origen_id: str | None = Field(default=None, json_schema_extra={"example": "press_plano_mancuernas"})


class ReportTimeCrunchRequest(BaseModel):
    """Solicitud para reportar falta de tiempo o imprevisto en un día."""
    tipo: UnforeseenTypeEnum = Field(
        default=UnforeseenTypeEnum.POCO_TIEMPO,
        json_schema_extra={"example": UnforeseenTypeEnum.POCO_TIEMPO},
    )
    dia_afectado: int = Field(..., ge=1, le=7, json_schema_extra={"example": 2})
    minutos_disponibles_hoy: int = Field(..., ge=10, le=120, json_schema_extra={"example": 25})
    detalle: str = Field(
        default="Tengo poco tiempo disponible hoy",
        json_schema_extra={"example": "Reunión urgente en 30 minutos"},
    )


class ReportDifficultyRequest(BaseModel):
    """Solicitud para reportar percepción de dificultad."""
    ejercicio_id: str = Field(..., json_schema_extra={"example": "remo_unilateral_mancuerna"})
    percepcion: DifficultyPerceptionEnum = Field(
        ...,
        json_schema_extra={"example": DifficultyPerceptionEnum.MUY_FACIL},
    )
    comentarios: str = Field(
        default="",
        json_schema_extra={"example": "Completé todas las repeticiones con mucha facilidad"},
    )


class GenericEventDispatchRequest(BaseModel):
    """Esquema genérico para despachar cualquier DomainEvent serializado."""
    event_type: str = Field(..., json_schema_extra={"example": "MolestiaReportada"})
    payload: dict[str, Any] = Field(
        ...,
        json_schema_extra={"example": {"zona_articular": "hombro", "intensidad_1_a_10": 5}},
    )
