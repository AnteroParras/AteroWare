import pygame


class Audio:
    def __init__(self):
        pygame.mixer.init()

    def reproducir(self, archivo, loop=False):
        """Reproduce una música con opción de loop"""
        pygame.mixer.music.load(f"../assets/musica/{archivo}")
        pygame.mixer.music.play(-1 if loop else 0)

    def detener(self):
        """Detiene la música"""
        pygame.mixer.music.stop()
