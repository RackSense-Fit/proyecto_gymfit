"""
Generador funcional puro de rutinas de entrenamiento semanales.
Ensambla slots con ejercicios principales, 1-2 alternativas y técnica fija de catálogo.
"""
import uuid
from src.catalog.filters import filter_by_muscle_group
from src.engine.explainer import explain_initial_routine
from src.models.catalog import Exercise, LevelParameters, SplitTemplate
from src.models.enums import GoalEnum, LevelEnum, MuscleGroupEnum
from src.models.profile import UserProfile
from src.models.routine import (
    DailyWorkout,
    ExerciseExecutionDetail,
    WeeklyRoutine,
    WorkoutSlot,
)


def calculate_default_weight_suggestion(
    exercise: Exercise,
    perfil: UserProfile,
) -> float:
    """Función pura que sugiere un peso inicial de referencia según ejercicio y perfil."""
    if "peso_corporal" in exercise.equipo_requerido and len(exercise.equipo_requerido) == 1:
        return 0.0

    # Estimaciones iniciales conservadoras para inicio de bloque
    base_factor = 0.4 if perfil.nivel == LevelEnum.PRINCIPIANTE else (0.6 if perfil.nivel == LevelEnum.INTERMEDIO else 0.8)
    
    if "mancuernas" in exercise.equipo_requerido:
        # Peso por mancuerna en kg
        suggested = round((perfil.peso_kg * 0.10 * base_factor) * 2) / 2
        return max(4.0, suggested)
    
    if "barra" in exercise.equipo_requerido:
        # Peso total de barra + discos en kg
        suggested = round((perfil.peso_kg * 0.35 * base_factor) / 2.5) * 2.5
        return max(20.0, suggested)
    
    if "maquina_prensa" in exercise.equipo_requerido:
        suggested = round((perfil.peso_kg * 0.8 * base_factor) / 5.0) * 5.0
        return max(30.0, suggested)

    # Máquinas y poleas en general
    return max(15.0, round((perfil.peso_kg * 0.25 * base_factor) / 5.0) * 5.0)


def calculate_rest_seconds(
    perfil: UserProfile,
    level_params: LevelParameters,
) -> int:
    """
    Calcula el tiempo de descanso recomendado entre series principalmente según el objetivo.

    Nota: El valor para GANAR_MUSCULO (150s) es una aproximación orientada a ejercicios
    compuestos (el volumen total efectivo importa más que el descanso corto, según evidencia
    reciente que descarta la idea de que el estrés metabólico de descansos cortos favorece
    más la hipertrofia). En una fase futura (cuando el modelo Exercise tenga un campo
    'mechanic' compound/isolation) debería refinarse para dar menos descanso a ejercicios
    de aislamiento (1-2 min) que a compuestos (2-3 min).
    """
    match perfil.objetivo:
        case GoalEnum.FUERZA:
            # Resíntesis de fosfocreatina y recuperación del SNC requieren 3-5 min con cargas >=85% 1RM
            return 240
        case GoalEnum.GANAR_MUSCULO:
            # Aproximación orientada a ejercicios compuestos; prima el volumen total efectivo
            return 150
        case GoalEnum.BAJAR_GRASA:
            return 30
        case GoalEnum.MANTENIMIENTO:
            return 60
        case _:
            return level_params.descanso_segundos


