"""
Reconstrucción determinista del estado mediante Fold / Reducción Funcional (functools.reduce).
S_final = fold_left(reduce_event, eventos, S_inicial)
"""
from functools import reduce
from typing import Sequence
from src.models.catalog import Catalog
from src.models.events import DomainEvent
from src.models.state import AppState
from src.reducer.state_reducer import reduce_event


def fold_events(
    initial_state: AppState,
    events: Sequence[DomainEvent],
    catalog: Catalog,
) -> AppState:
    """
    Función de orden superior que reduce (foldl) una secuencia ordenada de eventos
    sobre el estado inmutable inicial.
    
    Demuestra la propiedad matemática de Event Sourcing en Programación Funcional:
    Cualquier estado histórico S_t se obtiene de forma pura evaluando fold(S_0, E_1..t).
    """
    return reduce(
        lambda current_state, event: reduce_event(current_state, event, catalog),
        events,
        initial_state,
    )
