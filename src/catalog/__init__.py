"""
Paquete de Catálogo y Filtrado Funcional de GymFit Agent.
"""
from src.catalog.filters import (
    filter_by_equipment,
    filter_by_joint_safety,
    filter_by_level,
    filter_by_muscle_group,
    get_eligible_catalog,
    normalize_equipment,
)
from src.catalog.loader import (
    detectable_ids,
    load_equipment_vocabulary,
    load_exercises,
    load_full_catalog,
    load_level_parameters,
    load_split_templates,
)

__all__ = [
    "load_level_parameters",
    "load_exercises",
    "load_split_templates",
    "load_full_catalog",
    "load_equipment_vocabulary",
    "detectable_ids",
    "normalize_equipment",
    "filter_by_equipment",
    "filter_by_level",
    "filter_by_muscle_group",
    "filter_by_joint_safety",
    "get_eligible_catalog",
]
