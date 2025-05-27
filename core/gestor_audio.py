import pygame


class Audio:
    def __init__(self):
        pygame.mixer.init()
        self.volumen = 0.5
        pygame.mixer.music.set_volume(self.volumen)

    def set_volumen(self, valor):
        self.volumen = max(0, min(1, valor))
        pygame.mixer.music.set_volume(self.volumen)

    def get_volumen(self):
        return self.volumen
    def reproducir(self, archivo, loop=False):
        """Reproduce una música con opción de loop"""
        pygame.mixer.music.load(f"../assets/musica/{archivo}")
        pygame.mixer.music.play(-1 if loop else 0)

    def detener(self):
        """Detiene la música"""
        pygame.mixer.music.stop()
