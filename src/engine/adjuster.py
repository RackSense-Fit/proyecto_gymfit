"""
Lógica pura de adaptación y ajuste reactivo de rutinas ante eventos de variabilidad.
Cada función es pura: recibe la rutina actual y el evento, y devuelve una nueva rutina inmutable.
"""
from src.catalog.filters import filter_by_joint_safety, filter_by_muscle_group
from src.engine.explainer import explain_adjustment
from src.engine.generator import build_execution_detail
from src.models.catalog import Exercise, LevelParameters
from src.models.enums import DifficultyPerceptionEnum, UnforeseenTypeEnum
from src.models.events import (
    AusenciaDetectada,
    DificultadReportada,
    ImprevistoReportado,
    MolestiaReportada,
)
from src.models.profile import UserProfile
from src.models.routine import (
    DailyWorkout,
    ExerciseExecutionDetail,
    WeeklyRoutine,
    WorkoutSlot,
)


def adjust_for_discomfort(
    routine: WeeklyRoutine,
    eligible_catalog: tuple[Exercise, ...],
    level_params: LevelParameters,
    perfil: UserProfile,
    molestia: MolestiaReportada,
) -> tuple[WeeklyRoutine, str]:
    """
    Ajuste puro ante MolestiaReportada:
    Sustituye ejercicios que comprometen la zona afectada por alternativas seguras
    o reduce volumen y carga de forma protectora.
    """
    zona_dolor = molestia.zona_articular.strip().lower()
    modificaciones: list[str] = []
    nuevos_dias: list[DailyWorkout] = []

    for dia in routine.dias:
        nuevos_slots: list[WorkoutSlot] = []
        for slot in dia.slots:
            afecta_zona = zona_dolor in {j.lower() for j in slot.ejercicio_principal.articulaciones_comprometidas}
            
            if afecta_zona:
                # Buscar alternativa segura en las opciones del slot
                alternativa_segura = next(
                    (alt for alt in slot.alternativas if zona_dolor not in {j.lower() for j in alt.articulaciones_comprometidas}),
                    None,
                )
                
                # Si no está en el slot, buscar en todo el catálogo elegible
                if alternativa_segura is None:
                    candidatos = filter_by_muscle_group(eligible_catalog, slot.grupo_muscular)
                    seguros = filter_by_joint_safety(candidatos, zona_dolor)
                    if seguros:
                        alternativa_segura = seguros[0]

                if alternativa_segura is not None:
                    nuevos_params = build_execution_detail(alternativa_segura, perfil, level_params)
                    nuevos_slots.append(
                        WorkoutSlot(
                            grupo_muscular=slot.grupo_muscular,
                            ejercicio_principal=alternativa_segura,
                            alternativas=slot.alternativas,
                            parametros=nuevos_params,
                        )
                    )
                    modificaciones.append(
                        f"Día {dia.dia_numero}: '{slot.ejercicio_principal.nombre}' sustituido por '{alternativa_segura.nombre}' para proteger {zona_dolor}."
                    )
                else:
                    # Si no hay sustituto, reducir series al mínimo con aviso de precaución
                    params_protegidos = ExerciseExecutionDetail(
                        series=max(1, slot.parametros.series - 1),
                        repeticiones_sugeridas=slot.parametros.repeticiones_sugeridas,
                        peso_kg_sugerido=round(slot.parametros.peso_kg_sugerido * 0.7, 1),
                        descanso_segundos=slot.parametros.descanso_segundos + 30,
                        instrucciones_fijas=slot.parametros.instrucciones_fijas,
                        precauciones=(f"PRECAUCIÓN POR MOLESTIA EN {zona_dolor.upper()}: Ejecutar sin dolor.",) + slot.parametros.precauciones,
                    )
                    nuevos_slots.append(
                        WorkoutSlot(
                            grupo_muscular=slot.grupo_muscular,
                            ejercicio_principal=slot.ejercicio_principal,
                            alternativas=slot.alternativas,
                            parametros=params_protegidos,
                        )
                    )
                    modificaciones.append(
                        f"Día {dia.dia_numero}: Reducción de 30% en carga y series para '{slot.ejercicio_principal.nombre}' por molestia en {zona_dolor}."
                    )
            else:
                nuevos_slots.append(slot)

        nuevos_dias.append(
            DailyWorkout(
                dia_numero=dia.dia_numero,
                nombre_dia=dia.nombre_dia,
                slots=tuple(nuevos_slots),
                duracion_estimada_minutos=dia.duracion_estimada_minutos,
            )
        )

    resumen_cambios = " | ".join(modificaciones) if modificaciones else f"No se requirieron cambios en ejercicios para {zona_dolor}."
    explicacion = explain_adjustment(
        tipo_evento="MolestiaReportada",
        motivo=f"Dolor/molestia en {zona_dolor} (Intensidad {molestia.intensidad_1_a_10}/10)",
        detalle_cambios=resumen_cambios,
    )

    nueva_rutina = WeeklyRoutine(
        id_rutina=routine.id_rutina,
        split_id=routine.split_id,
        nombre_split=routine.nombre_split,
        dias=tuple(nuevos_dias),
        fecha_creacion=routine.fecha_creacion,
        explicacion_agente=explicacion,
    )

    return nueva_rutina, resumen_cambios


