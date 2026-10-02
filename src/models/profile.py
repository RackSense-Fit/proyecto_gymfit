"""
Modelo inmutable del perfil del usuario (UserProfile).
Distingue claramente entre campos fijos y editables.
"""
from dataclasses import dataclass
from src.models.enums import GoalEnum, LevelEnum, SexEnum


@dataclass(frozen=True)
class UserProfile:
    """
    Representa el perfil inmutable del usuario.
    
    Campos Fijos:
        - nombre: Nombre de pila o identificador del usuario.
        - sexo: Sexo biológico del usuario (para cálculos fisiológicos/antropométricos).
        
    Campos Editables (generan una nueva instancia de UserProfile sin mutar la previa):
        - peso_kg: Peso corporal en kilogramos.
        - altura_cm: Estatura en centímetros.
        - objetivo: Meta de entrenamiento (bajar_grasa, ganar_musculo, mantenimiento, fuerza).
        - nivel: Nivel de experiencia (principiante, intermedio, avanzado).
        - dias_disponibles: Número de días por semana que el usuario puede entrenar (1 a 7).
    """
    # Campos Fijos
    nombre: str
    sexo: SexEnum
    
    # Campos Editables
    peso_kg: float
    altura_cm: float
    objetivo: GoalEnum
    nivel: LevelEnum
    dias_disponibles: int

    def __post_init__(self) -> None:
        """Validaciones puras de integridad del dominio."""
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if self.peso_kg <= 0:
            raise ValueError("El peso debe ser un valor positivo en kg.")
        if self.altura_cm <= 0:
            raise ValueError("La altura debe ser un valor positivo en cm.")
        if not (1 <= self.dias_disponibles <= 7):
            raise ValueError("Los días disponibles deben estar entre 1 y 7 por semana.")

    @property
    def imc(self) -> float:
        """Calcula el Índice de Masa Corporal (IMC) de forma pura."""
        altura_m = self.altura_cm / 100.0
        return round(self.peso_kg / (altura_m ** 2), 2)
