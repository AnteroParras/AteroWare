import pygame
import random
from src.layout import draw_frame
from microgames.microgame_base import MicrojuegoBase



# Super Rotation System (SRS) wall kick data
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

class Tetris(MicrojuegoBase):
    def __init__(self, screen, tiempo, dificultad=1):
        super().__init__(screen, 120, dificultad)
        self.ancho_bloque = 30
        self.musica = "FinalBoss.mp3"
        self.columnas = 10
        self.filas = 20
        self.margen_x = (screen.get_width() - self.columnas * self.ancho_bloque) // 2
        self.margen_y = (screen.get_height() - self.filas * self.ancho_bloque) // 2
        self.grid = [[0] * self.columnas for _ in range(self.filas)]
        self.bolsa = []
        self.siguiente = None
        self.actual = None
        self.pos = [0, 3]
        self.rot = 0
        self.last = pygame.time.get_ticks()
        self.delay = 500
        self.fast = False
        self.lock_delay = 500
        self.lock_time = None
        self.guarda = None
        self.can_store = True
        self.score = 0
        self._fill_bag()
        self._next()

    def _fill_bag(self):
        lst = list(FORMAS.keys())
        random.shuffle(lst)
        self.bolsa += lst

    def _next(self):
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

    def _can_place(self, shape, off, rot):
        for i, row in enumerate(shape):
            for j, val in enumerate(row):
                if val:
                    x = self.pos[0] + i + off[0]
                    y = self.pos[1] + j + off[1]
                    if x < 0 or x >= self.filas or y < 0 or y >= self.columnas or self.grid[x][y]:
                        return False
        return True

    def _rotate(self, dir):
        old = self.rot
        new = (self.rot + dir) % len(FORMAS[self.actual])
        kicks = I_KICKS if self.actual == 'I' else JLSTZ_KICKS
        for dx, dy in kicks[(old, new)]:
            if self._can_place(FORMAS[self.actual][new], (dx, dy), new):
                self.pos[0] += dx
                self.pos[1] += dy
                self.rot = new
                self.lock_time = None
                break

    def manejar_eventos(self, event):
        # Movimiento continuo: izquierda, derecha y bajada rápida
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self._can_place(FORMAS[self.actual][self.rot], (0, -1), self.rot):
            self.pos[1] -= 1
            self.lock_time = None
        if keys[pygame.K_RIGHT] and self._can_place(FORMAS[self.actual][self.rot], (0, 1), self.rot):
            self.pos[1] += 1
            self.lock_time = None
        self.fast = keys[pygame.K_DOWN]

        # Procesar eventos puntuales
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Rotaciones y almacenar
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self._rotate(1)
            elif event.key == pygame.K_z:
                self._rotate(-1)
            elif event.key == pygame.K_LSHIFT and self.can_store:
                self._store()

            # Menú de pausa
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

        # Si no devolvimos "exit_to_menu", devolvemos None para seguir jugando
        return None

    def _store(self):
        self.actual, self.guarda = self.guarda, self.actual
        if not self.actual:
            self._next()
        else:
            self.pos = [0, self.columnas // 2 - len(FORMAS[self.actual][0][0]) // 2]
            self.rot = 0
        self.can_store = False

    def actualizar(self):
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
        for i, row in enumerate(FORMAS[self.actual][self.rot]):
            for j, val in enumerate(row):
                if val:
                    self.grid[self.pos[0] + i][self.pos[1] + j] = self.actual
        self._clear()
        self._next()

    def _clear(self):
        new = [r for r in self.grid if not all(r)]
        cnt = self.filas - len(new)
        for _ in range(cnt):
            new.insert(0, [0] * self.columnas)
        self.grid = new
        self.score += 100 * cnt
        self.win = cnt > 0

    def dibujar(self):
        super().dibujar()
        draw_frame()
        pygame.draw.rect(
            self.screen, (255, 255, 255),
            (self.margen_x - 2, self.margen_y - 2,
             self.columnas * self.ancho_bloque + 4,
             self.filas * self.ancho_bloque + 4), 2
        )
        txt = pygame.font.SysFont(None, 24).render(f"Puntos:{self.score}", True, (255, 255, 255))
        self.screen.blit(txt, (20, 280))
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
        shape = FORMAS[self.actual][self.rot]
        for i, row in enumerate(shape):
            for j, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen, COLORES[self.actual],
                        (self.margen_x + (self.pos[1] + j) * self.ancho_bloque,
                         self.margen_y + (self.pos[0] + i) * self.ancho_bloque,
                         self.ancho_bloque, self.ancho_bloque)
                    )
        if self.guarda:
            txt = pygame.font.SysFont(None, 24).render("Guardado", True, (255, 255, 255))
            self.screen.blit(txt, (20, 20))
            for i, row in enumerate(FORMAS[self.guarda][0]):
                for j, val in enumerate(row):
                    if val:
                        pygame.draw.rect(
                            self.screen, COLORES[self.guarda],
                            (20 + j * self.ancho_bloque,
                             40 + i * self.ancho_bloque,
                             self.ancho_bloque, self.ancho_bloque)
                        )
        if self.siguiente:
            txt = pygame.font.SysFont(None, 24).render("Siguiente", True, (255, 255, 255))
            self.screen.blit(txt, (20, 150))
            for i, row in enumerate(FORMAS[self.siguiente][0]):
                for j, val in enumerate(row):
                    if val:
                        pygame.draw.rect(
                            self.screen, COLORES[self.siguiente],
                            (20 + j * self.ancho_bloque,
                             170 + i * self.ancho_bloque,
                             self.ancho_bloque, self.ancho_bloque)
                        )