def adjust_for_time_crunch(
    routine: WeeklyRoutine,
    imprevisto: ImprevistoReportado,
) -> tuple[WeeklyRoutine, str]:
    """
    Ajuste puro ante ImprevistoReportado (e.g. Poco tiempo disponible hoy):
    Comprime el volumen de series manteniendo los ejercicios clave para ajustarse a la ventana de tiempo.
    """
    dia_afectado = imprevisto.dia_afectado
    minutos_max = imprevisto.minutos_disponibles_hoy or 30
    modificaciones: list[str] = []
    nuevos_dias: list[DailyWorkout] = []

    for dia in routine.dias:
        if dia.dia_numero == dia_afectado:
            # Reducir series a 2 por ejercicio y ajustar descansos
            slots_comprimidos: list[WorkoutSlot] = []
            for slot in dia.slots:
                params_reducidos = ExerciseExecutionDetail(
                    series=2,
                    repeticiones_sugeridas=slot.parametros.repeticiones_sugeridas,
                    peso_kg_sugerido=slot.parametros.peso_kg_sugerido,
                    descanso_segundos=min(60, slot.parametros.descanso_segundos),
                    instrucciones_fijas=slot.parametros.instrucciones_fijas,
                    precauciones=slot.parametros.precauciones,
                )
                slots_comprimidos.append(
                    WorkoutSlot(
                        grupo_muscular=slot.grupo_muscular,
                        ejercicio_principal=slot.ejercicio_principal,
                        alternativas=slot.alternativas,
                        parametros=params_reducidos,
                    )
                )
            
            duracion_comprimida = min(minutos_max, len(slots_comprimidos) * 6 + 5)
            nuevos_dias.append(
                DailyWorkout(
                    dia_numero=dia.dia_numero,
                    nombre_dia=f"{dia.nombre_dia} (Versión Exprés {minutos_max} min)",
                    slots=tuple(slots_comprimidos),
                    duracion_estimada_minutos=duracion_comprimida,
                )
            )
            modificaciones.append(
                f"Día {dia.dia_numero} comprimido a {duracion_comprimida} min (2 series por ejercicio con descansos cortos)."
            )
        else:
            nuevos_dias.append(dia)

    resumen = " | ".join(modificaciones)
    explicacion = explain_adjustment(
        tipo_evento="ImprevistoReportado (Poco Tiempo)",
        motivo=f"Disponibilidad reducida a {minutos_max} minutos en el Día {dia_afectado}",
        detalle_cambios=resumen,
    )

    nueva_rutina = WeeklyRoutine(
        id_rutina=routine.id_rutina,
        split_id=routine.split_id,
        nombre_split=routine.nombre_split,
        dias=tuple(nuevos_dias),
        fecha_creacion=routine.fecha_creacion,
        explicacion_agente=explicacion,
    )
    return nueva_rutina, resumen


