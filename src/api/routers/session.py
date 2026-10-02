"""
Router de FastAPI para registro en vivo de sesiones de entrenamiento y series.
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException
from src.api.schemas import SessionFinishRequest, SessionStartRequest, SetRecordRequest
from src.api.state_manager import get_current_timestamp, manager, serialize_dataclass
from src.models.events import SerieRegistrada, SesionFinalizada, SesionIniciada

router = APIRouter(prefix="/api/session", tags=["Sesión de Entrenamiento"])


@router.post("/start", summary="Iniciar una sesión de entrenamiento")
def start_session(req: SessionStartRequest) -> dict:
    state = manager.get_state()
    if state.sesion_en_curso is not None:
        raise HTTPException(
            status_code=409,
            detail=f"Ya existe una sesión activa con ID '{state.sesion_en_curso.id_sesion}'. Finalícela primero.",
        )

    now = datetime.now()
    fecha = req.fecha or now.strftime("%Y-%m-%d")
    hora_inicio = req.hora_inicio or now.strftime("%H:%M:%S")
    id_sesion = f"sesion_{now.strftime('%Y%m%d_%H%M%S')}"

    evento = SesionIniciada(
        id_sesion=id_sesion,
        dia_numero=req.dia_numero,
        fecha=fecha,
        hora_inicio=hora_inicio,
        timestamp=get_current_timestamp(),
    )
    manager.dispatch(evento)

    return {
        "message": "Sesión iniciada con éxito.",
        "id_sesion": id_sesion,
        "dia_numero": req.dia_numero,
        "hora_inicio": hora_inicio,
    }


@router.post("/set", summary="Registrar una serie completada con cronómetro de descanso")
def record_set(req: SetRecordRequest) -> dict:
    state = manager.get_state()
    if state.sesion_en_curso is None or state.sesion_en_curso.id_sesion != req.id_sesion:
        raise HTTPException(status_code=404, detail="No se encontró una sesión activa coincidente.")

    evento = SerieRegistrada(
        id_sesion=req.id_sesion,
        ejercicio_id=req.ejercicio_id,
        numero_serie=req.numero_serie,
        peso_kg=req.peso_kg,
        repeticiones=req.repeticiones,
        descanso_segundos_real=req.descanso_segundos_real,
        timestamp=get_current_timestamp(),
    )
    state_actualizado = manager.dispatch(evento)

    return {
        "message": "Serie registrada con éxito en la sesión activa.",
        "sesion_actual": serialize_dataclass(state_actualizado.sesion_en_curso),
    }


@router.post("/finish", summary="Finalizar la sesión de entrenamiento actual")
def finish_session(req: SessionFinishRequest) -> dict:
    state = manager.get_state()
    if state.sesion_en_curso is None or state.sesion_en_curso.id_sesion != req.id_sesion:
        raise HTTPException(status_code=404, detail="No se encontró una sesión activa coincidente.")

    hora_fin = req.hora_fin or datetime.now().strftime("%H:%M:%S")

    evento = SesionFinalizada(
        id_sesion=req.id_sesion,
        hora_fin=hora_fin,
        duracion_total_segundos=req.duracion_total_segundos,
        timestamp=get_current_timestamp(),
    )
    state_actualizado = manager.dispatch(evento)

    return {
        "message": "Sesión finalizada exitosamente. Calendario actualizado.",
        "total_sesiones_completadas": state_actualizado.total_sesiones_completadas,
        "dias_entrenados_mes": state_actualizado.dias_entrenados_mes_actual,
    }


@router.get("/active", summary="Consultar el estado de la sesión activa")
def get_active_session() -> dict:
    state = manager.get_state()
    if state.sesion_en_curso is None:
        return {"sesion_activa": None, "activa": False}
    return {
        "sesion_activa": serialize_dataclass(state.sesion_en_curso),
        "activa": True,
    }


@router.get("/history", summary="Consultar historial de sesiones y calendario")
def get_session_history() -> dict:
    state = manager.get_state()
    return {
        "total_sesiones": state.total_sesiones_completadas,
        "dias_entrenados_mes": state.dias_entrenados_mes_actual,
        "calendario": serialize_dataclass(state.calendario),
        "historial_sesiones": serialize_dataclass(state.historial_sesiones),
    }
