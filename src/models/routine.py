"""
Modelos inmutables de la Rutina de Entrenamiento (Salida del Sistema).
Garantiza que la técnica provenga fija del catálogo mientras los parámetros sean editables.
"""
from dataclasses import dataclass
from src.models.catalog import Exercise
from src.models.enums import MuscleGroupEnum


@dataclass(frozen=True)
class ExerciseExecutionDetail:
    """
    Parámetros de ejecución para un ejercicio dentro de la rutina.
    Los parámetros numéricos son editables por el usuario, mientras que la técnica es fija.
    """
    series: int
    repeticiones_sugeridas: int
    peso_kg_sugerido: float
    descanso_segundos: int
    instrucciones_fijas: tuple[str, ...]
    precauciones: tuple[str, ...]


@dataclass(frozen=True)
class WorkoutSlot:
    """
    Ranura muscular dentro de un día de entrenamiento.
    Contiene el ejercicio principal asignado y 1 a 2 alternativas viables del catálogo filtrado.
    """
    grupo_muscular: MuscleGroupEnum
    ejercicio_principal: Exercise
    alternativas: tuple[Exercise, ...]
    parametros: ExerciseExecutionDetail


@dataclass(frozen=True)
class DailyWorkout:
    """Plan de entrenamiento programado para un día específico."""
    dia_numero: int
    nombre_dia: str
    slots: tuple[WorkoutSlot, ...]
    duracion_estimada_minutos: int


@dataclass(frozen=True)
class WeeklyRoutine:
    """
    Rutina semanal completa generada por el agente de IA.
    Es inmutable; cualquier ajuste genera una nueva instancia preservando la historia.
    """
    id_rutina: str
    split_id: str
    nombre_split: str
    dias: tuple[DailyWorkout, ...]
    fecha_creacion: str
    explicacion_agente: str
