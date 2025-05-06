import pygame
import random
from src.layout import draw_frame, show_text
from microgames.microgame_base import MicrojuegoBase
from core.gestor_sprites import Sprite
from core.gestor_audio import Audio

class SnakeGame(MicrojuegoBase):
    def __init__(self, screen, tiempo, dificultad=1, infinity=False):
        super().__init__(screen, 8, dificultad)

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
            "cabeza_derecha": Sprite("../assets/microgames/Solid/head_right.png", self.tamano_celda_ancho,
                                     self.tamano_celda_alto),
            "cabeza_izquierda": Sprite("../assets/microgames/Solid/head_left.png", self.tamano_celda_ancho,
                                       self.tamano_celda_alto),
            "cabeza_arriba": Sprite("../assets/microgames/Solid/head_up.png", self.tamano_celda_ancho,
                                    self.tamano_celda_alto),
            "cabeza_abajo": Sprite("../assets/microgames/Solid/head_down.png", self.tamano_celda_ancho,
                                   self.tamano_celda_alto),
            "cuerpo_horizontal": Sprite("../assets/microgames/Solid/body_horizontal.png", self.tamano_celda_ancho,
                                        self.tamano_celda_alto),
            "cuerpo_vertical": Sprite("../assets/microgames/Solid/body_vertical.png", self.tamano_celda_ancho,
                                      self.tamano_celda_alto),
            "curva1": Sprite("../assets/microgames/Solid/body_bottomleft.png", self.tamano_celda_ancho,
                             self.tamano_celda_alto),
            "curva2": Sprite("../assets/microgames/Solid/body_topleft.png", self.tamano_celda_ancho,
                             self.tamano_celda_alto),
            "curva3": Sprite("../assets/microgames/Solid/body_topright.png", self.tamano_celda_ancho,
                             self.tamano_celda_alto),
            "curva4": Sprite("../assets/microgames/Solid/body_bottomright.png", self.tamano_celda_ancho,
                             self.tamano_celda_alto),
            "cola_derecha": Sprite("../assets/microgames/Solid/tail_left.png", self.tamano_celda_ancho,
                                   self.tamano_celda_alto),
            "cola_izquierda": Sprite("../assets/microgames/Solid/tail_right.png", self.tamano_celda_ancho,
                                     self.tamano_celda_alto),
            "cola_arriba": Sprite("../assets/microgames/Solid/tail_down.png", self.tamano_celda_ancho,
                                  self.tamano_celda_alto),
            "cola_abajo": Sprite("../assets/microgames/Solid/tail_up.png", self.tamano_celda_ancho,
                                 self.tamano_celda_alto)
        }

        self.imagen_derrota = pygame.image.load("../assets/microgames/Solid/lose.png").convert_alpha()
        self.imagen_derrota_rect = self.imagen_derrota.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        self.imagen_victoria = pygame.image.load("../assets/microgames/Solid/win.png").convert_alpha()
        self.imagen_victoria_rect = self.imagen_derrota.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        # Inicialización serpiente en la parte superior izquierda
        self.snake = [
            (self.margen + self.tamano_celda_ancho * 3, self.margen + self.tamano_celda_alto * 5),
            (self.margen + self.tamano_celda_ancho * 2, self.margen + self.tamano_celda_alto * 5),
            (self.margen + self.tamano_celda_ancho * 1, self.margen + self.tamano_celda_alto * 5)
        ]

        self.food = self.generar_comida()
        self.food_sprite = Sprite("../assets/microgames/Solid/apple.png", self.tamano_celda_ancho,
                                  self.tamano_celda_alto)

        self.remaining_food = 321 if infinity else (2 + self.dificultad)
        self.derrota = False

    def generar_comida(self):
        num_celdas_x = self.ancho // self.tamano_celda_ancho
        num_celdas_y = self.alto // self.tamano_celda_alto
        x = random.randint(0, num_celdas_x - 1) * self.tamano_celda_ancho + self.margen
        y = random.randint(0, num_celdas_y - 1) * self.tamano_celda_alto + self.margen
        return x, y

    def manejar_eventos(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direccion != "ABAJO":
                self.nueva_direccion = "ARRIBA"
            elif event.key == pygame.K_DOWN and self.direccion != "ARRIBA":
                self.nueva_direccion = "ABAJO"
            elif event.key == pygame.K_LEFT and self.direccion != "DERECHA":
                self.nueva_direccion = "IZQUIERDA"
            elif event.key == pygame.K_RIGHT and self.direccion != "IZQUIERDA":
                self.nueva_direccion = "DERECHA"
            elif event.key == pygame.K_ESCAPE:
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
        draw_frame()
        self.dibujar_fondo()

        if not self.win:
            text = "Game Over"
        else:
            if self.remaining_food > 1:
                text = f"Come: {self.remaining_food} manzanas"
            elif self.remaining_food == 1:
                text = f"Come: 1 manzana"
            else:
                text = f"Ganaste!!"

        show_text(text, size=40, justificacion='TOP', color=(0, 0, 0), edge=False)

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
                        sprite = self.sprites_serpiente["curva1"]  # ↖
                    elif (dx1 > 0 > dy2) or (dy1 < 0 < dx2):
                        sprite = self.sprites_serpiente["curva2"]  # ↗
                    elif (dx1 > 0 and dy2 > 0) or (dy1 > 0 and dx2 > 0):
                        sprite = self.sprites_serpiente["curva3"]  # ↘
                    elif (dx1 < 0 < dy2) or (dy1 > 0 > dx2):
                        sprite = self.sprites_serpiente["curva4"]  # ↙

            sprite.actualizar_posicion(x, y)
            sprite.dibujar(self.screen)

        self.food_sprite.actualizar_posicion(*self.food)
        self.food_sprite.dibujar(self.screen)

    def mostrar_derrota(self):
        self.audio.detener()
        self.audio.reproducir("BooBoo.mp3")

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Negro con 150 de opacidad

        # Dibujar la superposición en la pantalla
        self.screen.blit(overlay, (0, 0))

        # Dibujar la imagen de derrota
        self.screen.blit(self.imagen_derrota, self.imagen_derrota_rect)
        pygame.display.flip()

        self.screen.blit(self.imagen_derrota, self.imagen_derrota_rect)
        pygame.display.flip()

    def mostrar_victoria(self):
        self.audio.detener()
        self.audio.reproducir("Fnaf.mp3")
        self.remaining_food -= 1

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Negro con 150 de opacidad

        # Dibujar la superposición en la pantalla
        self.screen.blit(overlay, (0, 0))

        # Dibujar la imagen de derrota
        self.screen.blit(self.imagen_victoria, self.imagen_victoria_rect)
        pygame.display.flip()

        self.screen.blit(self.imagen_victoria, self.imagen_victoria_rect)
        pygame.display.flip()

    def ejecutar(self):
        self.audio.reproducir("Snake.mp3")

        reloj = pygame.time.Clock()
        inicio = pygame.time.get_ticks()

        while True:
            if self.win:
                if self.remaining_food > 0:
                    print(self.win)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return False
                        resultado = self.manejar_eventos(event)
                        if resultado == "exit_to_menu":
                            return False
                    self.actualizar()
                    self.dibujar()

                elif self.remaining_food == 0:
                    self.mostrar_victoria()
            elif not self.derrota:
                self.derrota = True
                self.mostrar_derrota()

            pygame.display.flip()

            if (pygame.time.get_ticks() - inicio) / 1000 > self.tiempo_limite:
                self.audio.detener()
                return self.win and self.remaining_food == -1

            reloj.tick(10)
