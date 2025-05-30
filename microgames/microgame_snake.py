from time import sleep

import pygame
import random
from src.layout import draw_frame, show_text
from microgames.microgame_base import MicrojuegoBase
from core.gestor_sprites import Sprite
from core.gestor_audio import Audio
from core.config import Config
from core.utils import ruta_recurso


class SnakeGame(MicrojuegoBase):
    """Microjuego de la serpiente"""
    def __init__(self, screen, tiempo, dificultad=1, infinity=False):
        self.infinity = infinity

        if infinity:
            time = 999
        else:
            time = 8
        super().__init__(screen, time,  dificultad)

        # Margen fijo
        self.margen = 40
        self.audio = Audio()


        # Zona jugable y tamaño de celda
        self.ancho = screen.get_width() - 2 * self.margen
        self.alto = screen.get_height() - 2 * self.margen

        self.tamano_celda_ancho = self.ancho // 18
        self.tamano_celda_alto = self.alto // 18

        self.correction_x = float(self.ancho / 18 - self.tamano_celda_ancho) * 18
        self.correction_y = float(self.alto / 18 - self.tamano_celda_alto) * 18

        self.direccion = "DERECHA"
        self.nueva_direccion = "DERECHA"
        self.win = True

        # Sprites
        self.sprites_serpiente = {
            "cabeza_derecha": Sprite(ruta_recurso("assets/microgames/Solid/head_right.png"), self.tamano_celda_ancho,
                                     self.tamano_celda_alto),
            "cabeza_izquierda": Sprite(ruta_recurso("assets/microgames/Solid/head_left.png"), self.tamano_celda_ancho,
                                       self.tamano_celda_alto),
            "cabeza_arriba": Sprite(ruta_recurso("assets/microgames/Solid/head_up.png"), self.tamano_celda_ancho,
                                    self.tamano_celda_alto),
            "cabeza_abajo": Sprite(ruta_recurso("assets/microgames/Solid/head_down.png"), self.tamano_celda_ancho,
                                   self.tamano_celda_alto),
            "cuerpo_horizontal": Sprite(ruta_recurso("assets/microgames/Solid/body_horizontal.png"), self.tamano_celda_ancho,
                                        self.tamano_celda_alto),
            "cuerpo_vertical": Sprite(ruta_recurso("assets/microgames/Solid/body_vertical.png"), self.tamano_celda_ancho,
                                      self.tamano_celda_alto),
            "curva1": Sprite(ruta_recurso("assets/microgames/Solid/body_bottomleft.png"), self.tamano_celda_ancho,
                             self.tamano_celda_alto),
            "curva2": Sprite(ruta_recurso("assets/microgames/Solid/body_topleft.png"), self.tamano_celda_ancho,
                             self.tamano_celda_alto),
            "curva3": Sprite(ruta_recurso("assets/microgames/Solid/body_topright.png"), self.tamano_celda_ancho,
                             self.tamano_celda_alto),
            "curva4": Sprite(ruta_recurso("assets/microgames/Solid/body_bottomright.png"), self.tamano_celda_ancho,
                             self.tamano_celda_alto),
            "cola_derecha": Sprite(ruta_recurso("assets/microgames/Solid/tail_left.png"), self.tamano_celda_ancho,
                                   self.tamano_celda_alto),
            "cola_izquierda": Sprite(ruta_recurso("assets/microgames/Solid/tail_right.png"), self.tamano_celda_ancho,
                                     self.tamano_celda_alto),
            "cola_arriba": Sprite(ruta_recurso("assets/microgames/Solid/tail_down.png"), self.tamano_celda_ancho,
                                  self.tamano_celda_alto),
            "cola_abajo": Sprite(ruta_recurso("assets/microgames/Solid/tail_up.png"), self.tamano_celda_ancho,
                                 self.tamano_celda_alto)
        }

        self.imagen_derrota = pygame.image.load(ruta_recurso("assets/microgames/Solid/lose.png")).convert_alpha()
        self.imagen_derrota_rect = self.imagen_derrota.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        self.imagen_victoria = pygame.image.load(ruta_recurso("assets/microgames/Solid/win.png")).convert_alpha()
        self.imagen_victoria_rect = self.imagen_derrota.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        # Inicialización serpiente
        self.snake = [
            (self.margen + self.tamano_celda_ancho * 3, self.margen + self.tamano_celda_alto * 5),
            (self.margen + self.tamano_celda_ancho * 2, self.margen + self.tamano_celda_alto * 5),
            (self.margen + self.tamano_celda_ancho * 1, self.margen + self.tamano_celda_alto * 5)
        ]

        self.food = self.generar_comida()
        self.food_sprite = Sprite(ruta_recurso("assets/microgames/Solid/apple.png"), self.tamano_celda_ancho,
                                  self.tamano_celda_alto)

        self.remaining_food = 321 if infinity else (2 + self.dificultad)
        self.derrota = False

    def generar_comida(self):
        """Genera una posición aleatoria para la comida dentro de las celdas disponibles."""
        num_celdas_x = self.ancho // self.tamano_celda_ancho
        num_celdas_y = self.alto // self.tamano_celda_alto
        x = random.randint(0, num_celdas_x - 1) * self.tamano_celda_ancho + self.margen
        y = random.randint(0, num_celdas_y - 1) * self.tamano_celda_alto + self.margen
        return x, y

    def manejar_eventos(self, event):
        """Maneja los eventos del teclado y el ratón."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w and self.direccion != "ABAJO":
                self.nueva_direccion = "ARRIBA"
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s and self.direccion != "ARRIBA":
                self.nueva_direccion = "ABAJO"
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a and self.direccion != "DERECHA":
                self.nueva_direccion = "IZQUIERDA"
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d and self.direccion != "IZQUIERDA":
                self.nueva_direccion = "DERECHA"
            elif event.key == pygame.K_ESCAPE:
                accion = self.menu.mostrar_pausa(self.screen)
                if accion == "continue":
                    pass
                elif accion == "options":
                    self.menu.mostrar_opciones(self.screen)
                elif accion == "exit":
                    return "exit_to_menu"

    def actualizar(self):
        """Actualiza la posición de la serpiente y verifica colisiones."""
        self.direccion = self.nueva_direccion
        x, y = self.snake[0]

        if self.direccion == "ARRIBA":
            y -= self.tamano_celda_alto
        elif self.direccion == "ABAJO":
            y += self.tamano_celda_alto
        elif self.direccion == "IZQUIERDA":
            x -= self.tamano_celda_ancho
        elif self.direccion == "DERECHA":
            x += self.tamano_celda_ancho

        nueva_cabeza = (x, y)

        if (nueva_cabeza in self.snake or
                x < self.margen or y < self.margen or
                x >= self.screen.get_width() - self.margen or
                y >= self.screen.get_height() - self.margen):
            self.win = False

        self.snake.insert(0, nueva_cabeza)

        if nueva_cabeza == self.food:
            self.remaining_food = self.remaining_food - 1
            self.food = self.generar_comida()
        else:
            self.snake.pop()

        if self.remaining_food <= 0:
            self.win = True

    def dibujar_fondo(self):
        """Dibuja el fondo del juego con un patrón de celdas."""
        for i in range(18):
            for j in range(18):
                x = self.margen + i * self.tamano_celda_ancho
                y = self.margen + j * self.tamano_celda_alto

                color = (170, 215, 81) if (i + j) % 2 == 0 else (162, 209, 73)

                if i == 17 or j == 17:
                    pygame.draw.rect(self.screen, color,
                                     (x, y, self.tamano_celda_ancho, self.tamano_celda_alto + self.correction_y))
                else:
                    pygame.draw.rect(self.screen, color, (x, y, self.tamano_celda_ancho, self.tamano_celda_alto))

    def dibujar(self):
        """Dibuja la serpiente, la comida y el texto en pantalla."""
        draw_frame(self.screen)
        self.dibujar_fondo()

        if not self.win:
            text = "Game Over"
        else:
            if self.remaining_food > 1:
                if self.infinity:
                    text = f"{self.remaining_food} manzanas"
                else:
                    text = f"Come: {self.remaining_food} manzanas"
            elif self.remaining_food == 1:
                if not self.infinity:
                    text = f"Come: 1 manzana"
            else:
                text = f"Ganaste!!"

        show_text(self.screen, text, size=40, justificacion='TOP', color=(0, 0, 0), edge=False)

        for i, segmento in enumerate(self.snake):
            x, y = segmento
            if i == 0:
                sprite = self.sprites_serpiente[f"cabeza_{self.direccion.lower()}"]
            elif i == len(self.snake) - 1:
                prev_x, prev_y = self.snake[i - 1]
                dx = prev_x - x
                dy = prev_y - y
                if dx > 0:
                    sprite = self.sprites_serpiente["cola_derecha"]
                elif dx < 0:
                    sprite = self.sprites_serpiente["cola_izquierda"]
                elif dy > 0:
                    sprite = self.sprites_serpiente["cola_abajo"]
                elif dy < 0:
                    sprite = self.sprites_serpiente["cola_arriba"]

            else:
                prev_x, prev_y = self.snake[i - 1]
                next_x, next_y = self.snake[i + 1]

                # Deltas
                dx1 = x - prev_x
                dy1 = y - prev_y
                dx2 = next_x - x
                dy2 = next_y - y

                if dx1 == 0 and dx2 == 0:
                    sprite = self.sprites_serpiente["cuerpo_vertical"]
                elif dy1 == 0 and dy2 == 0:
                    sprite = self.sprites_serpiente["cuerpo_horizontal"]
                else:
                    if (dx1 < 0 and dy2 < 0) or (dy1 < 0 and dx2 < 0):
                        sprite = self.sprites_serpiente["curva1"]
                    elif (dx1 > 0 > dy2) or (dy1 < 0 < dx2):
                        sprite = self.sprites_serpiente["curva2"]
                    elif (dx1 > 0 and dy2 > 0) or (dy1 > 0 and dx2 > 0):
                        sprite = self.sprites_serpiente["curva3"]
                    elif (dx1 < 0 < dy2) or (dy1 > 0 > dx2):
                        sprite = self.sprites_serpiente["curva4"]

            sprite.actualizar_posicion(x, y)
            sprite.dibujar(self.screen)

        self.food_sprite.actualizar_posicion(*self.food)
        self.food_sprite.dibujar(self.screen)

    def mostrar_derrota(self):
        """Muestra la pantalla de derrota con una superposición oscura y la imagen de derrota."""
        self.audio.detener()
        self.audio.reproducir("BooBoo.mp3")

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))

        # Dibujar la superposición en la pantalla
        self.screen.blit(overlay, (0, 0))

        # Dibujar la imagen de derrota
        self.screen.blit(self.imagen_derrota, self.imagen_derrota_rect)
        pygame.display.flip()

        self.screen.blit(self.imagen_derrota, self.imagen_derrota_rect)
        pygame.display.flip()


    def mostrar_victoria(self):
        """Muestra la pantalla de victoria"""
        self.audio.detener()
        self.audio.reproducir("Fnaf.mp3")
        self.remaining_food -= 1

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))

        # Dibujar la superposición en la pantalla
        self.screen.blit(overlay, (0, 0))

        # Dibujar la imagen de derrota
        self.screen.blit(self.imagen_victoria, self.imagen_victoria_rect)
        pygame.display.flip()

        self.screen.blit(self.imagen_victoria, self.imagen_victoria_rect)
        pygame.display.flip()

    def ejecutar(self):
        self.audio.reproducir("Snake.mp3")
        if Config.mostrar_ayuda:
            self.mostrar_controles(self.screen, "\nFlechas direccionales/WASD para mover a la serpiente")

        reloj = pygame.time.Clock()
        inicio = pygame.time.get_ticks()

        while True:
            if self.win:
                if self.remaining_food > 0:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return False
                        resultado = self.manejar_eventos(event)
                        if resultado == "exit_to_menu":
                            return "exit_to_menu"
                    self.actualizar()
                    self.dibujar()

                elif self.remaining_food == 0:
                    self.mostrar_victoria()
            elif not self.derrota:
                self.derrota = True
                self.mostrar_derrota()
                if self.infinity:
                    sleep(4)
                    return False

            pygame.display.flip()

            if (pygame.time.get_ticks() - inicio) / 1000 > self.tiempo_limite:
                self.audio.detener()
                return self.win and self.remaining_food == -1

            reloj.tick(10)
