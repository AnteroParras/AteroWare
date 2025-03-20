from microgames.microgame_hankujas import MicrojuegoExplotarBurbujas


class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.minijuegos = [MicrojuegoExplotarBurbujas]  # Lista de clases de minijuegos
        self.indice = 0  # Lleva el progreso

    def ejecutar_microjuego(self, time):
        """Ejecuta el minijuego actual y devuelve si ganó o perdió"""
        if self.indice >= len(self.minijuegos):
            return None  # No hay más minijuegos

        minijuego = self.minijuegos[self.indice](self.screen, time)
        resultado = minijuego.ejecutar()
        self.indice += 1
        return resultado
