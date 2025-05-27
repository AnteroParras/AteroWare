import pygame
from PIL import Image, ImageSequence
from core.utils import ruta_recurso


class Sprite(pygame.sprite.Sprite):
    def __init__(self, nombre_imagen, ancho, alto):
        """
        Inicializa un sprite con una imagen escalada.
        :param nombre_imagen: Ruta de la imagen del sprite
        :param ancho: Ancho del sprite
        :param alto: Alto del sprite
        """
        super().__init__()
        try:
            self.image = pygame.image.load(nombre_imagen)
            self.image = pygame.transform.scale(self.image, (ancho, alto))
            self.rect = self.image.get_rect()
        except pygame.error as e:
            print(f"Error al cargar la imagen: {e}")
            self.image = None
            self.rect = pygame.Rect(0, 0, ancho, alto)

    def dibujar(self, pantalla):
        """
        Dibuja el sprite en la pantalla en su posición actual.
        :param pantalla: Superficie donde se dibuja el sprite
        """
        if self.image:
            pantalla.blit(self.image, self.rect)

    def actualizar_posicion(self, x, y):
        """
        Actualiza la posición del rectángulo del sprite.
        :param x: Nueva posición en X
        :param y: Nueva posición en Y
        """
        self.rect.topleft = (x, y)

    def colisiona_con(self, otro_sprite):
        """
        Verifica si este sprite colisiona con otro sprite.
        :param otro_sprite: El otro objeto Sprite con el que se verificará la colisión.
        :return: True si hay colisión, False en caso contrario.
        """
        return self.rect.colliderect(otro_sprite.rect)


class GIFSprite(Sprite):
    def __init__(self, gif_path, ancho, alto):
        """
        Inicializa un sprite con una imagen escalada.
        :param gif_path: Ruta del gif
        :param ancho: Ancho del gif que queremos darle
        :param alto: Alto del gif que queremos darle
        """
        super().__init__(gif_path, ancho, alto)
        self.frames = []
        self.index = 0

        try:
            # Cargar el GIF y extraer fotogramas
            gif = Image.open(gif_path)
            for frame in ImageSequence.Iterator(gif):
                frame = frame.convert("RGBA")
                mode = frame.mode
                size = frame.size
                data = frame.tobytes()
                img = pygame.image.fromstring(data, size, mode)
                img = pygame.transform.scale(img, (ancho, alto))
                self.frames.append(img)

            if self.frames:
                # Establecer la primera imagen y el rectángulo
                self.image = self.frames[self.index]
                self.rect = self.image.get_rect()
            else:
                raise ValueError("El GIF no contiene fotogramas válidos.")
        except Exception as e:
            print(f"Error al cargar el GIF: {e}")
            self.image = None
            self.rect = pygame.Rect(0, 0, ancho, alto)

    def update(self):
        """
        Actualiza el fotograma del GIF

        Cuando llega al final se reinicia
        """
        if self.frames:
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]

    def dibujar(self, pantalla):
        """
        Dibuja el fotograma actual del GIF en la pantalla.
        :param pantalla: Superficie donde se dibuja el sprite
        """
        if self.image:
            pantalla.blit(self.image, self.rect)