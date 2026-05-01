from dataclasses import dataclass
from typing import Optional

@dataclass
class Materia:
    """Modelo de dominio para materia"""
    id_materia: int
    nombre: str
    division: str

    def __post__init__(self):
        """Validación básica al crear instancia"""
        if not self.nombre or len(self.nombre.strip()) == 0:
            raise ValueError("El nombre de la materia no puede estar vacio")
        if not self.division or len(self.division.strip()) == 0:
            raise ValueError("La division no puede estar vacia")
    def to_dict(self) -> dict:
        return{
            "id_materia": self.id_materia,
            "nombre": self.nombre,
            "division":self.division
        }
    