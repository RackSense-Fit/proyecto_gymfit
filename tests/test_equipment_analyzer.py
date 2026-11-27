"""
test_equipment_analyzer.py – Pruebas unitarias y con mocks del analizador de equipo.

Ejecutar:
    .venv\\Scripts\\python.exe -m pytest tests/test_equipment_analyzer.py -v
"""

from __future__ import annotations

import io
import json
import os
from pathlib import Path
import sys
from unittest.mock import MagicMock, patch

from dotenv import load_dotenv
from PIL import Image
from pydantic import ValidationError
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.catalog.loader import detectable_ids, load_equipment_vocabulary
from src.config.settings import GeminiSettings, load_settings
from src.models.catalog import EquipmentVocabularyItem
from src.vision.equipment_analyzer import (
    AnalisisEquipoResponse,
    EquipoDetectado,
    analyze_gym_image,
    armar_request,
    build_equipment_catalog_prompt,
    build_response_schema,
    equipment_ids_only,
    parsear_y_filtrar_respuesta,
    validar_imagen,
)


# ──────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────
@pytest.fixture
def settings_prueba() -> GeminiSettings:
    return GeminiSettings(modelo="gemini-test-model")


@pytest.fixture
def vocabulario_real() -> tuple[EquipmentVocabularyItem, ...]:
    return load_equipment_vocabulary(ROOT / "data" / "equipment_vocabulary.json")


@pytest.fixture
def prompts_reales() -> tuple[str, str]:
    sys_p = (ROOT / "data" / "prompts" / "equipment_system_prompt.txt").read_text(encoding="utf-8")
    usr_p = (ROOT / "data" / "prompts" / "equipment_user_prompt.txt").read_text(encoding="utf-8")
    return sys_p, usr_p


@pytest.fixture
def imagen_jpeg_valida() -> bytes:
    img = Image.new("RGB", (100, 100), color="red")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


@pytest.fixture
def imagen_png_valida() -> bytes:
    img = Image.new("RGB", (100, 100), color="blue")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture
def respuesta_mock() -> AnalisisEquipoResponse:
    return AnalisisEquipoResponse(
        equipos_detectados=[
            EquipoDetectado(
                equipo_id="mancuernas",
                confianza_0_a_1=0.95,
                justificacion_visual="Mancuernas hexagonales en rack a la derecha.",
            ),
            EquipoDetectado(
                equipo_id="banco_plano",
                confianza_0_a_1=0.88,
                justificacion_visual="Banco plano negro en el centro.",
            ),
        ],
        resumen="Área de peso libre con mancuernas y banco plano.",
        no_identificado=["máquina de press de hombro con discos"],
        personas_visibles=1,
        calidad_foto="buena",
        texto_visible=["GYMFIT", "15 KG"],
    )


# ──────────────────────────────────────────────
# Tests puros de validación de imagen
# ──────────────────────────────────────────────
class TestValidacion:
    def test_imagen_vacia_falla(self, settings_prueba: GeminiSettings):
        with pytest.raises(ValueError, match="vacía"):
            validar_imagen(b"", "image/jpeg", settings_prueba)

    def test_mime_invalido_falla(self, settings_prueba: GeminiSettings, imagen_jpeg_valida: bytes):
        with pytest.raises(ValueError, match="no soportado"):
            validar_imagen(imagen_jpeg_valida, "image/bmp", settings_prueba)

    def test_imagen_corrupta_falla(self, settings_prueba: GeminiSettings):
        with pytest.raises(ValueError, match="corrupta"):
            validar_imagen(b"esto no es una imagen", "image/jpeg", settings_prueba)

    def test_imagen_muy_grande_falla(self, settings_prueba: GeminiSettings):
        datos = b"\x00" * (settings_prueba.max_image_bytes + 1)
        with pytest.raises(ValueError, match="MB"):
            validar_imagen(datos, "image/jpeg", settings_prueba)

    def test_imagen_jpeg_valida_pasa(self, settings_prueba: GeminiSettings, imagen_jpeg_valida: bytes):
        validar_imagen(imagen_jpeg_valida, "image/jpeg", settings_prueba)

    def test_imagen_png_valida_pasa(self, settings_prueba: GeminiSettings, imagen_png_valida: bytes):
        validar_imagen(imagen_png_valida, "image/png", settings_prueba)


