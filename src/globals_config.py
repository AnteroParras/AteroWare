# Parámetros del juego
import pygame

MINIGAME_TIME = 5  # Duración de cada minijuego en segundos
INTERVAL_TIME = 5
LIVES = 3  # Número de vidas
LOST_LIVES = 0
TOTAL_LIVES = 3
LEVEL = 1

clock = pygame.time.Clock()

def increase_dificult():
    global MINIGAME_TIME, INTERVAL_TIME, LEVEL
    LEVEL += 1
    MINIGAME_TIME *= 0.8
    INTERVAL_TIME *= 0.8
