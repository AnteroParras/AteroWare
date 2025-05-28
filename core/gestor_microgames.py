import pygame

from microgames.microgame_hankujas import MicrojuegoExplotarBurbujas
from microgames.microgame_diana import MicrojuegoDispararFlecha
from microgames.microgame_snake import SnakeGame
from microgames.macro_pong4D import Pong4D
from core.gestor_audio import Audio
from microgames.microgame_tetris import Tetris
from microgames.microgame_pollovolador import MicrojuegoFlappyBird

class GameManager:
    """Clase que gestiona los microjuegos y el macrojuego final."""
    def __init__(self, screen):
        self.screen = screen
        self.minijuegos = [Tetris, SnakeGame, MicrojuegoExplotarBurbujas, MicrojuegoDispararFlecha, MicrojuegoFlappyBird]  # Lista de clases de minijuegos
        self.indice = 0  # Lleva el progreso
        self.dificultad = 1
        self.macro_win = False

    def reiniciar(self):
        """Reinicia el gestor de microjuegos a su estado inicial."""
        self.indice = 0

    def ejecutar_microjuego(self, time):
        """Ejecuta el microjuego actual o el macrojuego final si se han completado todos los microjuegos."""
        if self.indice >= len(self.minijuegos) :
            self.epic_final_intro()
            macrojuego = Pong4D(self.screen, time, self.dificultad)
            self.macro_win = macrojuego.ejecutar()

        else:
            # Ejecutar el minijuego
            minijuego = self.minijuegos[self.indice](self.screen, time, self.dificultad)
            resultado = minijuego.ejecutar()
            self.indice += 1

            if resultado == "exit_to_menu":
                self.indice = 0
                return "T"  # o la lógica que haga volver al menú

            return resultado or self.macro_win

    def isTerminado(self):
        """Verifica si se han completado todos los microjuegos y se ha ganado el macrojuego."""
        return self.macro_win

    def subir_dificultad(self):
        """Aumenta la dificultad del juego."""
        self.dificultad += 1

    def siguiente_vuelta(self):
        """Activa la siguiente vuelta."""
        self.indice = 0
        self.subir_dificultad()

    def simular_crasheo(self, screen):
        """Simula un fallo del programa con un mensaje humorístico."""
        import pygame
        import tkinter as tk
        from tkinter import messagebox
        import time

        """Simula un fallo del programa con un mensaje humorístico."""
        # Crear ventana de "El programa no responde" con tkinter
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal de tkinter
        messagebox.showwarning("Pygame: Tkinter exception",
                               """pygame 2.0.1 (SDL 2.0.14, Python 3.9.6)
Hello from the pygame community. https://www.pygame.org/contribute.html
2021-07-16 16:21:32.761 Python[5395:130550] -[SDLApplication _setup:]: unrecognized selector sent to instance 0x7fdfd0d0fed0
2021-07-16 16:21:32.763 Python[5395:130550] *** Terminating app due to uncaught exception 'NSInvalidArgumentException', reason: '-[SDLApplication _setup:]: unrecognized selector sent to instance 0x7fdfd0d0fed0'
*** First throw call stack:
(
        0   CoreFoundation                      0x00007fff4d7e4a7d __exceptionPreprocess + 256
        1   libobjc.A.dylib                     0x00007fff77eb8a17 objc_exception_throw + 48
        2   CoreFoundation                      0x00007fff4d85e886 -[NSObject(NSObject) __retain_OA] + 0
        3   CoreFoundation                      0x00007fff4d7868ef ___forwarding___ + 1485
        ...
       """)

        # Cerrar la ventana de pygame
        pygame.display.quit()

        # Esperar 1-2 segundos
        time.sleep(2)

        # Mostrar ventana humorística con sonido
        self.audio = Audio()
        self.music_file = "ururur.mp3"
        self.audio.reproducir(self.music_file)
        messagebox.showinfo("Solución encontrada", "Fallo mio, me falto un punto y coma")

    def epic_final_intro(self):
        """Muestra una introducción épica para el minijuego final >:]."""
        font = pygame.font.Font(None, 74)
        self.audio = Audio()
        self.music_file = "Preludio.mp3"
        self.audio.reproducir(self.music_file)

        messages = ["¡El desafío final comienza!", "Prepárate...", "3", "2", "1", "¡Vamos!"]
        for message in messages:
            self.screen.fill((0, 0, 0))  # Fondo negro
            text = font.render(message, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(1500)  # Espera 1.5 segundo entre mensajes

        self.audio.detener()
        self.simular_crasheo(self.screen)  # Simula un fallo del programa
