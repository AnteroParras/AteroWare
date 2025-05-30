import pygame
import random
from src.layout import draw_frame
from microgames.microgame_base import MicrojuegoBase
from core.config import Config

# Super Rotation System (SRS)
JLSTZ_KICKS = {
    (0, 1): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    (1, 0): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    (1, 2): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    (2, 1): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    (2, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    (3, 2): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    (3, 0): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    (0, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]
}
I_KICKS = {
    (0, 1): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    (1, 0): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    (1, 2): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    (2, 1): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    (2, 3): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    (3, 2): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    (3, 0): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    (0, 3): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)]
}

FORMAS = {
    'I': [[[1, 1, 1, 1]], [[1], [1], [1], [1]]],
    'O': [[[1, 1], [1, 1]]],
    'T': [[[0, 1, 0], [1, 1, 1]], [[1, 0], [1, 1], [1, 0]], [[1, 1, 1], [0, 1, 0]], [[0, 1], [1, 1], [0, 1]]],
    'S': [[[0, 1, 1], [1, 1, 0]], [[1, 0], [1, 1], [0, 1]]],
    'Z': [[[1, 1, 0], [0, 1, 1]], [[0, 1], [1, 1], [1, 0]]],
    'L': [[[1, 0], [1, 0], [1, 1]], [[1, 1, 1], [1, 0, 0]], [[1, 1], [0, 1], [0, 1]], [[0, 0, 1], [1, 1, 1]]],
    'J': [[[0, 1], [0, 1], [1, 1]], [[1, 0, 0], [1, 1, 1]], [[1, 1], [1, 0], [1, 0]], [[1, 1, 1], [0, 0, 1]]]
}

COLORES = {
    'I': (0, 255, 255), 'O': (255, 255, 0), 'T': (128, 0, 128),
    'S': (0, 255, 0), 'Z': (255, 0, 0), 'L': (255, 165, 0), 'J': (0, 0, 255)
}

# Gravedad en frames basados en la nes
GRAVITY_FRAMES = [48, 43, 38, 33, 28, 23, 18, 13, 8, 6] + [5] * 91


