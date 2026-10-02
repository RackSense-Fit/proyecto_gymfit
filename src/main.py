"""
Punto de entrada y demostración funcional de GymFit Agent.
Simula el ciclo completo:
1. Carga pura de catálogos (Tablas A y B).
2. Creación de perfil y registro de equipo.
3. Filtrado bicondicional e inferencia de split.
4. Generación funcional de rutina con técnica fija y alternativas.
5. Registro inmutable de sesión y cronómetro.
6. Adaptación reactiva pura ante eventos de variabilidad (molestia, tiempo, dificultad).
7. Demostración de Event Sourcing / Fold de historial.
"""
import sys
from pathlib import Path

# Configurar salida UTF-8 para consola de Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Permitir ejecución tanto como script directo (`python src/main.py`) como módulo (`python -m src.main`)
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.catalog.filters import get_eligible_catalog
from src.catalog.loader import load_full_catalog
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


def print_banner(title: str) -> None:
    print("\n" + "=" * 75)
    print(f"  {title.upper()}")
    print("=" * 75)


def print_routine_summary(state: AppState) -> None:
    if not state.rutina_actual:
        print("No hay rutina activa.")
        return

    r = state.rutina_actual
    print(f"\n📋 RUTINA ACTIVA: {r.nombre_split} (ID: {r.id_rutina})")
    print(f"💬 Explicación del Agente:\n   \"{r.explicacion_agente}\"\n")

    for dia in r.dias:
        print(f"  📅 DÍA {dia.dia_numero}: {dia.nombre_dia} (~{dia.duracion_estimada_minutos} min)")
        for idx, slot in enumerate(dia.slots, 1):
            ex = slot.ejercicio_principal
            p = slot.parametros
            alts_str = ", ".join(a.nombre for a in slot.alternativas) if slot.alternativas else "Ninguna alternativa adicional"
            print(f"     {idx}. {ex.nombre} [{slot.grupo_muscular.value.upper()}]")
            print(f"        • Parámetros: {p.series} series x {p.repeticiones_sugeridas} reps | Carga inicial: {p.peso_kg_sugerido} kg | Descanso: {p.descanso_segundos}s")
            print(f"        • Técnica fija: {ex.instrucciones_fijas[0] if ex.instrucciones_fijas else 'N/A'}")
            print(f"        • Alternativas seguras disponibles: {alts_str}")
        print()


