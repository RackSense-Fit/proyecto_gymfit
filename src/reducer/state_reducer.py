"""
Función reductora pura de estado para GymFit Agent (Event Sourcing / Pattern Matching).
(EstadoActual, Evento) -> NuevoEstado
Garantiza ausencia total de efectos secundarios y cero mutaciones.
"""
from dataclasses import replace

from src.catalog.filters import get_eligible_catalog
from src.engine.adjuster import (
    adjust_for_absence,
    adjust_for_difficulty,
    adjust_for_discomfort,
    adjust_for_time_crunch,
)
from src.models.catalog import Catalog
from src.models.events import (
    AusenciaDetectada,
    DificultadReportada,
    DomainEvent,
    EquipoActualizado,
    EquipoRegistrado,
    ImprevistoReportado,
    MolestiaReportada,
    PerfilCreado,
    RutinaGenerada,
    SerieRegistrada,
    SesionFinalizada,
    SesionIniciada,
)
from src.models.state import (
    AdjustmentLog,
    AppState,
    CalendarEntry,
    ExerciseSessionLog,
    SessionLog,
    SetLog,
)


def _append_set_to_session(session: SessionLog, serie: SerieRegistrada) -> SessionLog:
    """Función auxiliar pura para anexar una serie a una sesión inmutable."""
    nuevo_set = SetLog(
        numero_serie=serie.numero_serie,
        peso_kg=serie.peso_kg,
        repeticiones=serie.repeticiones,
        descanso_segundos_real=serie.descanso_segundos_real,
    )

    ejercicios_actuales = list(session.ejercicios)
    encontrado = False

    for idx, ex_log in enumerate(ejercicios_actuales):
        if ex_log.ejercicio_id == serie.ejercicio_id:
            # Reemplazar por una nueva tupla con la serie anexada
            nuevas_series = ex_log.series + (nuevo_set,)
            ejercicios_actuales[idx] = ExerciseSessionLog(
                ejercicio_id=ex_log.ejercicio_id,
                series=nuevas_series,
            )
            encontrado = True
            break

    if not encontrado:
        ejercicios_actuales.append(
            ExerciseSessionLog(
                ejercicio_id=serie.ejercicio_id,
                series=(nuevo_set,),
            )
        )

    return SessionLog(
        id_sesion=session.id_sesion,
        dia_numero=session.dia_numero,
        fecha=session.fecha,
        hora_inicio=session.hora_inicio,
        hora_fin=session.hora_fin,
        duracion_total_segundos=session.duracion_total_segundos,
        ejercicios=tuple(ejercicios_actuales),
    )