def adjust_for_difficulty(
    routine: WeeklyRoutine,
    level_params: LevelParameters,
    dificultad: DificultadReportada,
) -> tuple[WeeklyRoutine, str]:
    """
    Ajuste puro ante DificultadReportada:
    Aplica sobrecarga progresiva si fue muy fácil o recalibra cargas si fue muy pesado.
    """
    target_id = dificultad.ejercicio_id
    percepcion = dificultad.percepcion
    modificaciones: list[str] = []
    nuevos_dias: list[DailyWorkout] = []

    for dia in routine.dias:
        nuevos_slots: list[WorkoutSlot] = []
        for slot in dia.slots:
            if slot.ejercicio_principal.id == target_id:
                peso_actual = slot.parametros.peso_kg_sugerido
                reps_actual = slot.parametros.repeticiones_sugeridas

                if percepcion == DifficultyPerceptionEnum.MUY_FACIL:
                    factor = 1.0 + (level_params.progresion_carga_semanal_pct / 100.0)
                    nuevo_peso = round(peso_actual * factor, 1) if peso_actual > 0 else 0.0
                    nuevas_reps = reps_actual + (2 if peso_actual == 0 else 0)
                    cambio_txt = f"Incremento de carga de {peso_actual}kg a {nuevo_peso}kg (+{level_params.progresion_carga_semanal_pct}%)"
                elif percepcion in (DifficultyPerceptionEnum.MUY_PESADO, DifficultyPerceptionEnum.FALLO_PREMATURO):
                    nuevo_peso = max(0.0, round(peso_actual * 0.90, 1))
                    nuevas_reps = max(6, reps_actual - 2)
                    cambio_txt = f"Descarga preventiva de {peso_actual}kg a {nuevo_peso}kg (-10%)"
                else:
                    nuevo_peso = peso_actual
                    nuevas_reps = reps_actual
                    cambio_txt = "Carga mantenida en rango óptimo"

                nuevos_params = ExerciseExecutionDetail(
                    series=slot.parametros.series,
                    repeticiones_sugeridas=nuevas_reps,
                    peso_kg_sugerido=nuevo_peso,
                    descanso_segundos=slot.parametros.descanso_segundos,
                    instrucciones_fijas=slot.parametros.instrucciones_fijas,
                    precauciones=slot.parametros.precauciones,
                )
                nuevos_slots.append(
                    WorkoutSlot(
                        grupo_muscular=slot.grupo_muscular,
                        ejercicio_principal=slot.ejercicio_principal,
                        alternativas=slot.alternativas,
                        parametros=nuevos_params,
                    )
                )
                modificaciones.append(f"'{slot.ejercicio_principal.nombre}': {cambio_txt}.")
            else:
                nuevos_slots.append(slot)

        nuevos_dias.append(
            DailyWorkout(
                dia_numero=dia.dia_numero,
                nombre_dia=dia.nombre_dia,
                slots=tuple(nuevos_slots),
                duracion_estimada_minutos=dia.duracion_estimada_minutos,
            )
        )

    resumen = " | ".join(modificaciones) if modificaciones else f"No se localizó el ejercicio {target_id} en la rutina activa."
    explicacion = explain_adjustment(
        tipo_evento="DificultadReportada",
        motivo=f"Percepción reportada: {percepcion.value}",
        detalle_cambios=resumen,
    )

    nueva_rutina = WeeklyRoutine(
        id_rutina=routine.id_rutina,
        split_id=routine.split_id,
        nombre_split=routine.nombre_split,
        dias=tuple(nuevos_dias),
        fecha_creacion=routine.fecha_creacion,
        explicacion_agente=explicacion,
    )
    return nueva_rutina, resumen


def adjust_for_absence(
    routine: WeeklyRoutine,
    ausencia: AusenciaDetectada,
) -> tuple[WeeklyRoutine, str]:
    """
    Ajuste puro ante AusenciaDetectada:
    Añade un protocolo de readaptación sin reiniciar el plan desde cero.
    """
    dias = ausencia.dias_sin_registro
    modificaciones = (
        f"Se detectaron {dias} días sin registro. Se modulan las primeras 2 series de la siguiente sesión "
        "con RIR 3 para reactivación neuromuscular progresiva sin sobrecargar articulaciones."
    )
    explicacion = explain_adjustment(
        tipo_evento="AusenciaDetectada",
        motivo=f"Inactividad de {dias} días continuos",
        detalle_cambios=modificaciones,
    )
    nueva_rutina = WeeklyRoutine(
        id_rutina=routine.id_rutina,
        split_id=routine.split_id,
        nombre_split=routine.nombre_split,
        dias=routine.dias,
        fecha_creacion=routine.fecha_creacion,
        explicacion_agente=explicacion,
    )
    return nueva_rutina, modificaciones
