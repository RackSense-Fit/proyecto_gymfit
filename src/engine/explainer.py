"""
Generador funcional de explicaciones contextuales y justificaciones del agente.
"""
from src.models.catalog import SplitTemplate
from src.models.enums import GoalEnum, LevelEnum
from src.models.profile import UserProfile


def explain_initial_routine(
    perfil: UserProfile,
    split: SplitTemplate,
    total_ejercicios: int,
    equipos_usados: frozenset[str],
) -> str:
    """Genera una explicación contextual pura para la rutina generada inicialmente."""
    meta_desc = {
        GoalEnum.BAJAR_GRASA: "optimización metabólica y preservación de masa magra",
        GoalEnum.GANAR_MUSCULO: "estímulo hipertrófico y sobrecarga progresiva",
        GoalEnum.MANTENIMIENTO: "acondicionamiento físico y salud integral",
        GoalEnum.FUERZA: "adaptación neuromuscular e intensificación de cargas",
    }.get(perfil.objetivo, "desarrollo integral")

    nivel_desc = {
        LevelEnum.PRINCIPIANTE: "priorizando volumen moderado, rango amplio de repeticiones y control motor seguro",
        LevelEnum.INTERMEDIO: "con volumen balanceado y rangos medios de hipertrofia",
        LevelEnum.AVANZADO: "con alta densidad, series de mayor intensidad y descansos optimizados",
    }.get(perfil.nivel, "adaptado a tu experiencia")

    equipos_str = ", ".join(sorted(equipos_usados)) if equipos_usados else "peso corporal"

    return (
        f"Hola {perfil.nombre}. He diseñado tu plan semanal utilizando la estructura '{split.nombre}', "
        f"enfocada en {meta_desc} para tus {perfil.dias_disponibles} días disponibles. "
        f"La dosificación se calibró para tu nivel {perfil.nivel.value.capitalize()} ({nivel_desc}). "
        f"Todos los {total_ejercicios} ejercicios y sus alternativas fueron seleccionados exclusivamente "
        f"a partir de tu equipo disponible registrado ({equipos_str}), manteniendo la técnica fija "
        f"del catálogo por seguridad física."
    )


def explain_adjustment(
    tipo_evento: str,
    motivo: str,
    detalle_cambios: str,
) -> str:
    """Genera una explicación contextual pura para ajustes reactivos de la rutina."""
    return (
        f"[Ajuste Adaptativo del Agente] Evento: {tipo_evento}. "
        f"Motivo: {motivo}. "
        f"Modificaciones aplicadas: {detalle_cambios} "
        f"El resto del plan se mantiene estable para garantizar la continuidad del estímulo."
    )
