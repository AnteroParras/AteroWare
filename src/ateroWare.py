import pygame

from core.gestor_audio import Audio
from core.gestor_microgames import GameManager
from core.gestor_menus import Menu

from layout import inner_time_safe_life, fill_screen


# Inicialización de pygame y variables
class AteroWare:
    """Clase principal del juego AteroWare"""

    def __init__(self):
        self.LIVES = 3
        self.games_played = 0
        self.running = True
        self.jugar = False

        self.screen = pygame.display.set_mode((800, 692))
        pygame.display.set_caption("AteroWare")

        self.menu = Menu(self.screen)
        self.control_audio = Audio()
        self.control_juegos = GameManager(screen=self.screen)

    def reiniciar(self):
        """Reinicia el juego a sus valores iniciales"""
        self.LIVES = 3
        self.games_played = 0
        self.running = True
        self.jugar = False

        self.screen = pygame.display.set_mode((800, 692))
        pygame.display.set_caption("AteroWare")

        self.menu = Menu(self.screen)
        self.control_audio = Audio()
        self.control_juegos = GameManager(screen=self.screen)

    def bucle_juego(self):
        """Bucle principal del juego, controla la lógica del juego y los microjuegos"""
        while self.running and self.LIVES > 0 and not self.control_juegos.isTerminado():
            self.control_audio.reproducir(archivo="Pirim.mp3")
            inner_time_safe_life(self.screen, 2, self.LIVES)
            self.control_audio.detener()

            result = self.control_juegos.ejecutar_microjuego(7)

            self.games_played += 1

            if result == "T":
                return False

            if not result:
                self.LIVES -= 1

            if self.LIVES <= 0 or self.control_juegos.isTerminado():
                self.running = False

        self.reiniciar()

        if self.LIVES > 0:
            self.screen.fill((255, 255, 255))
            pygame.display.flip()
            self.menu.mostrar_menu(self.screen)
            return False

        else:
            fill_screen(self.screen, "RED")
            pygame.display.flip()

    def bucle_principal(self):
        """Muestra el menú principal y controla la lógica del juego"""
        while True:
            if not self.jugar:
                self.jugar = self.menu.mostrar_menu(self.screen)
                self.LIVES = 3
            else:
                self.jugar = self.bucle_juego()


pygame.init()
AteroWare = AteroWare()
AteroWare.bucle_principal()
