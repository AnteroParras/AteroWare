import pygame
from core.gestor_sprites import Sprite
from core.gestor_audio import Audio
from core.gestor_menus import Menu

class MicrojuegoBase:
    def __init__(self, screen, tiempo, dificultad=1):
        self.screen = screen
        self.sprites = []  # Lista de sprites del minijuego
        self.audio = Audio()
        self.tiempo_limite = tiempo  # Segundos para completar el minijuego
        self.win = False
        self.dificultad = dificultad
        self.musica = None # Música del minijuego
        self.menu = Menu(screen)

    def cargar_sprites(self):
        """Carga los sprites específicos del minijuego (sobreescrito en hijos)."""
        pass

    def reproducir_musica(self):
        """Reproduce la música del minijuego"""
        self.audio.reproducir(self.audio)

    def manejar_eventos(self, event):
        """Maneja eventos del minijuego (clics, teclas, etc.)"""
        pass

    def actualizar(self):
        """Lógica del minijuego"""
        pass

    def dibujar(self):
        """Dibuja los sprites en pantalla"""
        for sprite in self.sprites:
            sprite.dibujar(self.screen)

    def ejecutar(self):
        """Ejecuta el bucle del minijuego y devuelve si ganó o perdió"""
        self.audio.reproducir(self.musica)
        reloj = pygame.time.Clock()
        inicio = pygame.time.get_ticks()

        while True:
            self.screen.fill((0, 0, 0))  # Fondo negro
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                resultado = self.manejar_eventos(event)
                if resultado == "exit_to_menu":
                    return "exit_to_menu"  # o la lógica que haga volver al menú

            self.actualizar()
            self.dibujar()
            pygame.display.flip()

            # Verifica si se acabó el tiempo
            if (pygame.time.get_ticks() - inicio) / 1000 > self.tiempo_limite:
                return self.win  # Minijuego perdido
                self.audio.detener()

            reloj.tick(30)
