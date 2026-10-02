"""
Enumeraciones fuertemente tipadas e inmutables para el dominio de GymFit Agent.
"""
from enum import Enum


class GoalEnum(str, Enum):
    """Objetivo físico principal del usuario."""
    BAJAR_GRASA = "bajar_grasa"
    GANAR_MUSCULO = "ganar_musculo"
    MANTENIMIENTO = "mantenimiento"
    FUERZA = "fuerza"


class LevelEnum(str, Enum):
    """Nivel de experiencia deportiva del usuario (utilizado para Tabla A)."""
    PRINCIPIANTE = "principiante"
    INTERMEDIO = "intermedio"
    AVANZADO = "avanzado"


class SexEnum(str, Enum):
    """Sexo biológico del usuario (campo fijo)."""
    MASCULINO = "masculino"
    FEMENINO = "femenino"
    OTRO = "otro"


class MuscleGroupEnum(str, Enum):
    """Grupos musculares anatómicos principales."""
    PECHO = "pecho"
    ESPALDA = "espalda"
    HOMBROS = "hombros"
    CUADRICEPS = "cuadriceps"
    ISQUIOTIBIALES = "isquiotibiales"
    GLUTEOS = "gluteos"
    BICEPS = "biceps"
    TRICEPS = "triceps"
    CORE = "core"
    GEMELOS = "gemelos"


class MovementPatternEnum(str, Enum):
    """Patrones biomecánicos de movimiento."""
    EMPUJE = "empuje"
    TRACCION = "traccion"
    DOMINANTE_RODILLA = "dominante_rodilla"
    DOMINANTE_CADERA = "dominante_cadera"
    AISLAMIENTO = "aislamiento"
    CORE = "core"


class RiskLevelEnum(str, Enum):
    """Nivel de riesgo o demanda articular del ejercicio."""
    BAJO = "bajo"
    MEDIO = "medio"
    ALTO = "alto"


class DifficultyPerceptionEnum(str, Enum):
    """Dificultad reportada por el usuario al realizar una serie/ejercicio."""
    MUY_FACIL = "muy_facil"
    ADECUADO = "adecuado"
    MUY_PESADO = "muy_pesado"
    FALLO_PREMATURO = "fallo_prematuro"


class UnforeseenTypeEnum(str, Enum):
    """Tipos de imprevistos reportados en la rutina diaria."""
    POCO_TIEMPO = "poco_tiempo"
    MAL_SUENO = "mal_sueno"
    AUSENCIA_PASADA = "ausencia_pasada"
    EVENTO_SOCIAL = "evento_social"
