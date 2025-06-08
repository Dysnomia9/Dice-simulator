# Paquete GUI para el Simulador de Dados
# Este archivo hace que Python reconozca la carpeta gui como un paquete

__version__ = "1.0.0"
__author__ = "Simulador de Dados"

# Importaciones opcionales para facilitar el uso
from .main_window import SimuladorDados

__all__ = ['SimuladorDados']