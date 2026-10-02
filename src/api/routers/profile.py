"""
Router de FastAPI para gestión de perfil de usuario.
"""
from fastapi import APIRouter, HTTPException
from src.api.schemas import ProfileCreateRequest
from src.api.state_manager import get_current_timestamp, manager, serialize_dataclass
from src.models.events import PerfilCreado
from src.models.profile import UserProfile

router = APIRouter(prefix="/api/profile", tags=["Perfil"])


@router.post("", summary="Crear o actualizar perfil del usuario")
def create_profile(req: ProfileCreateRequest) -> dict:
    try:
        perfil = UserProfile(
            nombre=req.nombre,
            sexo=req.sexo,
            peso_kg=req.peso_kg,
            altura_cm=req.altura_cm,
            objetivo=req.objetivo,
            nivel=req.nivel,
            dias_disponibles=req.dias_disponibles,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    evento = PerfilCreado(perfil=perfil, timestamp=get_current_timestamp())
    manager.dispatch(evento)

    return {
        "message": "Perfil registrado con éxito mediante evento inmutable PerfilCreado.",
        "perfil": serialize_dataclass(perfil),
        "imc": perfil.imc,
    }


@router.get("", summary="Obtener perfil actual")
def get_profile() -> dict:
    state = manager.get_state()
    if state.perfil is None:
        raise HTTPException(status_code=404, detail="No se ha creado ningún perfil aún.")
    return {
        "perfil": serialize_dataclass(state.perfil),
        "imc": state.perfil.imc,
    }
