import pygame
import sys
from PIL import Image

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
ventana = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reproducción de GIF")

# Función para cargar un GIF y extraer sus fotogramas
def cargar_gif(ruta):
    gif = Image.open(ruta)
    fotogramas = []
    try:
        while True:
            # Convertir cada fotograma a un formato que Pygame pueda usar
            fotograma = gif.copy()
            fotograma = fotograma.convert("RGBA")  # Convertir a RGBA
            fotogramas.append(pygame.image.fromstring(fotograma.tobytes(), fotograma.size, 'RGBA'))
            gif.seek(gif.tell() + 1)  # Ir al siguiente fotograma
    except EOFError:
        pass  # Fin del GIF
    return fotogramas

# Función para reproducir un GIF
def reproducir_gif(ruta_gif, fps=10):
    fotogramas = cargar_gif(ruta_gif)  # Cargar los fotogramas del GIF

    if not fotogramas:
        print("No se pudieron cargar fotogramas del GIF.")
        return

    reloj = pygame.time.Clock()
    indice_fotograma = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Limpiar la ventana
        ventana.fill((0, 0, 0))  # Color negro de fondo

        # Mostrar el fotograma actual
        ventana.blit(fotogramas[indice_fotograma], (0, 0))

        # Actualizar el índice del fotograma
        indice_fotograma = (indice_fotograma + 1) % len(fotogramas)

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlar la tasa de fotogramas
        reloj.tick(fps)  # Controlar la velocidad de reproducción

# Bucle principal
if __name__ == "__main__":
    # Llamar a la función para reproducir el GIF
    ruta_gif = "tu_gif.gif"  # Cambia esto por la ruta de tu archivo GIF
    reproducir_gif(ruta_gif, fps=10)
