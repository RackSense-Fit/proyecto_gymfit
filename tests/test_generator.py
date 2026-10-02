"""
Pruebas unitarias para el generador funcional de rutinas y selector de splits.
"""
from pathlib import Path
import unittest
from src.catalog.loader import load_full_catalog
from src.catalog.filters import get_eligible_catalog
from src.engine.generator import generate_routine
from src.engine.split_selector import select_split_template
from src.models.enums import GoalEnum, LevelEnum, SexEnum
from src.models.profile import UserProfile


class TestRoutineGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        data_dir = Path(__file__).parent.parent / "data"
        cls.catalog = load_full_catalog(data_dir)

    def test_split_selection(self) -> None:
        # 3 días -> fullbody_3dias
        s3 = select_split_template(self.catalog.tabla_b_splits, 3, GoalEnum.GANAR_MUSCULO)
        self.assertEqual(s3.id, "fullbody_3dias")

        # 4 días -> upper_lower_4dias
        s4 = select_split_template(self.catalog.tabla_b_splits, 4, GoalEnum.BAJAR_GRASA)
        self.assertEqual(s4.id, "upper_lower_4dias")

        # 5 días -> push_pull_legs_5dias
        s5 = select_split_template(self.catalog.tabla_b_splits, 5, GoalEnum.FUERZA)
        self.assertEqual(s5.id, "push_pull_legs_5dias")

    def test_generate_routine_integrity(self) -> None:
        perfil = UserProfile(
            nombre="Ana",
            sexo=SexEnum.FEMENINO,
            peso_kg=60.0,
            altura_cm=165.0,
            objetivo=GoalEnum.GANAR_MUSCULO,
            nivel=LevelEnum.PRINCIPIANTE,
            dias_disponibles=3,
        )
        equipo = frozenset({"mancuernas", "banco_plano", "polea", "peso_corporal"})
        params = self.catalog.tabla_a_niveles[perfil.nivel]
        eligible = get_eligible_catalog(self.catalog.tabla_b_ejercicios, equipo, perfil.nivel, params)
        split = select_split_template(self.catalog.tabla_b_splits, perfil.dias_disponibles, perfil.objetivo)

        routine = generate_routine(perfil, eligible, params, split, "2026-09-18")

        self.assertEqual(len(routine.dias), 3)
        self.assertIsNotNone(routine.explicacion_agente)
        
        # Verificar que todos los ejercicios asignados usan exclusivamente equipo disponible
        for dia in routine.dias:
            for slot in dia.slots:
                ex = slot.ejercicio_principal
                self.assertTrue(ex.equipo_requerido.issubset(equipo | {"peso_corporal"}))
                # Verificar que las instrucciones fijas provienen del catálogo
                self.assertEqual(slot.parametros.instrucciones_fijas, ex.instrucciones_fijas)

    def test_advanced_level_series_range(self) -> None:
        """Verifica que el nivel avanzado tenga rango de series [4, 6]."""
        params_adv = self.catalog.tabla_a_niveles[LevelEnum.AVANZADO]
        self.assertEqual(params_adv.rango_series_por_ejercicio, (4, 6))

    def test_series_and_rest_by_goal(self) -> None:
        """Verifica que las series y descansos se calculen en función del objetivo."""
        from src.engine.generator import build_execution_detail, calculate_rest_seconds

        ex = self.catalog.tabla_b_ejercicios[0]
        params_intermedio = self.catalog.tabla_a_niveles[LevelEnum.INTERMEDIO] # rango_series: (3, 4)

        # 1. FUERZA -> series límite superior (4), descanso 240s
        p_fuerza = UserProfile("Test", SexEnum.MASCULINO, 75.0, 175.0, GoalEnum.FUERZA, LevelEnum.INTERMEDIO, 3)
        detail_fuerza = build_execution_detail(ex, p_fuerza, params_intermedio)
        self.assertEqual(detail_fuerza.series, 4)
        self.assertEqual(detail_fuerza.descanso_segundos, 240)
        self.assertEqual(calculate_rest_seconds(p_fuerza, params_intermedio), 240)

        # 2. BAJAR_GRASA -> series límite inferior (3), descanso 30s
        p_grasa = UserProfile("Test", SexEnum.MASCULINO, 75.0, 175.0, GoalEnum.BAJAR_GRASA, LevelEnum.INTERMEDIO, 3)
        detail_grasa = build_execution_detail(ex, p_grasa, params_intermedio)
        self.assertEqual(detail_grasa.series, 3)
        self.assertEqual(detail_grasa.descanso_segundos, 30)
        self.assertEqual(calculate_rest_seconds(p_grasa, params_intermedio), 30)

        # 3. GANAR_MUSCULO -> series promedio (3+4)//2 = 3, descanso 150s
        p_musculo = UserProfile("Test", SexEnum.MASCULINO, 75.0, 175.0, GoalEnum.GANAR_MUSCULO, LevelEnum.INTERMEDIO, 3)
        detail_musculo = build_execution_detail(ex, p_musculo, params_intermedio)
        self.assertEqual(detail_musculo.series, 3)
        self.assertEqual(detail_musculo.descanso_segundos, 150)
        self.assertEqual(calculate_rest_seconds(p_musculo, params_intermedio), 150)

        # 4. MANTENIMIENTO -> series promedio (3+4)//2 = 3, descanso 60s
        p_mant = UserProfile("Test", SexEnum.MASCULINO, 75.0, 175.0, GoalEnum.MANTENIMIENTO, LevelEnum.INTERMEDIO, 3)
        detail_mant = build_execution_detail(ex, p_mant, params_intermedio)
        self.assertEqual(detail_mant.series, 3)
        self.assertEqual(detail_mant.descanso_segundos, 60)
        self.assertEqual(calculate_rest_seconds(p_mant, params_intermedio), 60)


if __name__ == "__main__":
    unittest.main()

