"""
test_vision_demo.py – Script de demostración para probar el analizador de equipo.

Uso:
    .venv\\Scripts\\python.exe scripts\\test_vision_demo.py
    .venv\\Scripts\\python.exe scripts\\test_vision_demo.py ruta/a/foto_gym.jpg

Sin argumentos, usa una imagen de ejercicio del dataset incluido (si existe).
"""

import sys
from pathlib import Path

# Agregar raíz del proyecto al path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.vision.equipment_analyzer import (
    analyze_gym_image_from_file,
    equipment_ids_only,
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


def main():
    print("=" * 60)
    print("  🏋️ GymFit – Demo del Analizador de Equipo")
    print("=" * 60)
    print()

    # Determinar la imagen a analizar
    if len(sys.argv) >= 2:
        ruta = Path(sys.argv[1])
    else:
        ruta = buscar_imagen_demo()
        if ruta is None:
            print("❌ No se encontró una imagen de demo.")
            print("   Usa: python scripts/test_vision_demo.py <ruta_imagen>")
            sys.exit(1)

    print(f"📷 Imagen: {ruta}")
    print(f"   Tamaño: {ruta.stat().st_size / 1024:.1f} KB")
    print()
    print("🔄 Enviando a Gemini...")
    print()

    try:
        resultado = analyze_gym_image_from_file(ruta)
    except ValueError as e:
        print(f"❌ Error de validación: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"❌ Error del API: {e}")
        sys.exit(1)

    # Mostrar resultados
    print(f"📝 Resumen: {resultado.resumen}")
    print()
    print(f"🏋️ Equipos detectados: {len(resultado.equipos_detectados)}")
    print("-" * 60)

    for eq in resultado.equipos_detectados:
        barra = "█" * int(eq.confianza_0_a_1 * 20)
        espacios = "░" * (20 - int(eq.confianza_0_a_1 * 20))
        print(f"  {eq.equipo_id:<25} [{barra}{espacios}] {eq.confianza_0_a_1:.0%}")
        print(f"  {'':25} └─ {eq.justificacion_visual}")
        print()

    print("-" * 60)
    ids = equipment_ids_only(resultado)
    print(f"✅ IDs para el generador de rutinas: {ids}")
    print()
    print("Estos IDs se pueden pasar directamente a:")
    print('  generate_routine(equipo_disponible=["' + '", "'.join(ids) + '"])')


if __name__ == "__main__":
    main()