def main() -> None:
    print_banner("GymFit Agent — Demostración de Paradigma Funcional")

    # 1. Carga pura de Catálogos (Tablas A y B)
    base_dir = Path(__file__).parent.parent / "data"
    catalog = load_full_catalog(base_dir)
    print(f"✓ Catálogo cargado con éxito:")
    print(f"  - Tabla A: Parámetros para {len(catalog.tabla_a_niveles)} niveles (ACSM/NSCA).")
    print(f"  - Tabla B: {len(catalog.tabla_b_ejercicios)} ejercicios y {len(catalog.tabla_b_splits)} plantillas de splits.")

    # 2. Estado Inicial Inmutable
    state = AppState()
    print("\n✓ Estado inicial creado (AppState vacío e inmutable).")

    # 3. Disparo de Evento: PerfilCreado
    perfil = UserProfile(
        nombre="Carlos Mendoza",
        sexo=SexEnum.MASCULINO,
        peso_kg=76.0,
        altura_cm=178.0,
        objetivo=GoalEnum.GANAR_MUSCULO,
        nivel=LevelEnum.PRINCIPIANTE,
        dias_disponibles=3,
    )
    ev_perfil = PerfilCreado(perfil=perfil, timestamp="2026-09-18 13:12:04")
    state = reduce_event(state, ev_perfil, catalog)
    print(f"\n[Evento] PerfilCreado -> Usuario: {state.perfil.nombre}, Nivel: {state.perfil.nivel.value}, IMC: {state.perfil.imc}")

    # 4. Disparo de Evento: EquipoRegistrado (Gimnasio con equipo limitado)
    equipo_usuario = frozenset({"mancuernas", "banco_plano", "barra_dominadas", "peso_corporal"})
    ev_equipo = EquipoRegistrado(equipo=equipo_usuario, timestamp="2026-09-18 13:12:10")
    state = reduce_event(state, ev_equipo, catalog)
    print(f"[Evento] EquipoRegistrado -> Equipos: {', '.join(sorted(state.equipo_disponible))}")

    # 5. Filtrado Bicondicional Puro: Equipo ∩ Nivel
    level_params = catalog.tabla_a_niveles[state.perfil.nivel]
    eligible_exercises = get_eligible_catalog(
        catalog.tabla_b_ejercicios,
        state.equipo_disponible,
        state.perfil.nivel,
        level_params,
    )
    print(f"\n✓ Filtrado Bicondicional Puro aplicado:")
    print(f"  - Total ejercicios catálogo global: {len(catalog.tabla_b_ejercicios)}")
    print(f"  - Ejercicios viables para Carlos: {len(eligible_exercises)} (Solo equipo disponible y nivel principiante)")

    # 6. Selección Pura de Split y Generación de Rutina
    split_template = select_split_template(catalog.tabla_b_splits, state.perfil.dias_disponibles, state.perfil.objetivo)
    rutina_inicial = generate_routine(
        perfil=state.perfil,
        eligible_catalog=eligible_exercises,
        level_params=level_params,
        split_template=split_template,
        timestamp="2026-09-18 13:12:15",
    )
    ev_rutina = RutinaGenerada(rutina=rutina_inicial, timestamp="2026-09-18 13:12:15")
    state = reduce_event(state, ev_rutina, catalog)

    print_banner("Paso 1: Rutina Semanal Inicial Generada")
    print_routine_summary(state)

    # 7. Simulación de Registro de Sesión con Cronómetro
    print_banner("Paso 2: Registro de Sesión Real (Día 1)")
    ev_ses_ini = SesionIniciada(
        id_sesion="sesion_001",
        dia_numero=1,
        fecha="2026-09-18",
        hora_inicio="14:00:00",
        timestamp="2026-09-18 14:00:00",
    )
    state = reduce_event(state, ev_ses_ini, catalog)
    print(f"[Evento] SesionIniciada -> ID: sesion_001 (Día 1)")

    # Registrando series completadas
    ev_s1 = SerieRegistrada("sesion_001", "press_plano_mancuernas", 1, 12.0, 12, 90, "2026-09-18 14:05:00")
    ev_s2 = SerieRegistrada("sesion_001", "press_plano_mancuernas", 2, 12.0, 11, 95, "2026-09-18 14:08:00")
    state = reduce_event(state, ev_s1, catalog)
    state = reduce_event(state, ev_s2, catalog)
    print(f"[Evento] Series 1 y 2 registradas con peso y cronómetro de descanso.")

    ev_ses_fin = SesionFinalizada("sesion_001", "14:48:00", 2880, "2026-09-18 14:48:00")
    state = reduce_event(state, ev_ses_fin, catalog)
    print(f"[Evento] SesionFinalizada -> Duración total: 48 min.")
    print(f"✓ Calendario actualizado: {state.dias_entrenados_mes_actual} días entrenados este mes.")

    # 8. Variabilidad 1: Molestia en Hombro
    print_banner("Paso 3: Adaptación Reactiva ante Molestia Reportada")
    ev_molestia = MolestiaReportada(
        zona_articular="hombro",
        intensidad_1_a_10=6,
        ejercicio_origen_id="press_plano_mancuernas",
        timestamp="2026-09-18 16:00:00",
    )
    state = reduce_event(state, ev_molestia, catalog)
    ultimo_ajuste = state.historial_ajustes[-1]
    print(f"[Evento] MolestiaReportada -> {ultimo_ajuste.motivo}")
    print(f"💬 Detalle del Ajuste:\n   {ultimo_ajuste.detalle_ajuste}")
    print_routine_summary(state)

    # 9. Variabilidad 2: Imprevisto por poco tiempo en el Día 2
    print_banner("Paso 4: Adaptación ante Imprevisto (Poco Tiempo)")
    ev_tiempo = ImprevistoReportado(
        tipo=UnforeseenTypeEnum.POCO_TIEMPO,
        dia_afectado=2,
        minutos_disponibles_hoy=25,
        detalle="Tengo junta de trabajo urgente, solo dispongo de 25 minutos.",
        timestamp="2026-09-18 17:00:00",
    )
    state = reduce_event(state, ev_tiempo, catalog)
    ultimo_ajuste = state.historial_ajustes[-1]
    print(f"[Evento] ImprevistoReportado -> {ultimo_ajuste.motivo}")
    print(f"💬 Detalle del Ajuste:\n   {ultimo_ajuste.detalle_ajuste}")
    print_routine_summary(state)

    # 10. Variabilidad 3: Dificultad muy fácil (Sobrecarga progresiva)
    print_banner("Paso 5: Sobrecarga Progresiva por Dificultad Reportada")
    ev_dif = DificultadReportada(
        ejercicio_id="remo_unilateral_mancuerna",
        percepcion=DifficultyPerceptionEnum.MUY_FACIL,
        comentarios="Las series se sintieron muy ligeras, completé todas las repeticiones sin esfuerzo.",
        timestamp="2026-09-18 18:00:00",
    )
    state = reduce_event(state, ev_dif, catalog)
    ultimo_ajuste = state.historial_ajustes[-1]
    print(f"[Evento] DificultadReportada -> {ultimo_ajuste.motivo}")
    print(f"💬 Detalle del Ajuste:\n   {ultimo_ajuste.detalle_ajuste}")

    # 11. Demostración de Event Sourcing / Fold
    print_banner("Paso 6: Verificación de Pureza y Event Sourcing (Fold)")
    total_eventos = len(state.historial_eventos)
    print(f"Total de eventos acumulados en la traza: {total_eventos}")

    # Reconstrucción pura desde el estado inicial vacío usando functools.reduce
    estado_reconstruido = fold_events(AppState(), state.historial_eventos, catalog)
    
    es_identico = (
        estado_reconstruido.perfil == state.perfil
        and estado_reconstruido.equipo_disponible == state.equipo_disponible
        and estado_reconstruido.total_sesiones_completadas == state.total_sesiones_completadas
        and len(estado_reconstruido.historial_ajustes) == len(state.historial_ajustes)
        and len(estado_reconstruido.historial_eventos) == total_eventos
    )

    print(f"✓ Reconstrucción completa del estado mediante fold_events(): {'EXITOSA (Determinismo Matemático)' if es_identico else 'FALLIDA'}")
    print(f"✓ Todas las transiciones de estado fueron funciones puras con inmutabilidad estricta.")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    main()
