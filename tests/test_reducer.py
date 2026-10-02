"""
Pruebas unitarias para el Reductor Puro de Estado y Event Sourcing (Fold).
"""
from pathlib import Path
import unittest
from src.catalog.loader import load_full_catalog
from src.catalog.filters import get_eligible_catalog
from src.engine.generator import generate_routine
from src.engine.split_selector import select_split_template
from src.models.enums import (
    DifficultyPerceptionEnum,
    GoalEnum,
    LevelEnum,
    SexEnum,
    UnforeseenTypeEnum,
)
from src.models.events import (
    DificultadReportada,
    EquipoRegistrado,
    ImprevistoReportado,
    MolestiaReportada,
    PerfilCreado,
    RutinaGenerada,
    SerieRegistrada,
    SesionFinalizada,
    SesionIniciada,
)
from src.models.profile import UserProfile
from src.models.state import AppState
from src.reducer.history_fold import fold_events
from src.reducer.state_reducer import reduce_event


class TestStateReducerAndFold(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        data_dir = Path(__file__).parent.parent / "data"
        cls.catalog = load_full_catalog(data_dir)

    def test_state_immutability_and_events(self) -> None:
        state0 = AppState()
        
        perfil = UserProfile("Luis", SexEnum.MASCULINO, 70.0, 175.0, GoalEnum.MANTENIMIENTO, LevelEnum.PRINCIPIANTE, 3)
        ev_p = PerfilCreado(perfil, "2026-09-18 10:00:00")
        state1 = reduce_event(state0, ev_p, self.catalog)

        # Inmutabilidad: state0 no debe modificarse
        self.assertIsNone(state0.perfil)
        self.assertEqual(len(state0.historial_eventos), 0)

        # state1 debe tener el perfil
        self.assertEqual(state1.perfil, perfil)
        self.assertEqual(len(state1.historial_eventos), 1)

    def test_session_lifecycle(self) -> None:
        state = AppState()
        ev_ini = SesionIniciada("s1", 1, "2026-09-18", "10:00:00", "2026-09-18 10:00:00")
        state = reduce_event(state, ev_ini, self.catalog)
        self.assertIsNotNone(state.sesion_en_curso)

        ev_set = SerieRegistrada("s1", "press_banca_barra", 1, 50.0, 10, 90, "2026-09-18 10:05:00")
        state = reduce_event(state, ev_set, self.catalog)
        self.assertEqual(len(state.sesion_en_curso.ejercicios), 1)
        self.assertEqual(len(state.sesion_en_curso.ejercicios[0].series), 1)

        ev_fin = SesionFinalizada("s1", "10:45:00", 2700, "2026-09-18 10:45:00")
        state = reduce_event(state, ev_fin, self.catalog)
        self.assertIsNone(state.sesion_en_curso)
        self.assertEqual(state.total_sesiones_completadas, 1)
        self.assertEqual(state.dias_entrenados_mes_actual, 1)

    def test_fold_equivalence(self) -> None:
        perfil = UserProfile("David", SexEnum.MASCULINO, 80.0, 180.0, GoalEnum.GANAR_MUSCULO, LevelEnum.INTERMEDIO, 4)
        equipo = frozenset({"mancuernas", "banco_plano", "barra", "peso_corporal"})
        
        params = self.catalog.tabla_a_niveles[perfil.nivel]
        eligible = get_eligible_catalog(self.catalog.tabla_b_ejercicios, equipo, perfil.nivel, params)
        split = select_split_template(self.catalog.tabla_b_splits, perfil.dias_disponibles, perfil.objetivo)
        rutina = generate_routine(perfil, eligible, params, split, "2026-09-18")

        events = [
            PerfilCreado(perfil, "ts1"),
            EquipoRegistrado(equipo, "ts2"),
            RutinaGenerada(rutina, "ts3"),
            MolestiaReportada("hombro", 5, "press_plano_mancuernas", "ts4"),
            ImprevistoReportado(UnforeseenTypeEnum.POCO_TIEMPO, 1, 20, "Prisa", "ts5"),
        ]

        # Reducción paso a paso
        step_state = AppState()
        for ev in events:
            step_state = reduce_event(step_state, ev, self.catalog)

        # Reducción con fold_events
        folded_state = fold_events(AppState(), events, self.catalog)

        # Deben ser idénticos
        self.assertEqual(step_state.perfil, folded_state.perfil)
        self.assertEqual(step_state.equipo_disponible, folded_state.equipo_disponible)
        self.assertEqual(len(step_state.historial_ajustes), len(folded_state.historial_ajustes))
        self.assertEqual(len(step_state.historial_eventos), len(folded_state.historial_eventos))


if __name__ == "__main__":
    unittest.main()
