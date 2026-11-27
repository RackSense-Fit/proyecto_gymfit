"""
Router de FastAPI para registro y consulta de equipo disponible en el gimnasio.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import APIRouter, File, HTTPException, UploadFile
from src.api.schemas import EquipmentRegisterRequest
from src.api.state_manager import get_current_timestamp, manager, serialize_dataclass
from src.catalog.filters import get_eligible_catalog
from src.catalog.loader import load_equipment_vocabulary
from src.config.settings import load_settings
from src.models.events import EquipoActualizado, EquipoRegistrado
from src.vision.equipment_analyzer import (
    AnalisisEquipoResponse,
    analyze_gym_image,
    equipment_ids_only,
)

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_ENV_PATH = _PROJECT_ROOT / ".env"
_VOCAB_PATH = _PROJECT_ROOT / "data" / "equipment_vocabulary.json"
_SYSTEM_PROMPT_PATH = _PROJECT_ROOT / "data" / "prompts" / "equipment_system_prompt.txt"
_USER_PROMPT_PATH = _PROJECT_ROOT / "data" / "prompts" / "equipment_user_prompt.txt"

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


@router.post("/analyze-image", summary="Analizar foto de gimnasio con Gemini Vision")
async def analyze_equipment_image(file: UploadFile = File(...)) -> dict:
    """
    Recibe una imagen (bytes) y utiliza Gemini con Structured Outputs
    para identificar equipamiento compatible con el catálogo de GymFit.
    """
    try:
        load_dotenv(_ENV_PATH)
        api_key = os.getenv("GEMINI_API_KEY", "")
        settings = load_settings(_ENV_PATH)
        vocabulario = load_equipment_vocabulary(_VOCAB_PATH)
        system_prompt = _SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
        user_prompt = _USER_PROMPT_PATH.read_text(encoding="utf-8")

        image_bytes = await file.read()
        mime_type = file.content_type or "image/jpeg"
        resultado: AnalisisEquipoResponse = analyze_gym_image(
            image_bytes,
            mime_type,
            settings=settings,
            vocabulario=vocabulario,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            api_key=api_key,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return {
        "resumen": resultado.resumen,
        "equipos_detectados": [eq.model_dump() for eq in resultado.equipos_detectados],
        "equipment_ids": equipment_ids_only(resultado),
    }
