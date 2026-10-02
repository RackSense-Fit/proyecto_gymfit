"""
Modelos inmutables para el Catálogo del Sistema.
Separa estrictamente la Tabla A (Parámetros por Nivel) de la Tabla B (Ejercicios y Splits).
"""
from dataclasses import dataclass
from src.models.enums import (
    LevelEnum,
    MovementPatternEnum,
    MuscleGroupEnum,
    RiskLevelEnum,
)


@dataclass(frozen=True)
class LevelParameters:
    """
    Tabla A — Parámetros y reglas por nivel de experiencia (Lineamientos ACSM / NSCA).
    Son reglas que dependen del usuario, no del ejercicio en particular.
    """
    nivel: LevelEnum
    rango_series_por_ejercicio: tuple[int, int]
    rango_repeticiones: tuple[int, int]
    descanso_segundos: int
    progresion_carga_semanal_pct: float
    precauciones_generales: tuple[str, ...]
    ejercicios_restringidos_ids: frozenset[str]
    enfoque_principal: str


@dataclass(frozen=True)
class Exercise:
    """
    Tabla B — Ejercicio del Catálogo Universal (Free Exercise DB / wger compatible).
    Son hechos objetivos e inmutables del mundo, independientes del usuario.
    """
    id: str
    nombre: str
    grupo_muscular: MuscleGroupEnum
    patron_movimiento: MovementPatternEnum
    equipo_requerido: frozenset[str]
    nivel_minimo: LevelEnum
    nivel_riesgo: RiskLevelEnum
    articulaciones_comprometidas: frozenset[str]
    instrucciones_fijas: tuple[str, ...]
    errores_comunes: tuple[str, ...]
    precauciones_seguridad: tuple[str, ...]


@dataclass(frozen=True)
class DailySplitScheme:
    """Distribución de grupos musculares programados para un día específico de la semana."""
    dia_numero: int
    nombre_dia: str
    grupos_objetivo: tuple[MuscleGroupEnum, ...]


@dataclass(frozen=True)
class SplitTemplate:
    """Plantilla de división semanal (Fullbody, Torso/Pierna, Push/Pull/Legs)."""
    id: str
    nombre: str
    dias_semana: int
    descripcion: str
    distribucion: tuple[DailySplitScheme, ...]


@dataclass(frozen=True)
class Catalog:
    """Contenedor global e inmutable de ambas tablas de catálogo."""
    tabla_a_niveles: dict[LevelEnum, LevelParameters]
    tabla_b_ejercicios: tuple[Exercise, ...]
    tabla_b_splits: dict[str, SplitTemplate]