# ──────────────────────────────────────────────
# Tests de esquema dinámico y vocabulario
# ──────────────────────────────────────────────
class TestEsquemaDinamico:
    def test_esquema_dinamico_acepta_detectables_y_nuevos_campos(
        self, vocabulario_real: tuple[EquipmentVocabularyItem, ...]
    ):
        schema = build_response_schema(vocabulario_real)
        instancia = schema(
            equipos_detectados=[
                {
                    "equipo_id": "mancuernas",
                    "confianza_0_a_1": 0.92,
                    "justificacion_visual": "Par de mancuernas al frente.",
                }
            ],
            resumen="Zona de peso libre.",
            no_identificado=["máquina de pantorrilla sentado"],
            personas_visibles=2,
            calidad_foto="regular",
            texto_visible=["20 KG"],
        )
        dumped = instancia.model_dump()
        assert dumped["equipos_detectados"][0]["equipo_id"] == "mancuernas"
        assert dumped["no_identificado"] == ["máquina de pantorrilla sentado"]
        assert dumped["personas_visibles"] == 2
        assert dumped["calidad_foto"] == "regular"
        assert dumped["texto_visible"] == ["20 KG"]

    def test_esquema_dinamico_rechaza_ids_fuera_del_vocabulario(
        self, vocabulario_real: tuple[EquipmentVocabularyItem, ...]
    ):
        schema = build_response_schema(vocabulario_real)

        # ID inexistente en el vocabulario
        with pytest.raises(ValidationError):
            schema(
                equipos_detectados=[
                    {
                        "equipo_id": "press_hombro",
                        "confianza_0_a_1": 0.8,
                        "justificacion_visual": "...",
                    }
                ]
            )

        # peso_corporal tiene detectable=False, también debe rechazarse en el esquema
        with pytest.raises(ValidationError):
            schema(
                equipos_detectados=[
                    {
                        "equipo_id": "peso_corporal",
                        "confianza_0_a_1": 0.9,
                        "justificacion_visual": "...",
                    }
                ]
            )

    def test_esquema_dinamico_falla_si_no_hay_detectables(self):
        solo_no_detectable = (
            EquipmentVocabularyItem(
                id="peso_corporal",
                nombre_es="Peso corporal",
                descripcion_visual="Sin equipo.",
                detectable=False,
            ),
        )
        with pytest.raises(ValueError, match="detectable"):
            build_response_schema(solo_no_detectable)

    def test_todos_los_ids_detectables_son_aceptados(
        self, vocabulario_real: tuple[EquipmentVocabularyItem, ...]
    ):
        schema = build_response_schema(vocabulario_real)
        for eid in detectable_ids(vocabulario_real):
            instancia = schema(
                equipos_detectados=[
                    {
                        "equipo_id": eid,
                        "confianza_0_a_1": 0.4,
                        "justificacion_visual": "evidencia",
                    }
                ]
            )
            assert instancia.model_dump()["equipos_detectados"][0]["equipo_id"] == eid


# ──────────────────────────────────────────────
# Tests de armado de request y parseo puro
# ──────────────────────────────────────────────
class TestRequestYParseo:
    def test_armar_request_incluye_descripciones_y_sin_herramientas(
        self,
        imagen_jpeg_valida: bytes,
        settings_prueba: GeminiSettings,
        vocabulario_real: tuple[EquipmentVocabularyItem, ...],
        prompts_reales: tuple[str, str],
    ):
        sys_p, usr_p = prompts_reales
        payload = armar_request(
            imagen_jpeg_valida,
            "image/jpeg",
            settings_prueba,
            vocabulario_real,
            sys_p,
            usr_p,
        )
        assert payload.model == settings_prueba.modelo
        assert payload.config.temperature == settings_prueba.temperatura
        assert payload.config.tools is None
        assert payload.config.thinking_config is None

        sys_instr = str(payload.config.system_instruction)
        assert "polea" in sys_instr
        assert "Una torre de placas sin cables visibles NO es polea." in sys_instr
        assert "peso_corporal" not in build_equipment_catalog_prompt(vocabulario_real)

    def test_parsear_rechaza_id_fuera_de_vocabulario_en_json(
        self, vocabulario_real: tuple[EquipmentVocabularyItem, ...]
    ):
        raw_json = json.dumps(
            {
                "equipos_detectados": [
                    {
                        "equipo_id": "pantorrilla_sentado",
                        "confianza_0_a_1": 0.8,
                        "justificacion_visual": "Máquina de gemelos.",
                    }
                ],
                "resumen": "Área de máquinas.",
                "no_identificado": [],
                "personas_visibles": 0,
                "calidad_foto": "buena",
                "texto_visible": [],
            }
        )
        with pytest.raises(RuntimeError, match="respuesta estructurada válida"):
            parsear_y_filtrar_respuesta(raw_json, None, vocabulario_real)

    def test_parsear_conserva_no_identificado_y_baja_confianza(
        self, vocabulario_real: tuple[EquipmentVocabularyItem, ...]
    ):
        raw_json = json.dumps(
            {
                "equipos_detectados": [
                    {
                        "equipo_id": "mancuernas",
                        "confianza_0_a_1": 0.35,
                        "justificacion_visual": "Posible mancuerna parcial al fondo.",
                    }
                ],
                "resumen": "Gimnasio con máquina de press de hombro.",
                "no_identificado": ["máquina de press de hombro con palancas"],
                "personas_visibles": 1,
                "calidad_foto": "regular",
                "texto_visible": ["LIFE FITNESS"],
            }
        )
        res = parsear_y_filtrar_respuesta(raw_json, None, vocabulario_real)
        assert equipment_ids_only(res) == ["mancuernas"]
        assert res.equipos_detectados[0].confianza_0_a_1 == 0.35
        assert res.no_identificado == ["máquina de press de hombro con palancas"]
        assert res.personas_visibles == 1
        assert res.calidad_foto == "regular"
        assert res.texto_visible == ["LIFE FITNESS"]


