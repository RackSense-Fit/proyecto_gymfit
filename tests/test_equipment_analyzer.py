"""
test_equipment_analyzer.py – Pruebas del analizador de equipo de gimnasio.

Ejecutar:
    .venv\\Scripts\\python.exe -m pytest tests/test_equipment_analyzer.py -v

Nota: Los tests marcados con @pytest.mark.live hacen llamadas reales al API de Gemini.
      Para correrlos: pytest -v -m live
      Para omitirlos: pytest -v -m "not live"
"""

from __future__ import annotations

import io
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PIL import Image

# Asegurar que src esté en el path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.vision.equipment_analyzer import (
    EQUIPO_IDS,
    AnalisisEquipoResponse,
    EquipoDetectado,
    _validar_imagen,
    analyze_gym_image,
    equipment_ids_only,
)


# ──────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────
@pytest.fixture
def imagen_jpeg_valida() -> bytes:
    """Genera una imagen JPEG de prueba (1x1 pixel rojo)."""
    img = Image.new("RGB", (100, 100), color="red")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


@pytest.fixture
def imagen_png_valida() -> bytes:
    """Genera una imagen PNG de prueba."""
    img = Image.new("RGB", (100, 100), color="blue")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture
def respuesta_mock() -> AnalisisEquipoResponse:
    """Respuesta simulada del API."""
    return AnalisisEquipoResponse(
        equipos_detectados=[
            EquipoDetectado(
                equipo_id="mancuernas",
                confianza_0_a_1=0.95,
                justificacion_visual="Se ven mancuernas hexagonales en un rack a la derecha."
            ),
            EquipoDetectado(
                equipo_id="banco_plano",
                confianza_0_a_1=0.88,
                justificacion_visual="Banco plano negro visible en el centro de la imagen."
            ),
        ],
        resumen="Área de peso libre con mancuernas y un banco plano."
    )


# ──────────────────────────────────────────────
# Tests de validación de entrada
# ──────────────────────────────────────────────
class TestValidacion:
    """Tests para la función _validar_imagen."""

    def test_imagen_vacia_falla(self):
        with pytest.raises(ValueError, match="vacía"):
            _validar_imagen(b"", "image/jpeg")

    def test_mime_invalido_falla(self):
        img = Image.new("RGB", (10, 10))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        with pytest.raises(ValueError, match="no soportado"):
            _validar_imagen(buf.getvalue(), "image/bmp")

    def test_imagen_corrupta_falla(self):
        with pytest.raises(ValueError, match="corrupta"):
            _validar_imagen(b"esto no es una imagen", "image/jpeg")

    def test_imagen_muy_grande_falla(self):
        # Simular imagen de 21 MB
        datos = b"\x00" * (21 * 1024 * 1024)
        with pytest.raises(ValueError, match="MB"):
            _validar_imagen(datos, "image/jpeg")

    def test_imagen_jpeg_valida_pasa(self, imagen_jpeg_valida):
        # No debe lanzar excepción
        _validar_imagen(imagen_jpeg_valida, "image/jpeg")

    def test_imagen_png_valida_pasa(self, imagen_png_valida):
        _validar_imagen(imagen_png_valida, "image/png")


# ──────────────────────────────────────────────
# Tests de esquemas Pydantic
# ──────────────────────────────────────────────
class TestEsquemas:
    """Tests para los modelos Pydantic."""

    def test_equipo_detectado_valido(self):
        eq = EquipoDetectado(
            equipo_id="barra",
            confianza_0_a_1=0.9,
            justificacion_visual="Barra olímpica visible."
        )
        assert eq.equipo_id == "barra"
        assert eq.confianza_0_a_1 == 0.9

    def test_equipo_id_invalido_falla(self):
        with pytest.raises(Exception):
            EquipoDetectado(
                equipo_id="bicicleta_estatica",  # No existe en los 12 IDs
                confianza_0_a_1=0.9,
                justificacion_visual="..."
            )

    def test_confianza_fuera_de_rango_falla(self):
        with pytest.raises(Exception):
            EquipoDetectado(
                equipo_id="barra",
                confianza_0_a_1=1.5,  # > 1.0
                justificacion_visual="..."
            )

    def test_confianza_negativa_falla(self):
        with pytest.raises(Exception):
            EquipoDetectado(
                equipo_id="barra",
                confianza_0_a_1=-0.1,
                justificacion_visual="..."
            )

    def test_respuesta_vacia_valida(self):
        resp = AnalisisEquipoResponse()
        assert resp.equipos_detectados == []
        assert resp.resumen == ""

    def test_respuesta_con_equipos(self, respuesta_mock):
        assert len(respuesta_mock.equipos_detectados) == 2
        assert respuesta_mock.equipos_detectados[0].equipo_id == "mancuernas"

    def test_todos_los_ids_son_validos(self):
        """Verifica que los 12 IDs son aceptados por el Literal type."""
        for eid in EQUIPO_IDS:
            eq = EquipoDetectado(
                equipo_id=eid,
                confianza_0_a_1=0.5,
                justificacion_visual="test"
            )
            assert eq.equipo_id == eid