def reduce_event(
    state: AppState,
    event: DomainEvent,
    catalog: Catalog,
) -> AppState:
    """
    Función pura reductora de estado (Reducer).
    Aplica Structural Pattern Matching (match-case) sobre los tipos discriminados de DomainEvent.
    """
    nuevo_historial_eventos = state.historial_eventos + (event,)

    match event:
        # 1. Configuración de Perfil
        case PerfilCreado(perfil=perfil, timestamp=_):
            return replace(state, perfil=perfil, historial_eventos=nuevo_historial_eventos)

        # 2. Registro de Equipo
        case EquipoRegistrado(equipo=equipo, timestamp=_):
            return replace(state, equipo_disponible=equipo, historial_eventos=nuevo_historial_eventos)

        # 3. Actualización de Equipo
        case EquipoActualizado(nuevo_equipo=nuevo_equipo, timestamp=_):
            return replace(state, equipo_disponible=nuevo_equipo, historial_eventos=nuevo_historial_eventos)

        # 4. Planificación: Rutina Generada
        case RutinaGenerada(rutina=rutina, timestamp=_):
            return replace(state, rutina_actual=rutina, historial_eventos=nuevo_historial_eventos)

        # 5. Sesión: Iniciada
        case SesionIniciada(id_sesion=id_sesion, dia_numero=dia_num, fecha=fecha, hora_inicio=hora_inicio, timestamp=_):
            nueva_sesion = SessionLog(
                id_sesion=id_sesion,
                dia_numero=dia_num,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=None,
                duracion_total_segundos=None,
                ejercicios=(),
            )
            return replace(state, sesion_en_curso=nueva_sesion, historial_eventos=nuevo_historial_eventos)

        # 6. Sesión: Serie Registrada
        case SerieRegistrada() as serie:
            if state.sesion_en_curso is None or state.sesion_en_curso.id_sesion != serie.id_sesion:
                # No hay sesión activa coincidente, registrar el evento sin mutar sesión
                return replace(state, historial_eventos=nuevo_historial_eventos)

            sesion_actualizada = _append_set_to_session(state.sesion_en_curso, serie)
            return replace(state, sesion_en_curso=sesion_actualizada, historial_eventos=nuevo_historial_eventos)

        # 7. Sesión: Finalizada
        case SesionFinalizada(id_sesion=id_sesion, hora_fin=hora_fin, duracion_total_segundos=duracion, timestamp=ts):
            if state.sesion_en_curso is None or state.sesion_en_curso.id_sesion != id_sesion:
                return replace(state, historial_eventos=nuevo_historial_eventos)

            sesion_cerrada = SessionLog(
                id_sesion=state.sesion_en_curso.id_sesion,
                dia_numero=state.sesion_en_curso.dia_numero,
                fecha=state.sesion_en_curso.fecha,
                hora_inicio=state.sesion_en_curso.hora_inicio,
                hora_fin=hora_fin,
                duracion_total_segundos=duracion,
                ejercicios=state.sesion_en_curso.ejercicios,
            )
            nueva_entrada_cal = CalendarEntry(
                fecha_iso=state.sesion_en_curso.fecha,
                completado=True,
                id_sesion=id_sesion,
            )

            return replace(
                state,
                sesion_en_curso=None,
                historial_sesiones=state.historial_sesiones + (sesion_cerrada,),
                calendario=state.calendario + (nueva_entrada_cal,),
                historial_eventos=nuevo_historial_eventos,
            )

        # 8. Variabilidad: Dificultad Reportada
        case DificultadReportada() as dif:
            if state.rutina_actual is None or state.perfil is None:
                return replace(state, historial_eventos=nuevo_historial_eventos)

            level_params = catalog.tabla_a_niveles[state.perfil.nivel]
            rutina_ajustada, detalle = adjust_for_difficulty(state.rutina_actual, level_params, dif)
            ajuste_log = AdjustmentLog(
                timestamp=dif.timestamp,
                motivo=f"Dificultad '{dif.percepcion.value}' reportada en {dif.ejercicio_id}",
                detalle_ajuste=detalle,
                evento_causante_tipo="DificultadReportada",
            )

            return replace(
                state,
                rutina_actual=rutina_ajustada,
                historial_ajustes=state.historial_ajustes + (ajuste_log,),
                historial_eventos=nuevo_historial_eventos,
            )

        # 9. Variabilidad: Molestia Reportada
        case MolestiaReportada() as mol:
            if state.rutina_actual is None or state.perfil is None:
                return replace(state, historial_eventos=nuevo_historial_eventos)

            level_params = catalog.tabla_a_niveles[state.perfil.nivel]
            eligible = get_eligible_catalog(
                catalog.tabla_b_ejercicios,
                state.equipo_disponible,
                state.perfil.nivel,
                level_params,
            )
            rutina_ajustada, detalle = adjust_for_discomfort(
                state.rutina_actual,
                eligible,
                level_params,
                state.perfil,
                mol,
            )
            ajuste_log = AdjustmentLog(
                timestamp=mol.timestamp,
                motivo=f"Molestia en {mol.zona_articular} (Intensidad {mol.intensidad_1_a_10}/10)",
                detalle_ajuste=detalle,
                evento_causante_tipo="MolestiaReportada",
            )

            return replace(
                state,
                rutina_actual=rutina_ajustada,
                historial_ajustes=state.historial_ajustes + (ajuste_log,),
                historial_eventos=nuevo_historial_eventos,
            )

        # 10. Variabilidad: Imprevisto Reportado
        case ImprevistoReportado() as imp:
            if state.rutina_actual is None:
                return replace(state, historial_eventos=nuevo_historial_eventos)

            rutina_ajustada, detalle = adjust_for_time_crunch(state.rutina_actual, imp)
            ajuste_log = AdjustmentLog(
                timestamp=imp.timestamp,
                motivo=f"Imprevisto de tipo '{imp.tipo.value}' en Día {imp.dia_afectado}",
                detalle_ajuste=detalle,
                evento_causante_tipo="ImprevistoReportado",
            )

            return replace(
                state,
                rutina_actual=rutina_ajustada,
                historial_ajustes=state.historial_ajustes + (ajuste_log,),
                historial_eventos=nuevo_historial_eventos,
            )

        # 11. Variabilidad: Ausencia Detectada
        case AusenciaDetectada() as aus:
            if state.rutina_actual is None:
                return replace(state, historial_eventos=nuevo_historial_eventos)

            rutina_ajustada, detalle = adjust_for_absence(state.rutina_actual, aus)
            ajuste_log = AdjustmentLog(
                timestamp=aus.timestamp,
                motivo=f"Inactividad de {aus.dias_sin_registro} días detectada",
                detalle_ajuste=detalle,
                evento_causante_tipo="AusenciaDetectada",
            )

            return replace(
                state,
                rutina_actual=rutina_ajustada,
                historial_ajustes=state.historial_ajustes + (ajuste_log,),
                historial_eventos=nuevo_historial_eventos,
            )

        case _:
            # Caso residual seguro
            return replace(state, historial_eventos=nuevo_historial_eventos)

