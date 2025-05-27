import pygame
import random
from microgames.microgame_base import MicrojuegoBase
from core.gestor_sprites import Sprite
from core.config import Config

class MicrojuegoDispararFlecha(MicrojuegoBase):
    def __init__(self, screen, tiempo, dificultad=1):
        super().__init__(screen, tiempo, dificultad)
        self.musica = "Bananza.mp3"  # Música del minijuego

        # Tamaños de la diana y la flecha
        self.tam_diana = 120
        self.tam_flecha_x = 40
        self.tam_flecha_y = 60

        # Crear sprites con los tamaños ajustables
        self.diana = Sprite("../assets/microgames/diana/diana.png", self.tam_diana, self.tam_diana)
        self.flecha = Sprite("../assets/microgames/diana/bala.png", self.tam_flecha_x, self.tam_flecha_y)

        # Velocidades
        self.velocidad_diana = 5
        self.velocidad_flecha = 15
        self.flecha_en_movimiento = False
        self.juego_ganado = False  # Indica si el jugador ha ganado

        # Posicionar la diana en una posición aleatoria en la parte superior
        self.diana.actualizar_posicion(random.randint(50, screen.get_width() - self.tam_diana - 50), 50)

        # Posicionar la flecha en la parte inferior de la pantalla
        self.flecha.actualizar_posicion(screen.get_width() // 2, screen.get_height() - 100)

        # Fondo
        self.fondo = Sprite("../assets/microgames/diana/Bananzafondo.png", screen.get_width(), screen.get_height())

    def manejar_eventos(self, event):
        """Detecta si el jugador presionó espacio o hizo clic para disparar"""
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN):
            if not self.flecha_en_movimiento:  # Solo disparar si la flecha no está en movimiento
                self.flecha_en_movimiento = True

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
        self.fondo.dibujar(self.screen)  # Dibuja el fondo del escritorio
        self.diana.dibujar(self.screen)
        self.flecha.dibujar(self.screen)


    # Mostrar mensaje de victoria si el jugador acierta
        if self.juego_ganado:
            font = pygame.font.Font(None, 60)
            texto = font.render("¡Has acertado!", True, (0, 255, 0))
            self.screen.blit(texto, (self.screen.get_width() // 3, self.screen.get_height() // 2))

        pygame.display.flip()

    def ejecutar(self):
        """Ejecuta el bucle del minijuego y devuelve si ganó o perdió"""
        self.audio.reproducir(self.musica)
        if Config.mostrar_ayuda:
            self.mostrar_controles(self.screen, "\nDisparar: Espacio/Click Izquierdo")

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