"""
Pruebas unitarias para los filtros puros de catálogo.
"""
import unittest
from src.catalog.filters import (
    filter_by_equipment,
    filter_by_joint_safety,
    filter_by_level,
    filter_by_muscle_group,
    get_eligible_catalog,
)
from src.models.catalog import Exercise, LevelParameters
from src.models.enums import (
    LevelEnum,
    MovementPatternEnum,
    MuscleGroupEnum,
    RiskLevelEnum,
)


class TestCatalogFilters(unittest.TestCase):
    def setUp(self) -> None:
        self.ex1_banca = Exercise(
            id="press_banca_barra",
            nombre="Press de Banca",
            grupo_muscular=MuscleGroupEnum.PECHO,
            patron_movimiento=MovementPatternEnum.EMPUJE,
            equipo_requerido=frozenset({"barra", "banco_plano"}),
            nivel_minimo=LevelEnum.PRINCIPIANTE,
            nivel_riesgo=RiskLevelEnum.MEDIO,
            articulaciones_comprometidas=frozenset({"hombro", "codo"}),
            instrucciones_fijas=("Instrucción 1",),
            errores_comunes=("Error 1",),
            precauciones_seguridad=("Precaución 1",),
        )
        self.ex2_pushup = Exercise(
            id="flexiones_suelo",
            nombre="Flexiones de Pecho",
            grupo_muscular=MuscleGroupEnum.PECHO,
            patron_movimiento=MovementPatternEnum.EMPUJE,
            equipo_requerido=frozenset({"peso_corporal"}),
            nivel_minimo=LevelEnum.PRINCIPIANTE,
            nivel_riesgo=RiskLevelEnum.BAJO,
            articulaciones_comprometidas=frozenset({"muñeca", "codo"}),
            instrucciones_fijas=("Instrucción pushup",),
            errores_comunes=(),
            precauciones_seguridad=(),
        )
        self.ex3_avanzado = Exercise(
            id="sentadilla_trasera",
            nombre="Sentadilla",
            grupo_muscular=MuscleGroupEnum.CUADRICEPS,
            patron_movimiento=MovementPatternEnum.DOMINANTE_RODILLA,
            equipo_requerido=frozenset({"barra"}),
            nivel_minimo=LevelEnum.AVANZADO,
            nivel_riesgo=RiskLevelEnum.ALTO,
            articulaciones_comprometidas=frozenset({"rodilla", "lumbar"}),
            instrucciones_fijas=(),
            errores_comunes=(),
            precauciones_seguridad=(),
        )
        self.catalog = (self.ex1_banca, self.ex2_pushup, self.ex3_avanzado)

    def test_filter_by_equipment(self) -> None:
        # Solo peso corporal disponible
        res = filter_by_equipment(self.catalog, frozenset({"peso_corporal"}))
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].id, "flexiones_suelo")

        # Barra y banco disponibles
        res2 = filter_by_equipment(self.catalog, frozenset({"barra", "banco_plano"}))
        self.assertEqual(len(res2), 3) # Incluye peso corporal por defecto

    def test_filter_by_level(self) -> None:
        # Principiante no debe tener acceso a sentadilla avanzada
        res = filter_by_level(self.catalog, LevelEnum.PRINCIPIANTE)
        self.assertEqual(len(res), 2)
        self.assertNotIn(self.ex3_avanzado, res)

        # Avanzado tiene acceso a todo
        res_adv = filter_by_level(self.catalog, LevelEnum.AVANZADO)
        self.assertEqual(len(res_adv), 3)

    def test_filter_by_joint_safety(self) -> None:
        # Molestia en hombro debe filtrar press de banca
        res = filter_by_joint_safety(self.catalog, "hombro")
        self.assertNotIn(self.ex1_banca, res)
        self.assertIn(self.ex2_pushup, res)

    def test_biconditional_filter(self) -> None:
        # Solo mancuernas + nivel principiante
        params = LevelParameters(
            nivel=LevelEnum.PRINCIPIANTE,
            rango_series_por_ejercicio=(2, 3),
            rango_repeticiones=(10, 15),
            descanso_segundos=90,
            progresion_carga_semanal_pct=2.5,
            precauciones_generales=(),
            ejercicios_restringidos_ids=frozenset(),
            enfoque_principal="Adaptación",
        )
        res = get_eligible_catalog(self.catalog, frozenset({"mancuernas"}), LevelEnum.PRINCIPIANTE, params)
        # Solo flexiones es viable (peso_corporal)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].id, "flexiones_suelo")


if __name__ == "__main__":
    unittest.main()
