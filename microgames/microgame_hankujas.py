import random
import pygame
from src.layout import draw_frame, show_text
from microgames.microgame_base import MicrojuegoBase
from core.gestor_sprites import Sprite


class MicrojuegoExplotarBurbujas(MicrojuegoBase):
    def __init__(self, screen, time, dificultad=1):
        super().__init__(screen, time, dificultad=dificultad)
        # self.musica = "A1.mp3"  # Música del minijuego
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
                bubble = Sprite("../assets/microgames/explotar_burbujas/bad.png", self.num_x, self.num_y)
            else:
                bubble = Sprite("../assets/microgames/explotar_burbujas/good.png", self.num_x, self.num_y)

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
                            bubble.image = pygame.image.load("../assets/microgames/explotar_burbujas/good.png")
                            bubble.image = pygame.transform.scale(bubble.image, (self.num_x, self.num_y))

    def actualizar(self):
        """Actualizar estado del minijuego"""
        if len(self.selected_targets) == 0:  # Si explotaron todas las necesarias
            self.win = True  # Minijuego ganado

    def dibujar(self):
        """Dibuja los sprites en pantalla"""
        self.screen.fill((255, 255, 255))  # Fondo blanco
        draw_frame()
        self.bubbles.draw(self.screen)

        if not self.win:
            show_text("Haz feliz a Hank!!", justificacion="TOP")
        else:
            show_text("Ole que ole!!", justificacion="TOP")
        pygame.display.flip()
