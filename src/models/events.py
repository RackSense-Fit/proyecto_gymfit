"""
Modelado algebraico de Eventos del Dominio (Event Sourcing).
Cada evento es un tipo inmutable discriminado, agrupado en el tipo algebraico DomainEvent.
"""
from dataclasses import dataclass
from src.models.enums import DifficultyPerceptionEnum, UnforeseenTypeEnum
from src.models.profile import UserProfile
from src.models.routine import WeeklyRoutine


# -----------------------------------------------------------------------------
# 1. Eventos de Configuración Inicial y Perfil
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class PerfilCreado:
    """Evento disparado cuando el usuario crea o define su perfil por primera vez."""
    perfil: UserProfile
    timestamp: str


@dataclass(frozen=True)
class EquipoRegistrado:
    """Evento disparado cuando el usuario declara el equipo disponible en su gimnasio."""
    equipo: frozenset[str]
    timestamp: str


@dataclass(frozen=True)
class EquipoActualizado:
    """Evento disparado cuando el inventario de equipo del usuario cambia."""
    nuevo_equipo: frozenset[str]
    timestamp: str


# -----------------------------------------------------------------------------
# 2. Eventos de Planificación y Rutina
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class RutinaGenerada:
    """Evento disparado tras la generación o reestructuración de una rutina semanal."""
    rutina: WeeklyRoutine
    timestamp: str


# -----------------------------------------------------------------------------
# 3. Eventos de Sesión de Entrenamiento en Tiempo Real
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class SesionIniciada:
    """Evento disparado al comenzar a entrenar un día de la rutina."""
    id_sesion: str
    dia_numero: int
    fecha: str
    hora_inicio: str
    timestamp: str


@dataclass(frozen=True)
class SerieRegistrada:
    """Evento disparado al completar y registrar una serie con peso, reps y cronómetro de descanso."""
    id_sesion: str
    ejercicio_id: str
    numero_serie: int
    peso_kg: float
    repeticiones: int
    descanso_segundos_real: int
    timestamp: str


@dataclass(frozen=True)
class SesionFinalizada:
    """Evento disparado al terminar la sesión del día."""
    id_sesion: str
    hora_fin: str
    duracion_total_segundos: int
    timestamp: str


# -----------------------------------------------------------------------------
# 4. Eventos de Variabilidad Reportada por el Usuario
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class DificultadReportada:
    """Feedback del usuario sobre la exigencia percibida en un ejercicio."""
    ejercicio_id: str
    percepcion: DifficultyPerceptionEnum
    comentarios: str
    timestamp: str


@dataclass(frozen=True)
class MolestiaReportada:
    """Reporte de dolor articular o muscular que requiere ajuste de ejercicios/volumen."""
    zona_articular: str
    intensidad_1_a_10: int
    ejercicio_origen_id: str | None
    timestamp: str


@dataclass(frozen=True)
class ImprevistoReportado:
    """Reporte de contingencia (poco tiempo, mal descanso, evento social, día perdido)."""
    tipo: UnforeseenTypeEnum
    dia_afectado: int
    minutos_disponibles_hoy: int | None
    detalle: str
    timestamp: str


# -----------------------------------------------------------------------------
# 5. Eventos de Variabilidad Inferida por el Sistema
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class AusenciaDetectada:
    """Evento inferido por el sistema ante periodos prolongados sin registro de sesiones."""
    dias_sin_registro: int
    fecha_corte: str
    timestamp: str


# -----------------------------------------------------------------------------
# Tipo Algebraico de Unión (Discriminated Union)
# -----------------------------------------------------------------------------

type DomainEvent = (
    PerfilCreado
    | EquipoRegistrado
    | EquipoActualizado
    | RutinaGenerada
    | SesionIniciada
    | SerieRegistrada
    | SesionFinalizada
    | DificultadReportada
    | MolestiaReportada
    | ImprevistoReportado
    | AusenciaDetectada
)
