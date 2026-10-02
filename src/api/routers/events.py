"""
Router de FastAPI para consultas globales de estado, carga de fixtures demo y Event Sourcing.
"""
from fastapi import APIRouter
from src.api.state_manager import get_current_timestamp, manager, serialize_dataclass
from src.catalog.filters import get_eligible_catalog
from src.engine.generator import generate_routine
from src.engine.split_selector import select_split_template
from src.models.enums import GoalEnum, LevelEnum, SexEnum
from src.models.events import EquipoRegistrado, PerfilCreado, RutinaGenerada
from src.models.profile import UserProfile

router = APIRouter(prefix="/api/state", tags=["Estado y Event Sourcing"])


@router.get("", summary="Obtener el estado inmutable completo (AppState)")
def get_full_state() -> dict:
    state = manager.get_state()
    return {
        "state": serialize_dataclass(state),
    }


@router.post("/reset", summary="Reiniciar estado a limpio (para pruebas)")
def reset_state() -> dict:
    state = manager.reset_state()
    return {
        "message": "Estado reiniciado exitosamente a AppState limpio.",
        "state": serialize_dataclass(state),
    }


@router.get("/events", summary="Obtener la traza histórica completa de eventos")
def get_event_history() -> dict:
    state = manager.get_state()
    return {
        "total_eventos": len(state.historial_eventos),
        "eventos": [
            {
                "tipo": type(ev).__name__,
                "datos": serialize_dataclass(ev),
            }
            for ev in state.historial_eventos
        ],
    }


@router.post("/seed", summary="Precargar un caso demo completo (Perfil + Equipo + Rutina)")
def seed_demo_data() -> dict:
    """Precarga en 1 clic un escenario funcional listo para pruebas y demostraciones."""
    catalog = manager.get_catalog()
    manager.reset_state()

    # 1. Perfil demo
    perfil = UserProfile(
        nombre="Carlos Mendoza",
        sexo=SexEnum.MASCULINO,
        peso_kg=76.0,
        altura_cm=178.0,
        objetivo=GoalEnum.GANAR_MUSCULO,
        nivel=LevelEnum.PRINCIPIANTE,
        dias_disponibles=3,
    )
    ts = get_current_timestamp()
    manager.dispatch(PerfilCreado(perfil=perfil, timestamp=ts))

    # 2. Equipo demo
    equipo = frozenset({"mancuernas", "banco_plano", "barra_dominadas", "peso_corporal"})
    manager.dispatch(EquipoRegistrado(equipo=equipo, timestamp=ts))

    # 3. Generar rutina pura
    level_params = catalog.tabla_a_niveles[perfil.nivel]
    eligible = get_eligible_catalog(catalog.tabla_b_ejercicios, equipo, perfil.nivel, level_params)
    split = select_split_template(catalog.tabla_b_splits, perfil.dias_disponibles, perfil.objetivo)
    rutina = generate_routine(perfil, eligible, level_params, split, ts)
    state = manager.dispatch(RutinaGenerada(rutina=rutina, timestamp=ts))

    return {
        "message": "Caso demo precargado con éxito en el estado inmutable.",
        "state": serialize_dataclass(state),
    }