# ──────────────────────────────────────────────
# Tests de la función equipment_ids_only
# ──────────────────────────────────────────────
class TestUtilidades:

    def test_equipment_ids_only(self, respuesta_mock):
        ids = equipment_ids_only(respuesta_mock)
        assert ids == ["mancuernas", "banco_plano"]

    def test_equipment_ids_only_vacio(self):
        resp = AnalisisEquipoResponse()
        assert equipment_ids_only(resp) == []


# ──────────────────────────────────────────────
# Tests de analyze_gym_image (con mock del API)
# ──────────────────────────────────────────────
class TestAnalyzeGymImage:
    """Tests de la función principal con mock del API de Gemini."""

    def test_falta_api_key_falla(self, imagen_jpeg_valida):
        # 1. Cuando se pasa api_key="" explícitamente vacía
        with pytest.raises(ValueError, match="GEMINI_API_KEY"):
            analyze_gym_image(
                imagen_jpeg_valida,
                "image/jpeg",
                api_key="",
            )

        # 2. Cuando ni el argumento ni el entorno tienen API key
        with patch("src.vision.equipment_analyzer._API_KEY", ""):
            with patch.dict(os.environ, {"GEMINI_API_KEY": ""}, clear=False):
                with pytest.raises(ValueError, match="GEMINI_API_KEY"):
                    analyze_gym_image(
                        imagen_jpeg_valida,
                        "image/jpeg",
                        api_key=None,
                    )

    def test_llamada_exitosa_con_mock(self, imagen_jpeg_valida, respuesta_mock):
        """Simula una respuesta exitosa del API."""
        mock_response = MagicMock()
        mock_response.parsed = respuesta_mock

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch("src.vision.equipment_analyzer.genai.Client", return_value=mock_client):
            resultado = analyze_gym_image(
                imagen_jpeg_valida,
                "image/jpeg",
                api_key="fake-key-for-testing",
            )

        assert len(resultado.equipos_detectados) == 2
        assert resultado.equipos_detectados[0].equipo_id == "mancuernas"
        assert resultado.resumen == "Área de peso libre con mancuernas y un banco plano."

    def test_api_error_lanza_runtime_error(self, imagen_jpeg_valida):
        """Simula un error del API."""
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("503 Service Unavailable")

        with patch("src.vision.equipment_analyzer.genai.Client", return_value=mock_client):
            with pytest.raises(RuntimeError, match="Error al llamar a Gemini"):
                analyze_gym_image(
                    imagen_jpeg_valida,
                    "image/jpeg",
                    api_key="fake-key-for-testing",
                )

    def test_respuesta_sin_parsed_fallback(self, imagen_jpeg_valida, respuesta_mock):
        """Simula cuando .parsed es None pero .text tiene JSON válido."""
        mock_response = MagicMock()
        mock_response.parsed = None
        mock_response.text = respuesta_mock.model_dump_json()

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch("src.vision.equipment_analyzer.genai.Client", return_value=mock_client):
            resultado = analyze_gym_image(
                imagen_jpeg_valida,
                "image/jpeg",
                api_key="fake-key-for-testing",
            )

        assert len(resultado.equipos_detectados) == 2


# ──────────────────────────────────────────────
# Test LIVE (requiere API key real, marcado para opt-in)
# ──────────────────────────────────────────────
@pytest.mark.live
class TestLive:
    """
    Tests que hacen llamadas reales a Gemini.
    Ejecutar con: pytest -v -m live
    """

    def test_analisis_imagen_real(self):
        """Envía una imagen de prueba real al API."""
        # Crear una imagen de prueba simple (no es foto real de gym,
        # pero verifica la conectividad)
        img = Image.new("RGB", (200, 200), color="gray")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")

        resultado = analyze_gym_image(buf.getvalue(), "image/jpeg")

        # Validar que la respuesta es del tipo correcto
        assert isinstance(resultado, AnalisisEquipoResponse)
        assert isinstance(resultado.resumen, str)
        # Con una imagen gris, probablemente no detecte equipo
        for eq in resultado.equipos_detectados:
            assert eq.equipo_id in EQUIPO_IDS
            assert 0.0 <= eq.confianza_0_a_1 <= 1.0
