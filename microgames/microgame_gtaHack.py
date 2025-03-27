import random
import pygame
from src.layout import draw_frame, show_text
from microgames.microgame_base import MicrojuegoBase
from core.gestor_sprites import Sprite


class MicrojuegoHackearGTA(MicrojuegoBase):
    def __init__(self, screen, time, dificultad=1):
        super().__init__(screen, 100, dificultad=dificultad)
        #self.musica = "A1.mp3"  # Música del minijuego
        self.desfase = 40
        self.words = pygame.sprite.Group()  # Grupo de sprites
        self.change_time = 1 / dificultad
        self.clicked_targets = [False, False, False, False, False]
        self.targets = []
        self.num_x = (self.screen.get_width() - self.desfase * 2) // 5  # Ancho de burbujas
        self.num_y = (self.screen.get_height() - self.desfase * 2) // 7  # Alto de burbujas

        self.pos_obj = [0, 0, 0, 0, 0]
        self.cargar_sprites()

    def cargar_sprites(self):
        grid = []  # Para almacenar posiciones organizadas por columnas

        for col in range(5):
            column_positions = []
            for row in range(7):
                x = col * self.num_x + self.desfase
                y = row * self.num_y + self.desfase
                column_positions.append((x + self.num_x // 2, y + self.num_y // 2))
            grid.append(column_positions)

        # Seleccionar un índice aleatorio en cada columna
        selected_targets = set()
        for col_positions in grid:
            selected_targets.add(random.choice(col_positions))

        for col_positions in grid:
            for x, y in col_positions:
                if (x, y) in selected_targets:
                    palabro = Sprite("../assets/microgames/gtaHack/Si.png", self.num_x, self.num_y)
                    self.pos_obj.append(y + 37)

                else:
                    palabro = Sprite("../assets/microgames/gtaHack/No.png", self.num_x, self.num_y)
                palabro.actualizar_posicion(x - self.num_x // 2, y - self.num_y // 2)
                self.words.add(palabro)

    def manejar_eventos(self, event):
        """Detecta si una burbuja fue explotada con un clic"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            index = None
            for i in range(len(self.clicked_targets)):
                if not self.clicked_targets[i]:
                    index = i
                    break
            print(f"Supuesta posicion: {(self.num_y * 4) + 77}, indice {index}")
            if index is not None:
                if self.pos_obj[index] == (self.num_y * 4) + 77:
                    self.clicked_targets[index] = True
                    print("Clickao")

    def actualizar(self):
        """Actualizar estado del minijuego"""
        self.change_time -= 1 / 10

        if self.change_time <= 0:
            self.change_time = 1 / self.dificultad

            for sprite in self.words:
                temporal = sprite.rect.y + self.num_y
                if temporal >= self.screen.get_height() - self.desfase - self.num_y // 2:
                    sprite.rect.y = self.desfase
                else:
                    sprite.rect.y = temporal

        for i in range(len(self.pos_obj)):
            self.pos_obj[i] += self.num_y
            if self.pos_obj[i] >= self.screen.get_height() - self.desfase - self.num_y // 2:
                self.pos_obj[i] = self.desfase + 37
        if self.clicked_targets[-1]:  # Si explotaron todas las necesarias
            self.win = True  # Minijuego ganado

    def dibujar(self):
        """Dibuja los sprites en pantalla"""
        self.screen.fill((255, 255, 255))  # Fondo blanco
        draw_frame()
        self.words.draw(self.screen)
        pygame.display.flip()
