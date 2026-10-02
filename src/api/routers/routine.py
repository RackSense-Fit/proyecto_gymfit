"""
Router de FastAPI para generación y consulta de la rutina de entrenamiento semanal.
"""
from fastapi import APIRouter, HTTPException
from src.api.state_manager import get_current_timestamp, manager, serialize_dataclass
from src.catalog.filters import get_eligible_catalog
from src.engine.generator import generate_routine
from src.engine.split_selector import select_split_template
from src.models.events import RutinaGenerada

router = APIRouter(prefix="/api/routine", tags=["Rutina"])


@router.post("/generate", summary="Generar o recalcular la rutina semanal")
def generate_weekly_routine() -> dict:
    state = manager.get_state()
    catalog = manager.get_catalog()

    if state.perfil is None:
        raise HTTPException(status_code=400, detail="Debe registrar el perfil de usuario antes de generar la rutina.")
    if not state.equipo_disponible:
        raise HTTPException(status_code=400, detail="Debe registrar al menos un equipo disponible.")

    level_params = catalog.tabla_a_niveles[state.perfil.nivel]
    eligible_exercises = get_eligible_catalog(
        catalog.tabla_b_ejercicios,
        state.equipo_disponible,
        state.perfil.nivel,
        level_params,
    )
    if not eligible_exercises:
        raise HTTPException(
            status_code=422,
            detail="No hay suficientes ejercicios viables con el equipo y nivel seleccionados.",
        )

    split_template = select_split_template(
        catalog.tabla_b_splits,
        state.perfil.dias_disponibles,
        state.perfil.objetivo,
    )

    rutina = generate_routine(
        perfil=state.perfil,
        eligible_catalog=eligible_exercises,
        level_params=level_params,
        split_template=split_template,
        timestamp=get_current_timestamp(),
    )

    evento = RutinaGenerada(rutina=rutina, timestamp=get_current_timestamp())
    manager.dispatch(evento)

    return {
        "message": "Rutina generada con éxito mediante reglas puras.",
        "rutina": serialize_dataclass(rutina),
    }


@router.get("", summary="Obtener la rutina semanal activa")
def get_active_routine() -> dict:
    state = manager.get_state()
    if state.rutina_actual is None:
        raise HTTPException(status_code=404, detail="No existe ninguna rutina activa actualmente.")
    return {
        "rutina": serialize_dataclass(state.rutina_actual),
    }
