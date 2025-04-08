import pygame
import random
from microgames.microgame_base import MicrojuegoBase
from core.gestor_sprites import Sprite

class MicrojuegoDispararFlecha(MicrojuegoBase):
    def __init__(self, screen, tiempo, dificultad=1):
        super().__init__(screen, tiempo, dificultad)
        self.musica = "minijuego_flecha.mp3"  # Música del minijuego

        # Tamaños de la diana y la flecha
        self.tam_diana = 120
        self.tam_flecha_x = 40
        self.tam_flecha_y = 60

        # Crear sprites con los tamaños ajustables
        self.diana = Sprite("../assets/microgames/diana/Flecha.png", self.tam_diana, self.tam_diana)
        self.flecha = Sprite("../assets/microgames/diana/Diana.png", self.tam_flecha_x, self.tam_flecha_y)

        # Velocidades
        self.velocidad_diana = 5
        self.velocidad_flecha = 15
        self.flecha_en_movimiento = False
        self.juego_ganado = False  # Indica si el jugador ha ganado

        # Posicionar la diana en una posición aleatoria en la parte superior
        self.diana.actualizar_posicion(random.randint(50, screen.get_width() - self.tam_diana - 50), 50)

        # Posicionar la flecha en la parte inferior de la pantalla
        self.flecha.actualizar_posicion(screen.get_width() // 2, screen.get_height() - 100)

    def manejar_eventos(self, event):
        """Detecta si el jugador presionó espacio o hizo clic para disparar"""
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN):
            if not self.flecha_en_movimiento:  # Solo disparar si la flecha no está en movimiento
                self.flecha_en_movimiento = True

    def actualizar(self):
        """Mueve la diana y la flecha"""
        if self.juego_ganado:
            return  # No actualizar si el jugador ya ganó

        # Mover la diana de un lado a otro
        self.diana.rect.x += self.velocidad_diana
        if self.diana.rect.right >= self.screen.get_width() or self.diana.rect.left <= 0:
            self.velocidad_diana *= -1  # Cambiar dirección al chocar con los bordes

        # Mover la flecha si ha sido disparada
        if self.flecha_en_movimiento:
            self.flecha.rect.y -= self.velocidad_flecha

            # Verificar colisión con la diana
            if self.flecha.colisiona_con(self.diana):
                self.juego_ganado = True
                return True  # Minijuego ganado

            # Si la flecha sale de la pantalla, el jugador pierde
            if self.flecha.rect.bottom < 0:
                return False  # Minijuego perdido

    def dibujar(self):
        """Dibuja la diana y la flecha en pantalla"""
        self.screen.fill((255, 255, 255))  # Fondo blanco
        self.diana.dibujar(self.screen)
        self.flecha.dibujar(self.screen)

        # Mostrar mensaje de victoria si el jugador acierta
        if self.juego_ganado:
            font = pygame.font.Font(None, 60)
            texto = font.render("¡Has acertado!", True, (0, 255, 0))
            self.screen.blit(texto, (self.screen.get_width() // 3, self.screen.get_height() // 2))

        pygame.display.flip()
