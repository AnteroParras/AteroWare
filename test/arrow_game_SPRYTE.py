import pygame
import random
import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, nombre_imagen, ancho, alto):
        """
        Inicializa un sprite con una imagen escalada.
        :param nombre_imagen: Ruta de la imagen del sprite
        :param ancho: Ancho del sprite
        :param alto: Alto del sprite
        """
        super().__init__()
        self.image = pygame.image.load(nombre_imagen)
        self.image = pygame.transform.scale(self.image, (ancho, alto))
        self.rect = self.image.get_rect()

    def dibujar(self, pantalla):
        """
        Dibuja el sprite en la pantalla en su posición actual.
        :param pantalla: Superficie donde se dibuja el sprite
        """
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


# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dispara la Flecha")

# Cargar imágenes
fondo = pygame.Surface((ANCHO, ALTO))
fondo.fill((255, 255, 255))

# Crear los sprites
diana = Sprite("diana.png", 50, 50)
flecha = Sprite("flecha.png", 30, 10)

# Posición inicial
diana.actualizar_posicion(random.randint(100, 700), random.randint(100, 500))
flecha.actualizar_posicion(50, ALTO // 2)

# Variables de juego
velocidad_diana = 3
disparada = False
velocidad_flecha = 10

# Bucle principal
corriendo = True
while corriendo:
    pantalla.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                disparada = True

    # Mover la diana de izquierda a derecha
    diana.rect.x += velocidad_diana
    if diana.rect.right >= ANCHO or diana.rect.left <= 0:
        velocidad_diana *= -1

    # Mover la flecha al disparar
    if disparada:
        flecha.rect.x += velocidad_flecha
        if flecha.rect.right >= ANCHO:
            disparada = False
            flecha.actualizar_posicion(50, ALTO // 2)  # Reiniciar flecha

    # Comprobar colisión
    if flecha.colisiona_con(diana):
        print("¡Diana alcanzada!")
        diana.actualizar_posicion(random.randint(100, 700), random.randint(100, 500))
        disparada = False
        flecha.actualizar_posicion(50, ALTO // 2)

    # Dibujar sprites
    diana.dibujar(pantalla)
    flecha.dibujar(pantalla)

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()