"""
Paquete de Reducción de Estado y Event Sourcing de GymFit Agent.
"""
from src.reducer.history_fold import fold_events
from src.reducer.state_reducer import reduce_event

__all__ = [
    "reduce_event",
    "fold_events",
]