# ──────────────────────────────────────────────
# Tests de analyze_gym_image (con mock, sin red)
# ──────────────────────────────────────────────
class TestAnalyzeGymImage:
    def test_falta_api_key_falla(
        self,
        imagen_jpeg_valida: bytes,
        settings_prueba: GeminiSettings,
        vocabulario_real: tuple[EquipmentVocabularyItem, ...],
        prompts_reales: tuple[str, str],
    ):
        sys_p, usr_p = prompts_reales
        with pytest.raises(ValueError, match="GEMINI_API_KEY"):
            analyze_gym_image(
                imagen_jpeg_valida,
                "image/jpeg",
                settings=settings_prueba,
                vocabulario=vocabulario_real,
                system_prompt=sys_p,
                user_prompt=usr_p,
                api_key="",
            )

    def test_llamada_exitosa_con_mock(
        self,
        imagen_jpeg_valida: bytes,
        settings_prueba: GeminiSettings,
        vocabulario_real: tuple[EquipmentVocabularyItem, ...],
        prompts_reales: tuple[str, str],
        respuesta_mock: AnalisisEquipoResponse,
    ):
        sys_p, usr_p = prompts_reales
        mock_response = MagicMock()
        mock_response.parsed = respuesta_mock
        mock_response.text = None

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch("src.vision.equipment_analyzer.genai.Client", return_value=mock_client):
            resultado = analyze_gym_image(
                imagen_jpeg_valida,
                "image/jpeg",
                settings=settings_prueba,
                vocabulario=vocabulario_real,
                system_prompt=sys_p,
                user_prompt=usr_p,
                api_key="fake-key-for-testing",
            )

        assert equipment_ids_only(resultado) == ["mancuernas", "banco_plano"]
        assert resultado.no_identificado == ["máquina de press de hombro con discos"]
        assert resultado.personas_visibles == 1
        assert resultado.calidad_foto == "buena"
        assert resultado.texto_visible == ["GYMFIT", "15 KG"]

    def test_api_error_lanza_runtime_error(
        self,
        imagen_jpeg_valida: bytes,
        settings_prueba: GeminiSettings,
        vocabulario_real: tuple[EquipmentVocabularyItem, ...],
        prompts_reales: tuple[str, str],
    ):
        sys_p, usr_p = prompts_reales
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("503 Service Unavailable")

        with patch("src.vision.equipment_analyzer.genai.Client", return_value=mock_client):
            with pytest.raises(RuntimeError, match="Error al llamar a Gemini"):
                analyze_gym_image(
                    imagen_jpeg_valida,
                    "image/jpeg",
                    settings=settings_prueba,
                    vocabulario=vocabulario_real,
                    system_prompt=sys_p,
                    user_prompt=usr_p,
                    api_key="fake-key-for-testing",
                )

    def test_respuesta_sin_parsed_fallback(
        self,
        imagen_jpeg_valida: bytes,
        settings_prueba: GeminiSettings,
        vocabulario_real: tuple[EquipmentVocabularyItem, ...],
        prompts_reales: tuple[str, str],
        respuesta_mock: AnalisisEquipoResponse,
    ):
        sys_p, usr_p = prompts_reales
        mock_response = MagicMock()
        mock_response.parsed = None
        mock_response.text = respuesta_mock.model_dump_json()

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch("src.vision.equipment_analyzer.genai.Client", return_value=mock_client):
            resultado = analyze_gym_image(
                imagen_jpeg_valida,
                "image/jpeg",
                settings=settings_prueba,
                vocabulario=vocabulario_real,
                system_prompt=sys_p,
                user_prompt=usr_p,
                api_key="fake-key-for-testing",
            )

        assert len(resultado.equipos_detectados) == 2


# ──────────────────────────────────────────────
# Test LIVE (opt-in con -m live; omitido por defecto)
# ──────────────────────────────────────────────
@pytest.mark.live
class TestLive:
    def test_analisis_imagen_real(
        self,
        vocabulario_real: tuple[EquipmentVocabularyItem, ...],
        prompts_reales: tuple[str, str],
    ):
        env_path = ROOT / ".env"
        load_dotenv(env_path)
        settings = load_settings(env_path)
        api_key = os.getenv("GEMINI_API_KEY", "")
        sys_p, usr_p = prompts_reales

        img = Image.new("RGB", (200, 200), color="gray")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")

        resultado = analyze_gym_image(
            buf.getvalue(),
            "image/jpeg",
            settings=settings,
            vocabulario=vocabulario_real,
            system_prompt=sys_p,
            user_prompt=usr_p,
            api_key=api_key,
        )
        assert isinstance(resultado, AnalisisEquipoResponse)
        valid = set(detectable_ids(vocabulario_real))
        for eq in resultado.equipos_detectados:
            assert eq.equipo_id in valid
            assert 0.0 <= eq.confianza_0_a_1 <= 1.0
