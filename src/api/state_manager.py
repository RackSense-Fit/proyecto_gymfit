"""
Gestor de estado para la API de FastAPI.
Aplica principios funcionales: el estado global solo evoluciona invocando la función pura reduce_event.
"""
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any
from src.catalog.loader import load_full_catalog
from src.models.catalog import Catalog
from src.models.events import DomainEvent
from src.models.state import AppState
from src.reducer.state_reducer import reduce_event


class RuntimeStateManager:
    """Contenedor en memoria del catálogo estático y del estado inmutable actual."""
    def __init__(self, data_dir: Path | str | None = None) -> None:
        if data_dir is None:
            data_dir = Path(__file__).resolve().parent.parent.parent / "data"
        self.catalog: Catalog = load_full_catalog(data_dir)
        self.state: AppState = AppState()

    def get_catalog(self) -> Catalog:
        return self.catalog

    def get_state(self) -> AppState:
        return self.state

    def reset_state(self) -> AppState:
        """Reinicia el estado a una instancia limpia (AppState vacío)."""
        self.state = AppState()
        return self.state

    def dispatch(self, event: DomainEvent) -> AppState:
        """Aplica la reducción funcional pura: S_nuevo = reduce_event(S_actual, Evento)."""
        self.state = reduce_event(self.state, event, self.catalog)
        return self.state


# Instancia única para el ciclo de vida del servidor
manager = RuntimeStateManager()


def get_current_timestamp() -> str:
    """Retorna la fecha y hora ISO actual."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def serialize_dataclass(obj: Any) -> Any:
    """Convierte dataclasses inmutables y frozensets a estructuras serializables en JSON."""
    if obj is None:
        return None
    if isinstance(obj, frozenset):
        return sorted(list(obj))
    if isinstance(obj, (tuple, list)):
        return [serialize_dataclass(item) for item in obj]
    if hasattr(obj, "__dataclass_fields__"):
        result = {}
        for k, v in asdict(obj).items():
            result[k] = serialize_dataclass(getattr(obj, k))
        return result
    return obj
