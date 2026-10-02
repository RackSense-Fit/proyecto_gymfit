"""
Router de FastAPI para registro y consulta de equipo disponible en el gimnasio.
"""
from fastapi import APIRouter
from src.api.schemas import EquipmentRegisterRequest
from src.api.state_manager import get_current_timestamp, manager, serialize_dataclass
from src.catalog.filters import get_eligible_catalog
from src.models.events import EquipoActualizado, EquipoRegistrado

router = APIRouter(prefix="/api/equipment", tags=["Equipo"])


@router.post("", summary="Registrar o actualizar inventario de equipo disponible")
def register_equipment(req: EquipmentRegisterRequest) -> dict:
    nuevo_equipo = frozenset(req.equipo)
    timestamp = get_current_timestamp()

    state = manager.get_state()
    if not state.equipo_disponible:
        evento = EquipoRegistrado(equipo=nuevo_equipo, timestamp=timestamp)
    else:
        evento = EquipoActualizado(nuevo_equipo=nuevo_equipo, timestamp=timestamp)

    state_actualizado = manager.dispatch(evento)

    return {
        "message": f"Equipo {'registrado' if isinstance(evento, EquipoRegistrado) else 'actualizado'} con éxito.",
        "equipo_disponible": sorted(list(state_actualizado.equipo_disponible)),
    }


@router.get("", summary="Consultar equipo disponible y ejercicios viables")
def get_equipment_status() -> dict:
    state = manager.get_state()
    catalog = manager.get_catalog()

    viable_count = 0
    if state.perfil is not None:
        level_params = catalog.tabla_a_niveles[state.perfil.nivel]
        eligible = get_eligible_catalog(
            catalog.tabla_b_ejercicios,
            state.equipo_disponible,
            state.perfil.nivel,
            level_params,
        )
        viable_count = len(eligible)

    return {
        "equipo_disponible": sorted(list(state.equipo_disponible)),
        "ejercicios_viables_count": viable_count,
        "total_ejercicios_catalogo": len(catalog.tabla_b_ejercicios),
    }


@router.get("/catalog", summary="Listar catálogo universal de tipos de equipo")
def get_equipment_catalog() -> dict:
    catalog = manager.get_catalog()
    all_eq = set()
    for ex in catalog.tabla_b_ejercicios:
        all_eq.update(ex.equipo_requerido)
    return {
        "equipos_conocidos": sorted(list(all_eq)),
    }
