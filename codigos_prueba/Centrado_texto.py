import pygame

# Inicializar pygame
pygame.init()

# Obtener la resolución de la pantalla del usuario
#info = pygame.display.Info()
#SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h  # Ancho y alto de la pantalla

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 675

# Configurar ventana en pantalla completa
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Texto Centrado Dinámico")

# Colores
WHITE = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)

# Fuente
pygame.font.init()
font = pygame.font.Font(None, 80)  # Fuente predeterminada, tamaño 80

# Texto que queremos centrar
text_content = "¡Juego completa!"


def draw_text_centered(text, x, y):
    """Dibuja un texto centrado en (x, y) basado en el tamaño de la pantalla."""
    text_surface = font.render(text, True, TEXT_COLOR)  # Renderizar el texto
    text_rect = text_surface.get_rect(center=(x, y))  # Centrarlo en (x, y)
    screen.blit(text_surface, text_rect)  # Dibujar en la pantalla


# Bucle principal
running = True
while running:
    screen.fill(WHITE)  # Fondo blanco

    # Dibujar el texto SIEMPRE centrado
    draw_text_centered(text_content, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    pygame.display.flip()  # Actualizar pantalla

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
