"""
Funciones puras de filtrado de catálogo para GymFit Agent.
Implementa el filtrado bicondicional estricto: Equipo ∩ Nivel del Usuario.
"""
from typing import Sequence
from src.models.catalog import Exercise, LevelParameters
from src.models.enums import LevelEnum, MuscleGroupEnum


# Jerarquía estricta de niveles para determinar qué ejercicios son accesibles
LEVEL_HIERARCHY: dict[LevelEnum, set[LevelEnum]] = {
    LevelEnum.PRINCIPIANTE: {LevelEnum.PRINCIPIANTE},
    LevelEnum.INTERMEDIO: {LevelEnum.PRINCIPIANTE, LevelEnum.INTERMEDIO},
    LevelEnum.AVANZADO: {LevelEnum.PRINCIPIANTE, LevelEnum.INTERMEDIO, LevelEnum.AVANZADO},
}


def normalize_equipment(equipment: frozenset[str]) -> frozenset[str]:
    """
    Función pura que garantiza que 'peso_corporal' siempre esté disponible
    en cualquier gimnasio o entorno de entrenamiento.
    """
    return equipment | frozenset({"peso_corporal"})


def filter_by_equipment(
    exercises: Sequence[Exercise],
    available_equipment: frozenset[str],
) -> tuple[Exercise, ...]:
    """
    Filtro puro de equipo:
    Un ejercicio es viable si y solo si TODO su equipo requerido está contenido
    dentro del conjunto de equipo que el usuario tiene disponible.
    """
    normalized_eq = normalize_equipment(available_equipment)
    return tuple(
        ex for ex in exercises
        if ex.equipo_requerido.issubset(normalized_eq)
    )


def filter_by_level(
    exercises: Sequence[Exercise],
    user_level: LevelEnum,
    restricted_ids: frozenset[str] = frozenset(),
) -> tuple[Exercise, ...]:
    """
    Filtro puro de nivel:
    1. Filtra ejercicios cuyo nivel_minimo sea alcanzable por el usuario.
    2. Excluye cualquier ejercicio marcado como restringido en la Tabla A para dicho nivel.
    """
    allowed_levels = LEVEL_HIERARCHY.get(user_level, {LevelEnum.PRINCIPIANTE})
    return tuple(
        ex for ex in exercises
        if ex.nivel_minimo in allowed_levels and ex.id not in restricted_ids
    )


def filter_by_muscle_group(
    exercises: Sequence[Exercise],
    target_muscle: MuscleGroupEnum,
) -> tuple[Exercise, ...]:
    """Filtra puramente los ejercicios que pertenecen a un grupo muscular determinado."""
    return tuple(ex for ex in exercises if ex.grupo_muscular == target_muscle)


def filter_by_joint_safety(
    exercises: Sequence[Exercise],
    painful_joint: str,
) -> tuple[Exercise, ...]:
    """
    Filtro puro de seguridad articular:
    Excluye ejercicios que comprometen una articulación o zona con molestia reportada.
    """
    painful_normalized = painful_joint.strip().lower()
    return tuple(
        ex for ex in exercises
        if painful_normalized not in {j.lower() for j in ex.articulaciones_comprometidas}
    )


def get_eligible_catalog(
    exercises: Sequence[Exercise],
    available_equipment: frozenset[str],
    user_level: LevelEnum,
    level_params: LevelParameters,
) -> tuple[Exercise, ...]:
    """
    Composición pura de filtros (Filtrado Bicondicional):
    Solo los ejercicios que cumplen simultáneamente con el equipo disponible Y
    el nivel de experiencia del usuario llegan al motor de decisión.
    
    catálogo_elegible = filter_by_level(filter_by_equipment(catálogo, equipo), nivel)
    """
    equipment_filtered = filter_by_equipment(exercises, available_equipment)
    eligible = filter_by_level(
        equipment_filtered,
        user_level,
        level_params.ejercicios_restringidos_ids,
    )
    return eligible
