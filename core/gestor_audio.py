import pygame
from core.utils import ruta_recurso


class Audio:
    """Clase que gestiona la reproducción de música en el juego."""
    def __init__(self):
        """Inicializa el gestor de audio y establece el volumen inicial"""
        pygame.mixer.init()
        self.volumen = 0.5
        pygame.mixer.music.set_volume(self.volumen)

    def set_volumen(self, valor):
        """Establece el volumen de la música"""
        self.volumen = max(0, min(1, valor))
        pygame.mixer.music.set_volume(self.volumen)

    def get_volumen(self):
        """Obtiene el volumen actual de la música"""
        return self.volumen

    def reproducir(self, archivo, loop=False):
        """Reproduce una música con opción de loop"""
        pygame.mixer.music.load(ruta_recurso(f"assets/musica/{archivo}"))
        pygame.mixer.music.play(-1 if loop else 0)

    def detener(self):
        """Detiene la música"""
        pygame.mixer.music.stop()
