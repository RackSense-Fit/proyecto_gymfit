"""
test_vision_demo.py – Script de demostración CLI para probar el analizador de equipo.

Uso:
    .venv\\Scripts\\python.exe scripts\\test_vision_demo.py
    .venv\\Scripts\\python.exe scripts\\test_vision_demo.py ruta/a/foto_gym.jpg

Sin argumentos, usa una imagen de ejercicio del dataset incluido (si existe).
"""

from __future__ import annotations

import os
from pathlib import Path
import sys

from dotenv import load_dotenv

# Agregar raíz del proyecto al path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.catalog.loader import load_equipment_vocabulary
from src.config.settings import GeminiSettings, load_settings
from src.models.catalog import EquipmentVocabularyItem
from src.vision.equipment_analyzer import (
    AnalisisEquipoResponse,
    analyze_gym_image,
    equipment_ids_only,
)


EXT_TO_MIME: dict[str, str] = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".heic": "image/heic",
    ".heif": "image/heif",
}


def analyze_gym_image_from_file(
    file_path: str | Path,
    *,
    settings: GeminiSettings,
    vocabulario: tuple[EquipmentVocabularyItem, ...],
    system_prompt: str,
    user_prompt: str,
    api_key: str,
) -> AnalisisEquipoResponse:
    """Utilería CLI: lee una imagen desde disco y la envía al analizador."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró la imagen: {path}")

    mime = EXT_TO_MIME.get(path.suffix.lower())
    if mime is None:
        raise ValueError(f"Extensión '{path.suffix}' no soportada.")

    image_bytes = path.read_bytes()
    return analyze_gym_image(
        image_bytes,
        mime,
        settings=settings,
        vocabulario=vocabulario,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        api_key=api_key,
    )


def buscar_imagen_demo() -> Path | None:
    """Busca una imagen de ejercicio en el dataset externo (si existe)."""
    exercises_dir = ROOT / "data" / "external" / "free-exercise-db" / "exercises"
    if exercises_dir.exists():
        for ext in ("*.jpg", "*.png", "*.jpeg"):
            imagenes = list(exercises_dir.glob(f"**/{ext}"))
            if imagenes:
                return imagenes[0]
    return None


def main() -> None:
    print("=" * 60)
    print("  🏋️ GymFit – Demo del Analizador de Equipo")
    print("=" * 60)
    print()

    if len(sys.argv) >= 2:
        ruta = Path(sys.argv[1])
    else:
        ruta = buscar_imagen_demo()
        if ruta is None:
            print("❌ No se encontró una imagen de demo.")
            print("   Usa: python scripts/test_vision_demo.py <ruta_imagen>")
            sys.exit(1)

    env_path = ROOT / ".env"
    load_dotenv(env_path)
    api_key = os.getenv("GEMINI_API_KEY", "")

    settings = load_settings(env_path)
    vocabulario = load_equipment_vocabulary(ROOT / "data" / "equipment_vocabulary.json")
    system_prompt = (ROOT / "data" / "prompts" / "equipment_system_prompt.txt").read_text(encoding="utf-8")
    user_prompt = (ROOT / "data" / "prompts" / "equipment_user_prompt.txt").read_text(encoding="utf-8")

    print(f"📷 Imagen: {ruta}")
    print(f"   Tamaño: {ruta.stat().st_size / 1024:.1f} KB")
    print(f"🤖 Modelo: {settings.modelo}")
    print()
    print("🔄 Enviando a Gemini...")
    print()

    try:
        resultado = analyze_gym_image_from_file(
            ruta,
            settings=settings,
            vocabulario=vocabulario,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            api_key=api_key,
        )
    except ValueError as e:
        print(f"❌ Error de validación: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"❌ Error del API: {e}")
        sys.exit(1)

    print(f"📝 Resumen: {resultado.resumen}")
    print(f"📸 Calidad: {resultado.calidad_foto} | Personas visibles: {resultado.personas_visibles}")
    if resultado.texto_visible:
        print(f"🔤 Texto visible: {resultado.texto_visible}")
    print()
    print(f"🏋️ Equipos detectados: {len(resultado.equipos_detectados)}")
    print("-" * 60)

    for eq in resultado.equipos_detectados:
        barra = "█" * int(eq.confianza_0_a_1 * 20)
        espacios = "░" * (20 - int(eq.confianza_0_a_1 * 20))
        print(f"  {eq.equipo_id:<25} [{barra}{espacios}] {eq.confianza_0_a_1:.0%}")
        print(f"  {'':25} └─ {eq.justificacion_visual}")
        print()

    if resultado.no_identificado:
        print("❓ No identificado:")
        for desc in resultado.no_identificado:
            print(f"  - {desc}")
        print()

    print("-" * 60)
    ids = equipment_ids_only(resultado)
    print(f"✅ IDs para el generador de rutinas: {ids}")
    print()
    print("Estos IDs se pueden pasar directamente a:")
    print('  generate_routine(equipo_disponible=["' + '", "'.join(ids) + '"])')


if __name__ == "__main__":
    main()
