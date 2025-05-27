import pygame
import re  # Para usar expresiones regulares

from microgames.microgame_base import MicrojuegoBase


class MicrojuegoEscribirCodigo(MicrojuegoBase):
    """Microjuego donde el jugador debe escribir código Python, revelando letras por cada tecla presionada."""
    def __init__(self, screen, tiempo, dificultad=1):
        super().__init__(screen, tiempo, dificultad)

        # Texto original de la función (el código)
        self.texto_original = '''def manejar_eventos(self, event):
    """Detecta las teclas presionadas por el jugador y revela una letra del texto por cada tecla presionada.""" 
    if event.type == pygame.KEYDOWN:
        # Solo avanza el texto si no ha sido completado
        if self.indice_actual < len(self.texto_original):
            letra_presionada = pygame.key.name(event.key)  # Obtenemos la tecla presionada

            # Revelamos una letra del texto por cada tecla presionada
            self.texto_mostrado = (self.texto_mostrado[:self.indice_actual] +
                                   self.texto_original[self.indice_actual] +
                                   self.texto_mostrado[self.indice_actual + 1:])
            self.indice_actual += 1  # Avanzamos al siguiente índice'''

        self.texto_mostrado = '''def manejar_eventos(self, event):
    """Detecta las teclas presionadas por el jugador y revela una letra del texto por cada tecla presionada.""" 
     if event.type == pygame.KEYDOWN:
      # Solo avanza el texto si no ha sido completado
       if self.indice_actual < len(self.texto_original):
        letra_presionada = pygame.key.name(event.key)  # Obtenemos la tecla presionada'''

        # Aquí es donde el jugador empezará a escribir
        self.indice_actual = len(self.texto_mostrado)  # Empezamos donde ya está el texto fijo
        self.teclas_correctas = []  # Lista para almacenar las teclas correctas presionadas

        self.contador = len(self.texto_mostrado)

        # Variables de desfase
        self.desfase_x = 180  # Desfase horizontal
        self.desfase_y = 280 # Desfase vertical

        # Palabras clave en Python
        self.palabras_clave = ['def', 'if', 'else', 'elif', 'return', 'for', 'while', 'in', 'try', 'except', 'finally']

    def cargar_sprites(self):
        """Carga los sprites específicos del minijuego (si es necesario, por ahora no hay sprites)."""
        pass

    def manejar_eventos(self, event):
        """Detecta las teclas presionadas por el jugador y revela una letra del texto por cada tecla presionada."""
        if event.type == pygame.KEYDOWN:
            if self.indice_actual < len(self.texto_original):
                letra_presionada = pygame.key.name(event.key)  # Obtenemos la tecla presionada

                # Revelamos 3 letras del texto por cada tecla presionada
                siguiente_indice = self.indice_actual + 5  # Avanzamos 3 posiciones
                self.contador = self.contador + 5
                print(f"{self.contador} > {len(self.texto_original)}")

                if siguiente_indice > len(self.texto_original):
                    siguiente_indice = len(self.texto_original)  # Aseguramos que no nos pasemos

                # Revelamos las letras
                self.texto_mostrado = (self.texto_mostrado[:self.indice_actual] +
                                       self.texto_original[self.indice_actual:siguiente_indice] +
                                       self.texto_mostrado[siguiente_indice:])
                self.indice_actual = siguiente_indice  # Avanzamos al siguiente índice

    def actualizar(self):
        """Actualizar estado del minijuego."""
        if self.contador >= len(self.texto_original):
            self.win = True  # El jugador ha completado el texto correctamente

    def dibujar(self):
        """Dibuja el texto formateado como código en pantalla."""
        # Cargar el fondo del escritorio de IntelliJ
        fondo = pygame.image.load("../assets/microgames/codigo/metafondo.png")  # Asegúrate de tener la imagen del fondo
        fondo = pygame.transform.scale(fondo, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(fondo, (0, 0))  # Coloca la imagen como fondo

        # Usamos una fuente monoespaciada como "Courier New" y ajustamos el tamaño
        screen_width, screen_height = self.screen.get_size()
        font_size = 10  # Ajustamos el tamaño de la fuente al tamaño de la pantalla
        font = pygame.font.SysFont("JetBrains Mono", font_size)

        # Colores para las palabras clave y comentarios
        color_comentario = (169, 169, 169)  # Gris para los comentarios

        # Colores para las palabras clave
        color_funcion = (61,144,237)
        color_palabra_clave = (206, 123, 71)  # Azul para las palabras clave
        color_self = (140, 83, 134)  # Verde para `self.`
        color_len = (135, 135, 197)  # Naranja para `len()`

        # Separamos el texto en líneas para simular el formato de código
        lineas = self.texto_mostrado.split("\n")

        # Dibuja cada línea de código con un pequeño espacio entre ellas
        y_offset = self.desfase_y  # Usamos el desfase vertical
        for i, linea in enumerate(lineas):
            # Mantener la indentación
            espacios_iniciales = len(linea) - len(linea.lstrip())  # Contar los espacios iniciales
            partes = re.split(r'(\bself\.[a-zA-Z0-9_]*\b|\blen\b|\b(?:' + '|'.join(self.palabras_clave) + r')\b|#.*)', linea)

            x_offset = self.desfase_x + (espacios_iniciales * 10)  # Ajustar el desfase según los espacios

            for parte in partes:
                if parte.strip():  # Asegurarse de que la parte no esté vacía
                    if parte.startswith("self."):
                        texto = font.render(parte, True, color_self)  # Colorear `self.`
                    elif parte == "len":
                        texto = font.render(parte, True, color_len)  # Colorear `len()`
                    elif parte.strip() in self.palabras_clave:
                        texto = font.render(parte, True, color_palabra_clave)  # Colorear palabras clave
                    elif parte.startswith("#"):
                        texto = font.render(parte, True, color_comentario)  # Colorear comentarios
                    else:
                        texto = font.render(parte, True, (255, 255, 255))  # Blanco para texto normal

                    # Dibujamos la parte en la pantalla
                    self.screen.blit(texto, (x_offset, y_offset))
                    x_offset += texto.get_width() + 2  # Desplazamos para la siguiente parte

            y_offset += font_size + 2  # Espacio entre las líneas de código

        if self.win:
            font = pygame.font.Font(None, 48)
            texto_ganaste = font.render("¡Ganaste!", True, (0, 255, 0))
            self.screen.blit(texto_ganaste, (self.screen.get_width() // 2 - texto_ganaste.get_width() // 2, 300))

        pygame.display.flip()

    def ejecutar(self):
        super().ejecutar()