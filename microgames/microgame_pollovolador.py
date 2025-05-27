import pygame
import random
from time import sleep
from microgames.microgame_base import MicrojuegoBase
from core.gestor_audio import Audio
from core.gestor_sprites import Sprite
from core.config import Config
from core.utils import ruta_recurso

class MicrojuegoFlappyBird(MicrojuegoBase):
    """Microjuego inspirado en Flappy Bird, donde el jugador controla un pájaro que debe evitar obstáculos."""
    def __init__(self, screen, time, dificultad, infinity=False):
        self.infinity = infinity

        super().__init__(screen, time, dificultad)
        self.audio = Audio()
        self.music_file = "PolloLoco.mp3"

        self.SCREEN_WIDTH = screen.get_width()
        self.SCREEN_HEIGHT = screen.get_height()
        self.BIRD_SIZE = 30
        self.PIPE_WIDTH = 120
        self.PIPE_GAP = 200
        self.dificultad = dificultad
        self.PIPE_SPEED = 3 + 2 * (self.dificultad)
        self.GRAVITY = 0.75
        self.FLAP_STRENGTH = -10

        if infinity:
            self.tuberias_para_ganar = float('inf')  # Juego infinito, no hay objetivo de tuberías
        else:
            if self.dificultad == 1:
                self.tuberias_para_ganar = 5
            elif self.dificultad == 2:
                self.tuberias_para_ganar = 8
            else:
                self.tuberias_para_ganar = 12

        self.bird_sprite = Sprite(ruta_recurso("assets/microgames/gato_enfadao.jpg"), self.BIRD_SIZE, self.BIRD_SIZE)
        self.pipe_sprite = Sprite(ruta_recurso("assets/microgames/pollovolador/entubados.png"), self.PIPE_WIDTH, self.SCREEN_HEIGHT)
        self.fondo = Sprite(ruta_recurso("assets/microgames/pollovolador/PolloFondo.png"), screen.get_width(), screen.get_height())


        # Cargar imágenes de victoria y derrota
        self.imagen_victoria = pygame.image.load(ruta_recurso("assets/microgames/pollovolador/angry_win.jpg")).convert_alpha()
        self.imagen_derrota = pygame.image.load(ruta_recurso("assets/microgames/pollovolador/angry_lose.jpg")).convert_alpha()
        self.imagen_victoria_rect = self.imagen_victoria.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.imagen_derrota_rect = self.imagen_derrota.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))

        self.bird_y = self.SCREEN_HEIGHT // 2
        self.bird_velocity = 0
        self.pipes = []
        self.score = 0
        self.running = True

        self._crear_tubo()

    def manejar_eventos(self, event):
        """Maneja los eventos del microjuego, como el salto del pájaro y la pausa."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                accion = self.menu.mostrar_pausa(self.screen)
                if accion == "continue":
                    pass
                elif accion == "options":
                    self.menu.mostrar_opciones(self.screen)
                elif accion == "exit":
                    return "exit_to_menu"
        return None

    def _crear_tubo(self):
        """Crea un nuevo tubo con una altura aleatoria dentro de los límites de la pantalla."""
        pipe_height = random.randint(100, self.SCREEN_HEIGHT - self.PIPE_GAP - 100)
        self.pipes.append({
            "x": self.SCREEN_WIDTH,
            "top": pipe_height,
            "bottom": pipe_height + self.PIPE_GAP,
            "cruzado": False  # Para saber si ya se contó el punto
        })

    def _mover_tubos(self):
        """Mueve los tubos hacia la izquierda y elimina los que ya no están en pantalla."""
        for pipe in self.pipes:
            pipe["x"] -= self.PIPE_SPEED
        self.pipes = [pipe for pipe in self.pipes if pipe["x"] + self.PIPE_WIDTH > 0]
        if len(self.pipes) == 0 or self.pipes[-1]["x"] < self.SCREEN_WIDTH - 300:
            self._crear_tubo()

    def _dibujar_tubos(self):
        """Dibuja los tubos en la pantalla."""
        for pipe in self.pipes:
            # Tubo superior
            self.pipe_sprite.image = pygame.transform.flip(self.pipe_sprite.image, False, True)
            self.pipe_sprite.actualizar_posicion(pipe["x"], pipe["top"] - self.SCREEN_HEIGHT)
            self.pipe_sprite.dibujar(self.screen)
            # Tubo inferior
            self.pipe_sprite.image = pygame.transform.flip(self.pipe_sprite.image, False, True)
            self.pipe_sprite.actualizar_posicion(pipe["x"], pipe["bottom"])
            self.pipe_sprite.dibujar(self.screen)

    def _verificar_colisiones(self):
        """Verifica si el pájaro ha colisionado con los tubos o los bordes de la pantalla."""
        bird_rect = pygame.Rect(self.SCREEN_WIDTH // 2, self.bird_y, self.BIRD_SIZE, self.BIRD_SIZE)
        if self.bird_y <= 0 or self.bird_y + self.BIRD_SIZE >= self.SCREEN_HEIGHT:
            return True
        for pipe in self.pipes:
            pipe_top_rect = pygame.Rect(pipe["x"], 0, self.PIPE_WIDTH, pipe["top"])
            pipe_bottom_rect = pygame.Rect(pipe["x"], pipe["bottom"], self.PIPE_WIDTH, self.SCREEN_HEIGHT)
            if bird_rect.colliderect(pipe_top_rect) or bird_rect.colliderect(pipe_bottom_rect):
                return True
        return False

    def _actualizar_puntaje(self):
        """Actualiza el puntaje del jugador al pasar por los tubos."""
        for pipe in self.pipes:
            # Si el pájaro pasa el centro del tubo y no se ha contado aún
            if not pipe["cruzado"] and pipe["x"] + self.PIPE_WIDTH < self.SCREEN_WIDTH // 2:
                self.score += 1
                pipe["cruzado"] = True

    def mostrar_derrota(self):
        """Muestra la pantalla de derrota con un mensaje y reproduce un sonido."""
        self.audio.detener()
        self.audio.reproducir("BooBoo.mp3")
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(self.imagen_derrota, self.imagen_derrota_rect)
        pygame.display.flip()
        sleep(4)

    def mostrar_victoria(self):
        """Muestra la pantalla de victoria con un mensaje y reproduce un sonido."""
        self.audio.detener()
        self.audio.reproducir("Fnaf.mp3")
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(self.imagen_victoria, self.imagen_victoria_rect)
        pygame.display.flip()
        sleep(4)

    def ejecutar(self):
        """Ejecuta el bucle del microjuego y devuelve si ganó o perdió."""
        self.audio.reproducir(archivo=self.music_file, loop=True)
        if Config.mostrar_ayuda:
            self.mostrar_controles(self.screen, "\nVolar: Espacio")

        clock = pygame.time.Clock()
        victoria = False

        while self.running:
            self.screen.fill((135, 206, 250))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                resultado = self.manejar_eventos(event)
                if resultado == "exit_to_menu":
                    self.audio.detener()
                    return "exit_to_menu"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.bird_velocity = self.FLAP_STRENGTH

            self.bird_velocity += self.GRAVITY
            self.bird_y += self.bird_velocity

            self.fondo.dibujar(self.screen)
            self._mover_tubos()
            self._dibujar_tubos()

            self.bird_sprite.actualizar_posicion(self.SCREEN_WIDTH // 2, self.bird_y)
            self.bird_sprite.dibujar(self.screen)

            if self._verificar_colisiones():
                self.running = False
                victoria = False

            self._actualizar_puntaje()

            font = pygame.font.Font(None, 36)
            if not self.infinity:
                score_text = font.render(f"Puntaje: {self.score}/{self.tuberias_para_ganar}", True, (0, 0, 0))
                self.screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(60)

            if self.score >= self.tuberias_para_ganar:
                self.running = False
                victoria = True

        self.audio.detener()
        if victoria:
            self.mostrar_victoria()
        else:
            self.mostrar_derrota()
        return victoria