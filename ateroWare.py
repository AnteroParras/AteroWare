import pygame
import random
import globals_config as gc

from layout import init, inner_time_safe_life, show_text, fill_screen, COLORS as cl

from microgames import all_microgames_list

""" Inicializacion de variables y pantalla"""
pygame.init()
init()

MINIGAMES = all_microgames_list()
running = True

""" Bucle principal del juego """
while running and gc.LIVES > 0 and len(MINIGAMES) > 0:
    inner_time_safe_life(5)
    minigame = random.choice(MINIGAMES)  # Selecciona minijuego aleatorio
    MINIGAMES.remove(minigame)
    result = minigame()  # Ejecuta el minijuego

    if not result:
        gc.LIVES -= 1  # Pierde una vida si falla

    if gc.LIVES <= 0 or len(MINIGAMES) == 0:
        running = False # Si no quedan minijuegos o vidas pierdes


# Pantalla de Game Over
if gc.LIVES > 0:
    fill_screen("White")
    show_text("Ole ole los caracoles")
    pygame.display.flip()

else:
    fill_screen("RED")
    pygame.display.flip()

pygame.time.wait(2000)  # Espera 2 segundos antes de cerrar
pygame.quit()