def build_execution_detail(
    exercise: Exercise,
    perfil: UserProfile,
    level_params: LevelParameters,
) -> ExerciseExecutionDetail:
    """Construye los detalles de ejecución combinando Tabla A (series/reps/descanso) con Tabla B (técnica fija)."""
    # Ajuste de series según objetivo (fuerza -> superior, bajar_grasa -> inferior, hipertrofia/mantenimiento -> promedio)
    series_min, series_max = level_params.rango_series_por_ejercicio
    if perfil.objetivo == GoalEnum.FUERZA:
        series = series_max
    elif perfil.objetivo == GoalEnum.BAJAR_GRASA:
        series = series_min
    else:
        series = (series_min + series_max) // 2
    
    # Ajuste de repeticiones según objetivo (fuerza -> rango bajo, hipertrofia -> medio, quema -> alto)
    rep_min, rep_max = level_params.rango_repeticiones
    if perfil.objetivo == GoalEnum.FUERZA:
        reps = rep_min
    elif perfil.objetivo == GoalEnum.BAJAR_GRASA:
        reps = rep_max
    else:
        reps = (rep_min + rep_max) // 2

    peso_sugerido = calculate_default_weight_suggestion(exercise, perfil)
    descanso = calculate_rest_seconds(perfil, level_params)

    return ExerciseExecutionDetail(
        series=series,
        repeticiones_sugeridas=reps,
        peso_kg_sugerido=peso_sugerido,
        descanso_segundos=descanso,
        instrucciones_fijas=exercise.instrucciones_fijas,
        precauciones=exercise.precauciones_seguridad,
    )


def generate_workout_slot(
    target_muscle: MuscleGroupEnum,
    eligible_catalog: tuple[Exercise, ...],
    perfil: UserProfile,
    level_params: LevelParameters,
) -> WorkoutSlot | None:
    """
    Selecciona de forma pura el ejercicio principal y 1-2 alternativas para un grupo muscular.
    """
    matching_exercises = filter_by_muscle_group(eligible_catalog, target_muscle)
    if not matching_exercises:
        return None

    # El primero se asigna como principal; los siguientes hasta 2 como alternativas
    principal = matching_exercises[0]
    alternativas = tuple(matching_exercises[1:3])
    
    parametros = build_execution_detail(principal, perfil, level_params)

    return WorkoutSlot(
        grupo_muscular=target_muscle,
        ejercicio_principal=principal,
        alternativas=alternativas,
        parametros=parametros,
    )


def generate_routine(
    perfil: UserProfile,
    eligible_catalog: tuple[Exercise, ...],
    level_params: LevelParameters,
    split_template: SplitTemplate,
    timestamp: str,
    id_rutina: str | None = None,
) -> WeeklyRoutine:
    """
    Generador funcional completo de la rutina semanal.
    Produce una estructura inmutable WeeklyRoutine.
    """
    dias_list: list[DailyWorkout] = []
    total_slots_count = 0
    all_used_equipment: set[str] = set()

    for scheme in split_template.distribucion:
        slots_for_day: list[WorkoutSlot] = []
        for muscle in scheme.grupos_objetivo:
            slot = generate_workout_slot(muscle, eligible_catalog, perfil, level_params)
            if slot is not None:
                slots_for_day.append(slot)
                all_used_equipment.update(slot.ejercicio_principal.equipo_requerido)
                for alt in slot.alternativas:
                    all_used_equipment.update(alt.equipo_requerido)
        
        # Estimar duración en minutos: ~45 seg por serie + descanso
        total_series = sum(s.parametros.series for s in slots_for_day)
        tiempo_descanso_min = sum(s.parametros.series * s.parametros.descanso_segundos for s in slots_for_day) / 60.0
        tiempo_ejecucion_min = (total_series * 45) / 60.0
        duracion_estimada = int(tiempo_descanso_min + tiempo_ejecucion_min + 10) # 10 min calentamiento

        total_slots_count += len(slots_for_day)
        dias_list.append(
            DailyWorkout(
                dia_numero=scheme.dia_numero,
                nombre_dia=scheme.nombre_dia,
                slots=tuple(slots_for_day),
                duracion_estimada_minutos=max(30, duracion_estimada),
            )
        )

    routine_id = id_rutina or f"rutina_{uuid.uuid4().hex[:8]}"
    explicacion = explain_initial_routine(
        perfil=perfil,
        split=split_template,
        total_ejercicios=total_slots_count,
        equipos_usados=frozenset(all_used_equipment),
    )

    return WeeklyRoutine(
        id_rutina=routine_id,
        split_id=split_template.id,
        nombre_split=split_template.nombre,
        dias=tuple(dias_list),
        fecha_creacion=timestamp,
        explicacion_agente=explicacion,
    )
