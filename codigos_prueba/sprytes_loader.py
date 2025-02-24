import pygame

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Movimiento de Sprite en Pygame")


# Función para cargar imágenes y reescalarlas
def cargar_imagen(nombre, tamaño=None):
    imagen = pygame.image.load(nombre).convert_alpha()  # Cargar con transparencia
    if tamaño:
        imagen = pygame.transform.scale(imagen, tamaño)  # Redimensionar si es necesario
    return imagen


# Clase Sprite con Movimiento
class Bomba(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cargar_imagen("bomba.jpg")
        self.rect = self.image.get_rect()

    def update(self):



class Personaje(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = cargar_imagen("Sprytes/Bubble.png", (50, 50))  # Cargar imagen y escalarla
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_x = 2  # Velocidad en X
        self.vel_y = 2  # Velocidad en Y

    def update(self):
        """Actualizar la posición del sprite."""
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Hacer que rebote en los bordes
        if self.rect.right >= ANCHO or self.rect.left <= 0:
            self.vel_x = -self.vel_x  # Invertir dirección en X
        if self.rect.bottom >= ALTO or self.rect.top <= 0:
            self.vel_y = -self.vel_y  # Invertir dirección en Y


# Crear grupo de sprites
grupo_sprites = pygame.sprite.Group()
personaje = Personaje(100, 150)  # Crear personaje en coordenadas (100,150)
grupo_sprites.add(personaje)

# Bucle principal
reloj = pygame.time.Clock()  # Controlar FPS
ejecutando = True
while ejecutando:
    pantalla.fill((0, 0, 0))  # Fondo negro
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    personaje.update()

    pygame.display.flip()  # Actualizar pantalla
    reloj.tick(60)  # Limitar a 60 FPS

pygame.quit()
