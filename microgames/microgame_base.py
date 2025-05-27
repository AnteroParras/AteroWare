import pygame
from pygame import SurfaceType

from core.gestor_sprites import Sprite
from core.gestor_audio import Audio
from core.gestor_menus import Menu

class MicrojuegoBase:
    def __init__(self, screen , tiempo, dificultad=1):
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

    def mostrar_controles(self, screen, texto, tiempo=3):
        import pygame
        font = pygame.font.Font(None, 48)
        ancho_max = self.screen.get_width() - 100

        # Procesa saltos de línea explícitos
        lineas = []
        for linea_bruta in texto.split('\n'):
            palabras = linea_bruta.split(" ")
            linea = ""
            for palabra in palabras:
                test_linea = linea + palabra + " "
                if font.size(test_linea)[0] <= ancho_max:
                    linea = test_linea
                else:
                    lineas.append(linea.strip())
                    linea = palabra + " "
            if linea:
                lineas.append(linea.strip())
            # Si la línea era solo un salto, añade línea vacía
            if not linea_bruta.strip():
                lineas.append("")

        reloj = pygame.time.Clock()
        start = pygame.time.get_ticks()
        while (pygame.time.get_ticks() - start) < tiempo * 1000:
            self.screen.fill((30, 30, 60))
            rect = pygame.Rect(50, 100, self.screen.get_width() - 100, self.screen.get_height() - 200)
            pygame.draw.rect(self.screen, (50, 50, 120), rect, border_radius=30)
            pygame.draw.rect(self.screen, (200, 200, 255), rect, 4, border_radius=30)

            titulo = pygame.font.Font(None, 64).render("Controles", True, (255, 255, 255))
            self.screen.blit(titulo, titulo.get_rect(center=(self.screen.get_width() // 2, 150)))

            y = rect.top + 80
            for linea in lineas:
                surf = font.render(linea, True, (255, 255, 255))
                rect_texto = surf.get_rect(center=(self.screen.get_width() // 2, y))
                self.screen.blit(surf, rect_texto)
                y += 55

            msg = pygame.font.Font(None, 32).render("¡Prepárate!", True, (255, 255, 0))
            self.screen.blit(msg, msg.get_rect(center=(self.screen.get_width() // 2, rect.bottom - 40)))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            reloj.tick(60)