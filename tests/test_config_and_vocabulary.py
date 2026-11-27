"""
Pruebas para src/config/settings.py y el loader de vocabulario de equipo.
"""
from __future__ import annotations

from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.catalog.loader import (
    detectable_ids,
    load_equipment_vocabulary,
    load_exercises,
)
from src.config.settings import GeminiSettings, load_settings
from src.models.catalog import EquipmentVocabularyItem


# ──────────────────────────────────────────────
# Tests de Vocabulario de Equipo
# ──────────────────────────────────────────────
class TestEquipmentVocabularyLoader:
    def test_carga_vocabulario_real_correctamente(self):
        vocab = load_equipment_vocabulary(ROOT / "data" / "equipment_vocabulary.json")
        assert isinstance(vocab, tuple)
        assert len(vocab) == 12
        assert all(isinstance(item, EquipmentVocabularyItem) for item in vocab)

        # Inmutabilidad (dataclass frozen)
        with pytest.raises(FrozenInstanceError):
            vocab[0].nombre_es = "Otro"  # type: ignore[misc]

    def test_peso_corporal_fuera_de_detectables(self):
        vocab = load_equipment_vocabulary(ROOT / "data" / "equipment_vocabulary.json")
        peso_corp = next(item for item in vocab if item.id == "peso_corporal")
        assert peso_corp.detectable is False

        detectables = detectable_ids(vocab)
        assert isinstance(detectables, tuple)
        assert "peso_corporal" not in detectables
        assert len(detectables) == 11

    def test_coincidencia_exacta_vocabulario_y_catalogo_tabla_b(self):
        vocab = load_equipment_vocabulary(ROOT / "data" / "equipment_vocabulary.json")
        ejercicios = load_exercises(ROOT / "data" / "table_b_exercises.json")

        vocab_ids = {item.id for item in vocab}
        catalog_ids = {eq for ex in ejercicios for eq in ex.equipo_requerido}

        assert vocab_ids == catalog_ids

    def test_rechaza_ids_duplicados(self, tmp_path: Path):
        data = [
            {
                "id": "mancuernas",
                "nombre_es": "Mancuernas",
                "descripcion_visual": "Pesas cortas.",
                "detectable": True,
            },
            {
                "id": "mancuernas",
                "nombre_es": "Mancuernas 2",
                "descripcion_visual": "Duplicado.",
                "detectable": True,
            },
        ]
        bad_file = tmp_path / "dup.json"
        bad_file.write_text(json.dumps(data), encoding="utf-8")

        with pytest.raises(ValueError, match="duplicado"):
            load_equipment_vocabulary(bad_file)

    def test_rechaza_json_mal_formado(self, tmp_path: Path):
        bad_file = tmp_path / "malformed.json"
        bad_file.write_text("{esto no es json válido", encoding="utf-8")

        with pytest.raises(json.JSONDecodeError):
            load_equipment_vocabulary(bad_file)

    @pytest.mark.parametrize("campo_faltante", ["id", "nombre_es", "descripcion_visual", "detectable"])
    def test_rechaza_campos_faltantes(self, tmp_path: Path, campo_faltante: str):
        entry = {
            "id": "barra",
            "nombre_es": "Barra",
            "descripcion_visual": "Barra larga.",
            "detectable": True,
        }
        del entry[campo_faltante]

        bad_file = tmp_path / "missing_field.json"
        bad_file.write_text(json.dumps([entry]), encoding="utf-8")

        with pytest.raises(ValueError, match="Faltan campos obligatorios"):
            load_equipment_vocabulary(bad_file)


# ──────────────────────────────────────────────
# Tests de GeminiSettings y load_settings
# ──────────────────────────────────────────────
class TestGeminiSettings:
    def test_load_settings_con_modelo_en_entorno(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("GEMINI_MODEL", "gemini-3.5-flash")
        settings = load_settings(env_path=None)

        assert isinstance(settings, GeminiSettings)
        assert settings.modelo == "gemini-3.5-flash"
        assert settings.temperatura == 0.2
        assert settings.max_image_bytes == 20 * 1024 * 1024
        assert isinstance(settings.mime_types_validos, tuple)
        assert "image/jpeg" in settings.mime_types_validos

        with pytest.raises(FrozenInstanceError):
            settings.modelo = "otro-modelo"  # type: ignore[misc]

    def test_load_settings_falla_si_falta_gemini_model(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.delenv("GEMINI_MODEL", raising=False)
        with pytest.raises(ValueError, match="GEMINI_MODEL"):
            load_settings(env_path=None)

    def test_load_settings_falla_si_gemini_model_vacio(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("GEMINI_MODEL", "   ")
        with pytest.raises(ValueError, match="GEMINI_MODEL"):
            load_settings(env_path=None)
