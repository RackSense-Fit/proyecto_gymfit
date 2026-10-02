"""
Carga pura de catálogos desde archivos JSON hacia estructuras de datos inmutables.
"""
import json
from pathlib import Path
from src.models.catalog import (
    Catalog,
    DailySplitScheme,
    Exercise,
    LevelParameters,
    SplitTemplate,
)
from src.models.enums import (
    LevelEnum,
    MovementPatternEnum,
    MuscleGroupEnum,
    RiskLevelEnum,
)


def load_level_parameters(filepath: Path | str) -> dict[LevelEnum, LevelParameters]:
    """Carga de forma pura los parámetros de la Tabla A desde un archivo JSON."""
    path = Path(filepath)
    with path.open("r", encoding="utf-8") as f:
        raw_data = json.load(f)

    result: dict[LevelEnum, LevelParameters] = {}
    for key, val in raw_data.items():
        level_enum = LevelEnum(val["nivel"])
        params = LevelParameters(
            nivel=level_enum,
            rango_series_por_ejercicio=tuple(val["rango_series_por_ejercicio"]),
            rango_repeticiones=tuple(val["rango_repeticiones"]),
            descanso_segundos=int(val["descanso_segundos"]),
            progresion_carga_semanal_pct=float(val["progresion_carga_semanal_pct"]),
            precauciones_generales=tuple(val["precauciones_generales"]),
            ejercicios_restringidos_ids=frozenset(val["ejercicios_restringidos_ids"]),
            enfoque_principal=str(val["enfoque_principal"]),
        )
        result[level_enum] = params
    return result


def load_exercises(filepath: Path | str) -> tuple[Exercise, ...]:
    """Carga de forma pura el catálogo de ejercicios de la Tabla B desde un archivo JSON."""
    path = Path(filepath)
    with path.open("r", encoding="utf-8") as f:
        raw_list = json.load(f)

    exercises: list[Exercise] = []
    for item in raw_list:
        ex = Exercise(
            id=str(item["id"]),
            nombre=str(item["nombre"]),
            grupo_muscular=MuscleGroupEnum(item["grupo_muscular"]),
            patron_movimiento=MovementPatternEnum(item["patron_movimiento"]),
            equipo_requerido=frozenset(item["equipo_requerido"]),
            nivel_minimo=LevelEnum(item["nivel_minimo"]),
            nivel_riesgo=RiskLevelEnum(item["nivel_riesgo"]),
            articulaciones_comprometidas=frozenset(item["articulaciones_comprometidas"]),
            instrucciones_fijas=tuple(item["instrucciones_fijas"]),
            errores_comunes=tuple(item["errores_comunes"]),
            precauciones_seguridad=tuple(item["precauciones_seguridad"]),
        )
        exercises.append(ex)
    return tuple(exercises)


def load_split_templates(filepath: Path | str) -> dict[str, SplitTemplate]:
    """Carga de forma pura las plantillas de splits de la Tabla B desde un archivo JSON."""
    path = Path(filepath)
    with path.open("r", encoding="utf-8") as f:
        raw_dict = json.load(f)

    splits: dict[str, SplitTemplate] = {}
    for split_id, data in raw_dict.items():
        dias_list: list[DailySplitScheme] = []
        for d in data["distribucion"]:
            scheme = DailySplitScheme(
                dia_numero=int(d["dia_numero"]),
                nombre_dia=str(d["nombre_dia"]),
                grupos_objetivo=tuple(MuscleGroupEnum(g) for g in d["grupos_objetivo"]),
            )
            dias_list.append(scheme)

        template = SplitTemplate(
            id=str(data["id"]),
            nombre=str(data["nombre"]),
            dias_semana=int(data["dias_semana"]),
            descripcion=str(data["descripcion"]),
            distribucion=tuple(dias_list),
        )
        splits[split_id] = template
    return splits


def load_full_catalog(data_dir: Path | str) -> Catalog:
    """Función de composición pura que carga todo el catálogo estático."""
    base = Path(data_dir)
    tabla_a = load_level_parameters(base / "table_a_levels.json")
    tabla_b_ejercicios = load_exercises(base / "table_b_exercises.json")
    tabla_b_splits = load_split_templates(base / "table_b_splits.json")

    return Catalog(
        tabla_a_niveles=tabla_a,
        tabla_b_ejercicios=tabla_b_ejercicios,
        tabla_b_splits=tabla_b_splits,
    )
