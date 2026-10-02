"""
Paquete del Motor de Decisión Funcional y Agente IA de GymFit.
"""
from src.engine.adjuster import (
    adjust_for_absence,
    adjust_for_difficulty,
    adjust_for_discomfort,
    adjust_for_time_crunch,
)
from src.engine.explainer import (
    explain_adjustment,
    explain_initial_routine,
)
from src.engine.generator import (
    build_execution_detail,
    calculate_default_weight_suggestion,
    generate_routine,
    generate_workout_slot,
)
from src.engine.split_selector import select_split_template

__all__ = [
    "select_split_template",
    "calculate_default_weight_suggestion",
    "build_execution_detail",
    "generate_workout_slot",
    "generate_routine",
    "adjust_for_discomfort",
    "adjust_for_time_crunch",
    "adjust_for_difficulty",
    "adjust_for_absence",
    "explain_initial_routine",
    "explain_adjustment",
]
