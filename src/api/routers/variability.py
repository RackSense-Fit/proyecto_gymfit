"""
Router de FastAPI para reportar eventos de variabilidad y adaptaciones en tiempo real.
"""
from fastapi import APIRouter, HTTPException
from src.api.schemas import (
    ReportDifficultyRequest,
    ReportDiscomfortRequest,
    ReportTimeCrunchRequest,
)
from src.api.state_manager import get_current_timestamp, manager, serialize_dataclass
from src.models.events import (
    DificultadReportada,
    ImprevistoReportado,
    MolestiaReportada,
)

router = APIRouter(prefix="/api/adjustments", tags=["Adaptaciones y Variabilidad"])


@router.post("/discomfort", summary="Reportar molestia articular para adaptación reactiva")
def report_discomfort(req: ReportDiscomfortRequest) -> dict:
    state = manager.get_state()
    if state.rutina_actual is None:
        raise HTTPException(status_code=400, detail="Debe existir una rutina activa para aplicar adaptaciones.")

    evento = MolestiaReportada(
        zona_articular=req.zona_articular,
        intensidad_1_a_10=req.intensidad_1_a_10,
        ejercicio_origen_id=req.ejercicio_origen_id,
        timestamp=get_current_timestamp(),
    )
    state_actualizado = manager.dispatch(evento)
    ultimo_ajuste = state_actualizado.historial_ajustes[-1] if state_actualizado.historial_ajustes else None

    return {
        "message": "Molestia procesada y rutina reajustada de forma pura.",
        "ajuste": serialize_dataclass(ultimo_ajuste),
        "explicacion_agente": state_actualizado.rutina_actual.explicacion_agente,
    }


@router.post("/time-crunch", summary="Reportar falta de tiempo para versión exprés")
def report_time_crunch(req: ReportTimeCrunchRequest) -> dict:
    state = manager.get_state()
    if state.rutina_actual is None:
        raise HTTPException(status_code=400, detail="Debe existir una rutina activa para aplicar adaptaciones.")

    evento = ImprevistoReportado(
        tipo=req.tipo,
        dia_afectado=req.dia_afectado,
        minutos_disponibles_hoy=req.minutos_disponibles_hoy,
        detalle=req.detalle,
        timestamp=get_current_timestamp(),
    )
    state_actualizado = manager.dispatch(evento)
    ultimo_ajuste = state_actualizado.historial_ajustes[-1] if state_actualizado.historial_ajustes else None

    return {
        "message": "Rutina adaptada a versión exprés según la ventana de tiempo disponible.",
        "ajuste": serialize_dataclass(ultimo_ajuste),
        "explicacion_agente": state_actualizado.rutina_actual.explicacion_agente,
    }


@router.post("/difficulty", summary="Reportar dificultad para sobrecarga o descarga progresiva")
def report_difficulty(req: ReportDifficultyRequest) -> dict:
    state = manager.get_state()
    if state.rutina_actual is None:
        raise HTTPException(status_code=400, detail="Debe existir una rutina activa para aplicar adaptaciones.")

    evento = DificultadReportada(
        ejercicio_id=req.ejercicio_id,
        percepcion=req.percepcion,
        comentarios=req.comentarios,
        timestamp=get_current_timestamp(),
    )
    state_actualizado = manager.dispatch(evento)
    ultimo_ajuste = state_actualizado.historial_ajustes[-1] if state_actualizado.historial_ajustes else None

    return {
        "message": "Dificultad procesada. Parámetros de carga y repeticiones actualizados.",
        "ajuste": serialize_dataclass(ultimo_ajuste),
        "explicacion_agente": state_actualizado.rutina_actual.explicacion_agente,
    }


@router.get("/history", summary="Consultar historial completo de adaptaciones y explicaciones")
def get_adjustments_history() -> dict:
    state = manager.get_state()
    return {
        "total_ajustes": len(state.historial_ajustes),
        "historial_ajustes": serialize_dataclass(state.historial_ajustes),
    }
