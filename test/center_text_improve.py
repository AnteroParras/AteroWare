import pygame
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 1200, 675
ventana = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Texto Justificado y Centrado")

# Función para mostrar texto justificado y centrado
def show_text(texto, x, y, justificacion='MIDDLE'):
    fuente = pygame.font.Font(None, 36)  # Usar fuente predeterminada
    lineas = texto.split('\n')  # Dividir el texto en líneas
    altura_total = len(lineas) * fuente.get_height()  # Altura total del texto

    # Calcular la posición Y según la justificación
    if justificacion == 'TOP':
        y_pos = y  # Alineación superior
    elif justificacion == 'MIDDLE':
        y_pos = y - altura_total // 2  # Alineación media
    elif justificacion == 'BOTTOM':
        y_pos = y - altura_total  # Alineación inferior
    else:
        raise ValueError("La justificación debe ser 'TOP', 'MIDDLE' o 'BOTTOM'.")

    # Dibujar cada línea de texto
    for i, linea in enumerate(lineas):
        texto_renderizado = fuente.render(linea, True, (255, 255, 255))  # Texto en blanco
        x_pos = x - texto_renderizado.get_width() // 2  # Centrar horizontalmente
        ventana.blit(texto_renderizado, (x_pos, y_pos + i * fuente.get_height()))  # Dibujar la línea

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Limpiar la ventana
    ventana.fill((0, 0, 0))  # Color negro de fondo

    # Llamar a la función para mostrar el texto
    mostrar_texto("Hola, mundo!\nEsto es un texto\njustificado y centrado.", WIDTH // 2, HEIGHT // 2, 'MIDDLE')

    # Mostrar texto alineado en la parte superior
    mostrar_texto("Texto Alineado Arriba", WIDTH // 2, 100, 'TOP')

    # Mostrar texto alineado en la parte inferior
    mostrar_texto("Texto Alineado Abajo", WIDTH // 2, HEIGHT - 100, 'BOTTOM')

    # Actualizar la pantalla
    pygame.display.flip()
