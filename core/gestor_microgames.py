from microgames.microgame_hankujas import MicrojuegoExplotarBurbujas
from microgames.microgame_codigo import MicrojuegoEscribirCodigo
from microgames.microgame_diana import MicrojuegoDispararFlecha
from microgames.microgame_snake import SnakeGame


class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.minijuegos = [SnakeGame]  # Lista de clases de minijuegos
        self.indice = 0  # Lleva el progreso
        self.dificultad = 1

    def ejecutar_microjuego(self, time):
        """Ejecuta el minijuego actual y devuelve si ganó o perdió"""
        if self.indice >= len(self.minijuegos):
            return None  # No hay más minijuegos

        minijuego = self.minijuegos[self.indice](self.screen, time, self.dificultad)
        resultado = minijuego.ejecutar()
        self.indice += 1
        return resultado

    def isTerminado(self):
        return self.indice >= len(self.minijuegos)

    def subir_dificultad(self):
        self.dificultad += 1

    def siguiente_vuelta(self):
        self.indice = 0
        self.subir_dificultad()
