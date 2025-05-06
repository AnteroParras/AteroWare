import pygame
import globals_config as gc

from core.gestor_audio import Audio
from core.gestor_microgames import GameManager
from core.gestor_menus import Menu

from layout import init, inner_time_safe_life, show_text, fill_screen, screen


# Inicialización de pygame y variables
pygame.init()
init()
menu = Menu(screen)

# Mostrar el menú principal

# Bucle principal del juego
running = True
games_played = 0
control_audio = Audio()
control_juegos = GameManager(screen=screen)

jugar = False


def bucle_juego(LIVES=3, games_played=0, running=True):
    while running and LIVES > 0 and not control_juegos.isTerminado():
        control_audio.reproducir(archivo="Pirim.mp3")
        inner_time_safe_life(2)
        control_audio.detener()

        result = control_juegos.ejecutar_microjuego(7)  # Ejecuta el minijuego

        games_played += 1

        if result == "T":
            return False

        if not result:
            gc.LIVES -= 1  # Pierde una vida si falla

        if gc.LIVES <= 0 or control_juegos.isTerminado():
            running = False  # Si no quedan minijuegos o vidas pierdes

    if gc.LIVES > 0:
        fill_screen("WHITE")
        show_text("Ole ole los caracoles")
        pygame.display.flip()
        menu.mostrar_menu(screen)

    else:
        fill_screen("RED")
        pygame.display.flip()


while True:
    if not jugar:
        jugar = menu.mostrar_menu(screen)
    else:
        jugar = bucle_juego()