class Tetris(MicrojuegoBase):
    """Clase que representa el minijuego Tetris"""
    def __init__(self, screen, tiempo, dificultad=1, infinity=False):
        super().__init__(screen, 999 if infinity else 12, dificultad)
        self.musica = "T1.mp3"
        self.infinity = infinity

        self.ancho_bloque = 30
        self.columnas = 10
        self.filas = 20
        self.margen_x = (screen.get_width() - self.columnas * self.ancho_bloque) // 2
        self.margen_y = (screen.get_height() - self.filas * self.ancho_bloque) // 2
        self.grid = [[0] * self.columnas for _ in range(self.filas)]
        self.bolsa = []

        self.ancho = screen.get_width()
        self.height = screen.get_height()

        self.siguiente = None
        self.actual = None
        self.pos = [0, 3]
        self.rot = 0
        self.last = pygame.time.get_ticks()

        self.level = 0
        self.lines = 0

        self.delay = GRAVITY_FRAMES[self.level] * (1000 / 60)
        self.fast = False
        self.lock_delay = 500
        self.lock_time = None

        self.guarda = None
        self.can_store = True
        self.score = 0

        self.last_rotate = False
        self._fill_bag()
        self._next()

    def _fill_bag(self):
        """Inicializa el minijuego Tetris"""
        lst = list(FORMAS.keys())
        random.shuffle(lst)
        self.bolsa += lst

    def _next(self):
        """Genera la siguiente pieza y la coloca en la posición inicial"""
        if not self.bolsa:
            self._fill_bag()
        if self.siguiente is None:
            self.siguiente = self.bolsa.pop(0)
        self.actual = self.siguiente
        self.siguiente = self.bolsa.pop(0)
        self.pos = [0, self.columnas // 2 - len(FORMAS[self.actual][0][0]) // 2]
        self.rot = 0
        self.can_store = True
        self.lock_time = None
        self.last_rotate = False

    def _can_place(self, shape, off, rot):
        """Verifica si se puede colocar la pieza en la posición y rotación dadas"""
        for i, row in enumerate(shape):
            for j, val in enumerate(row):
                if val:
                    x = self.pos[0] + i + off[0]
                    y = self.pos[1] + j + off[1]
                    if x < 0 or x >= self.filas or y < 0 or y >= self.columnas or self.grid[x][y]:
                        return False
        return True

    def _rotate(self, dir):
        """Rota la pieza en la dirección indicada, aplicando las reglas de SRS"""
        old = self.rot
        new = (self.rot + dir) % len(FORMAS[self.actual])
        kicks = I_KICKS if self.actual == 'I' else JLSTZ_KICKS
        for dx, dy in kicks[(old, new)]:
            if self._can_place(FORMAS[self.actual][new], (dx, dy), new):
                self.pos[0] += dx
                self.pos[1] += dy
                self.rot = new
                self.lock_time = None
                self.last_rotate = True
                break

    def manejar_eventos(self, event):
        """Maneja los eventos del teclado y actualiza la posición de la pieza"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self._can_place(FORMAS[self.actual][self.rot], (0, -1), self.rot):
            self.pos[1] -= 1
            self.lock_time = None
            self.last_rotate = False
        if keys[pygame.K_RIGHT] and self._can_place(FORMAS[self.actual][self.rot], (0, 1), self.rot):
            self.pos[1] += 1
            self.lock_time = None
            self.last_rotate = False
        self.fast = keys[pygame.K_DOWN]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self._rotate(1)
            elif event.key == pygame.K_z:
                self._rotate(-1)
            elif event.key == pygame.K_LSHIFT and self.can_store:
                self._store()
            elif event.key == pygame.K_SPACE:
                self._hard_drop()
            elif event.key == pygame.K_ESCAPE:
                accion = self.menu.mostrar_pausa(self.screen)
                if accion == "continue":
                    pass
                elif accion == "options":
                    self.menu.mostrar_opciones(self.screen)
                elif accion == "exit":
                    return "exit_to_menu"


    def _store(self):
        """Guarda la pieza actual en la reserva y coloca la siguiente pieza"""
        self.actual, self.guarda = self.guarda, self.actual
        if not self.actual:
            self._next()
        else:
            self.pos = [0, self.columnas // 2 - len(FORMAS[self.actual][0][0]) // 2]
            self.rot = 0
        self.can_store = False
        self.last_rotate = False

    def actualizar(self):
        """Actualiza la lógica del minijuego Tetris"""
        self.delay = GRAVITY_FRAMES[min(self.level, len(GRAVITY_FRAMES) - 1)] * (1000 / 60)
        now = pygame.time.get_ticks()
        spd = 50 if self.fast else self.delay
        if now - self.last > spd:
            self.last = now
            if self._can_place(FORMAS[self.actual][self.rot], (1, 0), self.rot):
                self.pos[0] += 1
            else:
                if self.fast:
                    self._lock()
                else:
                    if self.lock_time is None:
                        self.lock_time = now
                    elif now - self.lock_time > self.lock_delay:
                        self._lock()
        else:
            if self._can_place(FORMAS[self.actual][self.rot], (1, 0), self.rot):
                self.lock_time = None

    def _lock(self):
        """Fija la pieza actual en la cuadrícula y limpia líneas si es necesario"""
        # place piece
        for i, row in enumerate(FORMAS[self.actual][self.rot]):
            for j, val in enumerate(row):
                if val:
                    self.grid[self.pos[0] + i][self.pos[1] + j] = self.actual

        new = [r for r in self.grid if not all(r)]
        cnt = self.filas - len(new)
        for _ in range(cnt):
            new.insert(0, [0] * self.columnas)
        self.grid = new

        # Control de nivel y líneas
        self.lines += cnt

        if not self.infinity:
            if self.lines >= self.dificultad:
                self.win = True

        if cnt > 0:
            self.level = self.lines // 5
            if self.level == 8:
                self.audio.detener()
                self.musica = "T2.mp3"
                self.audio.reproducir(self.musica)

        self.score += 100 * cnt + (50 * cnt if cnt > 1 else 0)
        self._next()

    def _hard_drop(self):
        """Deja caer la pieza actual hasta el fondo de la cuadrícula"""
        while self._can_place(FORMAS[self.actual][self.rot], (1, 0), self.rot):
            self.pos[0] += 1
        self._lock()

    def _posicion_sombra(self):
        """Devuelve la posición más baja posible de la pieza actual (ghost piece)."""
        pos_ghost = list(self.pos)
        while self._can_place(FORMAS[self.actual][self.rot],
                              (pos_ghost[0] + 1 - self.pos[0], pos_ghost[1] - self.pos[1]), self.rot):
            pos_ghost[0] += 1
        return pos_ghost

    def dibujar(self):
        """Dibuja el minijuego Tetris en la pantalla"""
        super().dibujar()
        draw_frame(self.screen)
        pygame.draw.rect(
            self.screen, (255, 255, 255),
            (self.margen_x - 2, self.margen_y - 2,
             self.columnas * self.ancho_bloque + 4,
             self.filas * self.ancho_bloque + 4), 2
        )

        # Mostrar puntuación, líneas y nivel
        font = pygame.font.SysFont(None, 24)
        txt_score = font.render(f"Puntos: {self.score}", True, (255, 255, 255))
        txt_lines = font.render(f"Lineas: {self.lines}", True, (255, 255, 255))
        self.screen.blit(txt_score, (80, 280))
        self.screen.blit(txt_lines, (80, 310))

        if self.infinity:
            txt_level = font.render(f"Nivel: {self.level}", True, (255, 255, 255))
            self.screen.blit(txt_level, (80, 340))
        else:
            txt_objetivo = font.render(f"¡Haz {self.dificultad} lineas!", True, (255, 255, 255))
            self.screen.blit(txt_objetivo, (int(self.ancho // 2 * 0.89), 340))

        # Dibujar la cuadrícula y piezas
        for i in range(self.filas):
            for j in range(self.columnas):
                p = self.grid[i][j]
                if p:
                    pygame.draw.rect(
                        self.screen, COLORES[p],
                        (self.margen_x + j * self.ancho_bloque,
                         self.margen_y + i * self.ancho_bloque,
                         self.ancho_bloque, self.ancho_bloque)
                    )

        # Sombra de la pieza (ghost piece)
        pos_ghost = self._posicion_sombra()
        for i, row in enumerate(FORMAS[self.actual][self.rot]):
            for j, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen, (200, 200, 200, 100),  # Color gris claro
                        (self.margen_x + (pos_ghost[1] + j) * self.ancho_bloque,
                         self.margen_y + (pos_ghost[0] + i) * self.ancho_bloque,
                         self.ancho_bloque, self.ancho_bloque)
                    )
        
        # Pieza actual
        for i, row in enumerate(FORMAS[self.actual][self.rot]):
            for j, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen, COLORES[self.actual],
                        (self.margen_x + (self.pos[1] + j) * self.ancho_bloque,
                         self.margen_y + (self.pos[0] + i) * self.ancho_bloque,
                         self.ancho_bloque, self.ancho_bloque)
                    )

        # Pieza guardada
        if self.guarda:
            tx = pygame.font.SysFont(None, 24).render("Guardado", True, (255, 255, 255))
            self.screen.blit(tx, (40, 40))
            for i, row in enumerate(FORMAS[self.guarda][0]):
                for j, v in enumerate(row):
                    if v:
                        pygame.draw.rect(
                            self.screen, COLORES[self.guarda],
                            (40 + j * self.ancho_bloque,
                             60 + i * self.ancho_bloque,
                             self.ancho_bloque, self.ancho_bloque)
                        )

        # Siguiente pieza
        if self.siguiente:
            tx = pygame.font.SysFont(None, 24).render("Siguiente", True, (255, 255, 255))
            self.screen.blit(tx, (80, 150))
            for i, row in enumerate(FORMAS[self.siguiente][0]):
                for j, v in enumerate(row):
                    if v:
                        pygame.draw.rect(
                            self.screen, COLORES[self.siguiente],
                            (80 + j * self.ancho_bloque,
                             190 + i * self.ancho_bloque,
                             self.ancho_bloque, self.ancho_bloque)
                        )

    def ejecutar(self):
        """Ejecuta el bucle del minijuego y devuelve si ganó o perdió"""
        self.audio.reproducir(self.musica)
        if Config.mostrar_ayuda:
            self.mostrar_controles(self.screen, "\nRotar piezas FlechaArriba/Z\nFlechas - Mover pieza\nEspacio - Caída rápida de la pieza\nShift izquierdo - Guardar pieza actual")

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

            if not self.win:
                self.actualizar()

            self.dibujar()
            if self.win and not self.infinity:
                font = pygame.font.SysFont(None, 48)
                txt_score = font.render(f"YEEEEY", True, (255, 255, 255))
                self.screen.blit(txt_score, (int(self.ancho // 2 * 0.85), 280))
            pygame.display.flip()

            if (pygame.time.get_ticks() - inicio) / 1000 > self.tiempo_limite:
                self.audio.detener()
                return self.win

            reloj.tick(30)