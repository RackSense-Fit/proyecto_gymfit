"""
Suite de pruebas de integración para la API de FastAPI con TestClient.
"""
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.api.app import app
from src.api.state_manager import manager
from src.vision.equipment_analyzer import AnalisisEquipoResponse, EquipoDetectado


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

    def test_static_vendor_files_respond_200(self) -> None:
        """Verifica que cada archivo en /static/vendor/ responda con código HTTP 200."""
        vendor_files = [
            "tf.min.js",
            "coco-ssd.min.js",
            "model.json",
            "group1-shard1of5",
            "group1-shard2of5",
            "group1-shard3of5",
            "group1-shard4of5",
            "group1-shard5of5",
            "README.md",
        ]
        for filename in vendor_files:
            resp = self.client.get(f"/static/vendor/{filename}")
            self.assertEqual(
                resp.status_code,
                200,
                f"El archivo /static/vendor/{filename} no respondió 200 (obtenido: {resp.status_code})",
            )
            self.assertGreater(
                len(resp.content),
                0,
                f"El archivo /static/vendor/{filename} se encuentra vacío",
            )

    def test_app_starts_with_empty_static_directory(self) -> None:
        """Verifica que la app arranque igual sin errores si la carpeta static está vacía o no existe."""
        import tempfile
        from pathlib import Path
        from src.api.app import create_app

        with tempfile.TemporaryDirectory() as empty_dir:
            empty_path = Path(empty_dir) / "empty_static"
            # No creamos previamente empty_path para probar que create_app la crea y arranca sin error
            test_app = create_app(static_dir=empty_path)
            test_client = TestClient(test_app)

            # Verificar que las rutas clave siguen respondiendo 200
            res_health = test_client.get("/health")
            self.assertEqual(res_health.status_code, 200)
            self.assertEqual(res_health.json()["status"], "healthy")

            res_root = test_client.get("/")
            self.assertEqual(res_root.status_code, 200)

            # La carpeta estática vacía responde 404 al buscar un recurso inexistente sin crashear
            res_static = test_client.get("/static/vendor/inexistente.js")
            self.assertEqual(res_static.status_code, 404)

    def test_vendor_content_types(self) -> None:
        """Verifica que los tipos MIME servidos para JS y JSON sean estrictamente correctos."""
        resp_tf = self.client.get("/static/vendor/tf.min.js")
        self.assertEqual(resp_tf.status_code, 200)
        ct_tf = resp_tf.headers.get("content-type", "")
        self.assertTrue(
            ct_tf.startswith(("text/javascript", "application/javascript")),
            f"Content-Type inesperado para tf.min.js: {ct_tf}",
        )

        resp_coco = self.client.get("/static/vendor/coco-ssd.min.js")
        self.assertEqual(resp_coco.status_code, 200)
        ct_coco = resp_coco.headers.get("content-type", "")
        self.assertTrue(
            ct_coco.startswith(("text/javascript", "application/javascript")),
            f"Content-Type inesperado para coco-ssd.min.js: {ct_coco}",
        )

        resp_model = self.client.get("/static/vendor/model.json")
        self.assertEqual(resp_model.status_code, 200)
        ct_model = resp_model.headers.get("content-type", "")
        self.assertTrue(
            ct_model.startswith("application/json"),
            f"Content-Type inesperado para model.json: {ct_model}",
        )

    def test_security_path_traversal_and_sensitive_files(self) -> None:
        """Verifica que no haya vulnerabilidades de Directory Traversal ni acceso a archivos sensibles."""
        # Path traversal no debe responder 200 bajo ninguna circunstancia
        traversal_paths = [
            "/static/../.env",
            "/static/%2e%2e/.env",
            "/static/%2E%2E/.env",
            "/exercise-images/../../.env",
            "/exercise-images/%2e%2e/%2e%2e/.env",
        ]
        for path in traversal_paths:
            resp = self.client.get(path)
            self.assertNotEqual(
                resp.status_code,
                200,
                f"La ruta vulnerable {path} respondió con código 200 OK",
            )

        # Archivos sensibles del sistema/proyecto no deben ser accesibles vía URL
        sensitive_paths = [
            "/.env",
            "/static/.env",
            "/exercise-images/.env",
            "/.git",
            "/.git/config",
            "/static/.git",
            "/exercise-images/.git",
            "/data/table_a_levels.json",
            "/data/table_b_exercises.json",
            "/data/table_b_splits.json",
            "/static/data/table_a_levels.json",
            "/exercise-images/data/table_a_levels.json",
        ]
        for path in sensitive_paths:
            resp = self.client.get(path)
            self.assertNotEqual(
                resp.status_code,
                200,
                f"El recurso sensible {path} fue accesible con código 200 OK",
            )

        # /static/vendor/ no debe listar archivos del directorio
        resp_dir = self.client.get("/static/vendor/")
        self.assertNotEqual(
            resp_dir.status_code,
            200,
            "El directorio /static/vendor/ devolvió 200 (potencial listado de directorio)",
        )

    def test_exercise_images_mounting_and_fallback(self) -> None:
        """Verifica el montaje condicional de /exercise-images/ y arranque limpio si no existe."""
        from pathlib import Path
        from src.api.app import create_app

        # 1. Si existe en el entorno actual, la app por defecto responde a los recursos de ejercicios
        resp_ex = self.client.get("/exercise-images/Close-Grip_Front_Lat_Pulldown.json")
        self.assertEqual(resp_ex.status_code, 200)

        # 2. Si el directorio NO existe, create_app arranca normalmente sin la ruta
        test_app = create_app(exercises_dir=Path("/directorio/totalmente/inexistente/exercises"))
        test_client = TestClient(test_app)

        res_health = test_client.get("/health")
        self.assertEqual(res_health.status_code, 200)
        self.assertEqual(res_health.json()["status"], "healthy")

        res_missing_route = test_client.get("/exercise-images/Close-Grip_Front_Lat_Pulldown.json")
        self.assertEqual(res_missing_route.status_code, 404)

    def test_verify_model_html_served(self) -> None:
        """Verifica que la página desechable /static/verify-model.html se sirva con código 200."""
        resp = self.client.get("/static/verify-model.html")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("text/html", resp.headers.get("content-type", ""))
        self.assertIn("Verificación de Carga Local del Modelo COCO-SSD", resp.text)
        self.assertIn("/static/vendor/model.json", resp.text)

    def test_root_and_dashboard_return_html_fileresponse(self) -> None:
        """Verifica que / y /dashboard respondan con código 200 y sirvan index.html vía FileResponse."""
        for endpoint in ["/", "/dashboard"]:
            resp = self.client.get(endpoint)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("text/html", resp.headers.get("content-type", ""))
            self.assertIn("GymFit Agent — Dashboard Interactivo", resp.text)
            self.assertIn('<link rel="stylesheet" href="/static/css/styles.css">', resp.text)
            self.assertIn('<script src="/static/js/equipo.js"></script>', resp.text)
            self.assertIn('<script src="/static/js/eventos.js"></script>', resp.text)

    def test_extracted_frontend_assets_respond_200(self) -> None:
        """Verifica que los assets extraídos del frontend (CSS y JS modulares) respondan 200."""
        assets = [
            ("/static/css/styles.css", "text/css"),
            ("/static/js/equipo.js", ("text/javascript", "application/javascript")),
            ("/static/js/cronometro.js", ("text/javascript", "application/javascript")),
            ("/static/js/perfil.js", ("text/javascript", "application/javascript")),
            ("/static/js/rutina.js", ("text/javascript", "application/javascript")),
            ("/static/js/eventos.js", ("text/javascript", "application/javascript")),
        ]
        for path, expected_ct in assets:
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, 200, f"Error cargando asset {path}")
            ct = resp.headers.get("content-type", "")
            if isinstance(expected_ct, tuple):
                self.assertTrue(ct.startswith(expected_ct), f"Tipo incorrecto para {path}: {ct}")
            else:
                self.assertTrue(ct.startswith(expected_ct), f"Tipo incorrecto para {path}: {ct}")

    def test_analyze_equipment_image_endpoint_success(self) -> None:
        """Verifica que /api/equipment/analyze-image responda 200 y devuelva la estructura adecuada."""
        fake_response = AnalisisEquipoResponse(
            equipos_detectados=[
                EquipoDetectado(
                    equipo_id="mancuernas",
                    confianza_0_a_1=0.95,
                    justificacion_visual="Rack de mancuernas visible.",
                ),
                EquipoDetectado(
                    equipo_id="banco_plano",
                    confianza_0_a_1=0.90,
                    justificacion_visual="Banco plano en el centro.",
                ),
            ],
            resumen="Zona de peso libre con mancuernas y banco plano.",
        )

        with patch("src.api.routers.equipment.analyze_gym_image", return_value=fake_response):
            # Simular carga de archivo multipart
            files = {"file": ("test.jpg", b"\xff\xd8\xff\xe0fakejpegcontent", "image/jpeg")}
            resp = self.client.post("/api/equipment/analyze-image", files=files)

        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("equipment_ids", data)
        self.assertEqual(data["equipment_ids"], ["mancuernas", "banco_plano"])
        self.assertEqual(len(data["equipos_detectados"]), 2)
        self.assertIn("Zona de peso libre", data["resumen"])

    def test_analyze_equipment_image_endpoint_invalid_image(self) -> None:
        """Verifica que una imagen vacía o inválida devuelva 400 Bad Request."""
        files = {"file": ("vacio.jpg", b"", "image/jpeg")}
        resp = self.client.post("/api/equipment/analyze-image", files=files)
        self.assertEqual(resp.status_code, 400)

    def test_analyze_equipment_image_endpoint_gemini_error(self) -> None:
        """Verifica que un fallo en el API de Gemini devuelva 502 Bad Gateway."""
        with patch("src.api.routers.equipment.analyze_gym_image", side_effect=RuntimeError("API quota exceeded")):
            files = {"file": ("test.jpg", b"fake", "image/jpeg")}
            resp = self.client.post("/api/equipment/analyze-image", files=files)
        self.assertEqual(resp.status_code, 502)


if __name__ == "__main__":
    unittest.main()
