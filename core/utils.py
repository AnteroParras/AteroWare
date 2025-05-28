import os
import sys

def ruta_recurso(rel_path):
    """Obtiene la ruta absoluta a un recurso, compatible con PyInstaller."""
    try:
        base_path = sys._MEIPASS  # cuando se ejecuta el .exe
    except AttributeError:
        base_path = os.path.abspath(".")  # cuando se ejecuta como .py

    return os.path.join(base_path, rel_path)