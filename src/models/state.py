"""
Estado inmutable de la aplicación (AppState) y estructuras de registro de sesión.
Todo el estado evoluciona exclusivamente mediante funciones reductoras puras.
"""
from dataclasses import dataclass
from src.models.events import DomainEvent
from src.models.profile import UserProfile
from src.models.routine import WeeklyRoutine


@dataclass(frozen=True)
class SetLog:
    """Registro inmutable de una serie individual completada."""
    numero_serie: int
    peso_kg: float
    repeticiones: int
    descanso_segundos_real: int


@dataclass(frozen=True)
class ExerciseSessionLog:
    """Registro inmutable de todas las series de un ejercicio en una sesión."""
    ejercicio_id: str
    series: tuple[SetLog, ...]


@dataclass(frozen=True)
class SessionLog:
    """Registro inmutable de una sesión de entrenamiento completada o en progreso."""
    id_sesion: str
    dia_numero: int
    fecha: str
    hora_inicio: str
    hora_fin: str | None
    duracion_total_segundos: int | None
    ejercicios: tuple[ExerciseSessionLog, ...]


@dataclass(frozen=True)
class CalendarEntry:
    """Registro inmutable de un día en el calendario de entrenamiento mensual."""
    fecha_iso: str
    completado: bool
    id_sesion: str | None


@dataclass(frozen=True)
class AdjustmentLog:
    """Registro inmutable de adaptaciones explicadas realizadas por el agente."""
    timestamp: str
    motivo: str
    detalle_ajuste: str
    evento_causante_tipo: str


@dataclass(frozen=True)
class AppState:
    """
    Estado global inmutable de GymFit Agent.
    
    Principios de inmutabilidad:
    - No existen setters ni mutaciones 'in-place'.
    - Las colecciones son tuplas inmutables (`tuple`) o conjuntos congelados (`frozenset`).
    - Para cambiar el estado, la función reductora devuelve una nueva instancia de AppState.
    """
    perfil: UserProfile | None = None
    equipo_disponible: frozenset[str] = frozenset()
    rutina_actual: WeeklyRoutine | None = None
    sesion_en_curso: SessionLog | None = None
    historial_sesiones: tuple[SessionLog, ...] = ()
    calendario: tuple[CalendarEntry, ...] = ()
    historial_ajustes: tuple[AdjustmentLog, ...] = ()
    historial_eventos: tuple[DomainEvent, ...] = ()

    @property
    def total_sesiones_completadas(self) -> int:
        """Calcula el total de sesiones finalizadas con éxito."""
        return len(self.historial_sesiones)

    @property
    def dias_entrenados_mes_actual(self) -> int:
        """Conteo puro de días entrenados en el calendario."""
        return sum(1 for entry in self.calendario if entry.completado)
