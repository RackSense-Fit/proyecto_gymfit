"""
Suite de pruebas de integración para la API de FastAPI con TestClient.
"""
import unittest
from fastapi.testclient import TestClient
from src.api.app import app
from src.api.state_manager import manager


class TestFastAPIIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def setUp(self) -> None:
        # Reiniciar estado antes de cada prueba
        manager.reset_state()

    def test_root_and_health(self) -> None:
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("GymFit Agent", r.text)

        r_dash = self.client.get("/dashboard")
        self.assertEqual(r_dash.status_code, 200)
        self.assertIn("GymFit Agent — Dashboard Interactivo", r_dash.text)

        r_health = self.client.get("/health")
        self.assertEqual(r_health.status_code, 200)
        self.assertEqual(r_health.json()["status"], "healthy")

    def test_seed_demo_data(self) -> None:
        res_seed = self.client.post("/api/state/seed")
        self.assertEqual(res_seed.status_code, 200)
        state_data = res_seed.json()["state"]
        self.assertIsNotNone(state_data["perfil"])
        self.assertIsNotNone(state_data["rutina_actual"])
        self.assertEqual(len(state_data["rutina_actual"]["dias"]), 3)

    def test_full_api_workflow(self) -> None:
        # 1. Crear Perfil
        res_p = self.client.post(
            "/api/profile",
            json={
                "nombre": "Elena Torres",
                "sexo": "femenino",
                "peso_kg": 62.0,
                "altura_cm": 168.0,
                "objetivo": "ganar_musculo",
                "nivel": "principiante",
                "dias_disponibles": 3,
            },
        )
        self.assertEqual(res_p.status_code, 200)
        self.assertEqual(res_p.json()["perfil"]["nombre"], "Elena Torres")

        # 2. Registrar Equipo
        res_eq = self.client.post(
            "/api/equipment",
            json={"equipo": ["mancuernas", "banco_plano", "polea", "peso_corporal"]},
        )
        self.assertEqual(res_eq.status_code, 200)
        self.assertIn("mancuernas", res_eq.json()["equipo_disponible"])

        # 3. Generar Rutina Semanal
        res_r = self.client.post("/api/routine/generate")
        self.assertEqual(res_r.status_code, 200)
        rutina_data = res_r.json()["rutina"]
        self.assertEqual(len(rutina_data["dias"]), 3)
        self.assertIn("Elena Torres", rutina_data["explicacion_agente"])

        # 4. Iniciar y Registrar Sesión
        res_s_ini = self.client.post(
            "/api/session/start",
            json={"dia_numero": 1, "fecha": "2026-09-20", "hora_inicio": "10:00:00"},
        )
        self.assertEqual(res_s_ini.status_code, 200)
        id_sesion = res_s_ini.json()["id_sesion"]

        # Registrar Serie con descanso
        res_set = self.client.post(
            "/api/session/set",
            json={
                "id_sesion": id_sesion,
                "ejercicio_id": "press_plano_mancuernas",
                "numero_serie": 1,
                "peso_kg": 10.0,
                "repeticiones": 12,
                "descanso_segundos_real": 90,
            },
        )
        self.assertEqual(res_set.status_code, 200)

        # Finalizar Sesión
        res_s_fin = self.client.post(
            "/api/session/finish",
            json={
                "id_sesion": id_sesion,
                "hora_fin": "10:45:00",
                "duracion_total_segundos": 2700,
            },
        )
        self.assertEqual(res_s_fin.status_code, 200)
        self.assertEqual(res_s_fin.json()["total_sesiones_completadas"], 1)

        # 5. Reportar Molestia en Hombro
        res_mol = self.client.post(
            "/api/adjustments/discomfort",
            json={
                "zona_articular": "hombro",
                "intensidad_1_a_10": 5,
                "ejercicio_origen_id": "press_plano_mancuernas",
            },
        )
        self.assertEqual(res_mol.status_code, 200)
        self.assertIn("hombro", res_mol.json()["ajuste"]["motivo"])

        # 6. Reportar Falta de Tiempo
        res_time = self.client.post(
            "/api/adjustments/time-crunch",
            json={
                "tipo": "poco_tiempo",
                "dia_afectado": 2,
                "minutos_disponibles_hoy": 20,
                "detalle": "Prisa",
            },
        )
        self.assertEqual(res_time.status_code, 200)

        # 7. Consultar Estado y Traza de Eventos
        res_state = self.client.get("/api/state")
        self.assertEqual(res_state.status_code, 200)
        self.assertEqual(len(res_state.json()["state"]["historial_ajustes"]), 2)

        res_events = self.client.get("/api/state/events")
        self.assertEqual(res_events.status_code, 200)
        self.assertGreaterEqual(res_events.json()["total_eventos"], 6)


if __name__ == "__main__":
    unittest.main()
