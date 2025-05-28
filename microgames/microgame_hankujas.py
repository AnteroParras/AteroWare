import random
import pygame
from src.layout import draw_frame, show_text
from microgames.microgame_base import MicrojuegoBase
from core.gestor_sprites import Sprite
from core.config import Config
from core.utils import ruta_recurso


class MicrojuegoExplotarBurbujas(MicrojuegoBase):
    """Microjuego donde el jugador debe hacer clic en hanks tristes para hacerlas felices."""
    def __init__(self, screen, time, dificultad=1):
        super().__init__(screen, time, dificultad=dificultad)

        self.desfase = 40
        self.clicked_targets = set()
        self.num_x = (self.screen.get_width() - self.desfase * 2) // 8  # Ancho de burbujas
        self.num_y = (self.screen.get_height() - self.desfase * 2) // 4  # Alto de burbujas
        self.radius = min(self.num_x, self.num_y) // 2  # Radio de detección
        self.targets = []
        self.bubbles = pygame.sprite.Group()  # Grupo de sprites
        self.selected_targets = set()
        self.num_of_targets = 3 + int((dificultad-1)*1.5)

        self.win = False
        self.musica = "man.mp3"

        self.cargar_sprites()

    def cargar_sprites(self):
        """Crea las burbujas en la pantalla"""
        for row in range(4):
            for col in range(8):
                x = col * self.num_x + self.desfase
                y = row * self.num_y + self.desfase
                self.targets.append((x + self.num_x // 2, y + self.num_y // 2))  # Centro de la burbuja

        self.selected_targets = set(random.sample(range(len(self.targets)), self.num_of_targets))  # Seleccionadas

        for i, (x, y) in enumerate(self.targets):
            if i in self.selected_targets:
                bubble = Sprite(ruta_recurso("assets/microgames/explotar_burbujas/bad.png"), self.num_x, self.num_y)
            else:
                bubble = Sprite(ruta_recurso("assets/microgames/explotar_burbujas/good.png"), self.num_x, self.num_y)

            bubble.actualizar_posicion(x - self.num_x // 2, y - self.num_y // 2)
            self.bubbles.add(bubble)

    def manejar_eventos(self, event):
        """Detecta si una burbuja fue explotada con un clic"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            for i, (x, y) in enumerate(self.targets):
                if i in self.selected_targets and (mx - x) ** 2 + (my - y) ** 2 <= self.radius ** 2:
                    self.clicked_targets.add(i)
                    self.selected_targets.remove(i)

                    # Cambiar la imagen de la burbuja explotada
                    for bubble in self.bubbles:
                        if bubble.rect.collidepoint(mx, my):
                            bubble.image = pygame.image.load(ruta_recurso("assets/microgames/explotar_burbujas/good.png"))
                            bubble.image = pygame.transform.scale(bubble.image, (self.num_x, self.num_y))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                accion = self.menu.mostrar_pausa(self.screen)
                if accion == "continue":
                    # simplemente salimos del menú de pausa
                    pass
                elif accion == "options":
                    self.menu.mostrar_opciones(self.screen)
                    # al cerrar opciones volverá aquí y saldrá de pausa
                elif accion == "exit":
                    # retornamos una señal para que el bucle superior maneje la salida
                    return "exit_to_menu"

    def actualizar(self):
        """Actualizar estado del minijuego"""
        if len(self.selected_targets) == 0:  # Si explotaron todas las necesarias
            self.win = True  # Minijuego ganado

    def dibujar(self):
        """Dibuja los sprites en pantalla"""
        self.screen.fill((255, 255, 255))
        draw_frame(self.screen)
        self.bubbles.draw(self.screen)

        if not self.win:
            show_text(self.screen, "Haz feliz a Hank!!", justificacion="TOP")
        else:
            show_text(self.screen,"Ole que ole!!", justificacion="TOP")
        pygame.display.flip()

    def ejecutar(self):
        """Ejecuta el bucle del minijuego y devuelve si ganó o perdió"""
        self.audio.reproducir(self.musica)
        if Config.mostrar_ayuda:
            self.mostrar_controles(self.screen, "\n¡Click Izquierdo en las caras tristes!")

        reloj = pygame.time.Clock()
        inicio = pygame.time.get_ticks()

        while True:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                resultado = self.manejar_eventos(event)
                if resultado == "exit_to_menu":
                    return "exit_to_menu"  # volver al menú

            self.actualizar()
            self.dibujar()
            pygame.display.flip()

            # Verifica si se acabó el tiempo
            if (pygame.time.get_ticks() - inicio) / 1000 > self.tiempo_limite:
                return self.win  # Minijuego perdido
                self.audio.detener()

            reloj.tick(30)