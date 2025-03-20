import pygame
from core.gestor_audio import Audio
from core.gestor_microgames import GameManager

import globals_config as gc

from layout import init, inner_time_safe_life, show_text, fill_screen, screen

from microgames_prev import all_microgames_list

""" Inicializacion de variables y pantalla"""
pygame.init()
init()

MINIGAMES = all_microgames_list()
running = True
games_played = 0

""" Bucle principal del juego """
control_audio = Audio()
control_juegos = GameManager(screen=screen)

while running and gc.LIVES > 0 and len(MINIGAMES) > 0:

    control_audio.reproducir(archivo="A1.mp3")
    inner_time_safe_life(gc.INTERVAL_TIME)
    control_audio.detener()

    result = control_juegos.ejecutar_microjuego(7)  # Ejecuta el minijuego

    games_played += 1

    if not result:
        gc.LIVES -= 1  # Pierde una vida si falla

    if gc.LIVES <= 0 or len(MINIGAMES) == 0:
        running = False # Si no quedan minijuegos o vidas pierdes
    gc.increase_dificult()


if gc.LIVES > 0:
    fill_screen("WHITE")
    show_text("Ole ole los caracoles")
    pygame.display.flip()

else:
    fill_screen("RED")
    pygame.display.flip()

pygame.time.wait(2000)  # Espera 2 segundos antes de cerrar
pygame.quit()
