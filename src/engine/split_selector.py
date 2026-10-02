"""
Selección pura de plantillas de división semanal (Split) según disponibilidad y objetivo.
"""
from src.models.catalog import SplitTemplate
from src.models.enums import GoalEnum


def select_split_template(
    available_splits: dict[str, SplitTemplate],
    dias_disponibles: int,
    objetivo: GoalEnum,
) -> SplitTemplate:
    """
    Función pura que selecciona la plantilla de split óptima.
    
    Reglas funcionales:
    - Si dias_disponibles <= 2: Fullbody 2 días.
    - Si dias_disponibles == 3: Fullbody 3 días.
    - Si dias_disponibles == 4: Upper / Lower 4 días.
    - Si dias_disponibles == 5: Push / Pull / Legs 5 días.
    - Si dias_disponibles >= 6: Push / Pull / Legs 6 días.
    """
    if dias_disponibles <= 2:
        target_id = "fullbody_2dias"
    elif dias_disponibles == 3:
        target_id = "fullbody_3dias"
    elif dias_disponibles == 4:
        target_id = "upper_lower_4dias"
    elif dias_disponibles == 5:
        target_id = "push_pull_legs_5dias"
    else:
        target_id = "push_pull_legs_6dias"

    # Retorna la plantilla solicitada o el fallback de 3 días si no existiera
    if target_id in available_splits:
        return available_splits[target_id]
    
    # Fallback determinista al primer split disponible
    return next(iter(available_splits.values()))
