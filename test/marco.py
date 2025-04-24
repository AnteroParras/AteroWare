import pygame

# Inicializar pygame
pygame.init()

# Obtener la resolución de la pantalla del usuario
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h  # Ancho y alto de la pantalla
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 675



# Configurar ventana (comienza en pantalla completa)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juego con Pantalla Completa y Marco")

# Colores
WHITE = (255, 255, 255)
EXTERNAL_FRAME_COLOR = (208, 144, 248)
GRADIENT_FRAME_COLOR = (224, 187, 248)

EXTERNAL_FRAME_THICKNESS = 30  # Grosor del marco
GRADIENT_FRAME_THICKNESS = 10

# Estado del modo de pantalla
fullscreen = False

# Bucle principal
running = True
while running:
    screen.fill(WHITE)  # Fondo blanco

    pygame.draw.rect(screen, EXTERNAL_FRAME_COLOR, (0, 0, SCREEN_WIDTH,EXTERNAL_FRAME_THICKNESS))
    pygame.draw.rect(screen, GRADIENT_FRAME_COLOR, (0, EXTERNAL_FRAME_THICKNESS, SCREEN_WIDTH, GRADIENT_FRAME_THICKNESS))

    pygame.draw.rect(screen, EXTERNAL_FRAME_COLOR, (0, 0, EXTERNAL_FRAME_THICKNESS, SCREEN_WIDTH))
    pygame.draw.rect(screen, GRADIENT_FRAME_COLOR, (EXTERNAL_FRAME_THICKNESS,EXTERNAL_FRAME_THICKNESS,
                                                    GRADIENT_FRAME_THICKNESS,
                                                    SCREEN_HEIGHT))

    pygame.draw.rect(screen, EXTERNAL_FRAME_COLOR, (0, SCREEN_HEIGHT - EXTERNAL_FRAME_THICKNESS,
                                                    SCREEN_WIDTH, EXTERNAL_FRAME_THICKNESS))
    pygame.draw.rect(screen, GRADIENT_FRAME_COLOR, (EXTERNAL_FRAME_THICKNESS,
                                                    SCREEN_HEIGHT - EXTERNAL_FRAME_THICKNESS -GRADIENT_FRAME_THICKNESS,
                                                    SCREEN_WIDTH, GRADIENT_FRAME_THICKNESS))

    pygame.draw.rect(screen, EXTERNAL_FRAME_COLOR, (SCREEN_WIDTH - EXTERNAL_FRAME_THICKNESS, 0,
                                                    SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(screen, GRADIENT_FRAME_COLOR, (SCREEN_WIDTH - GRADIENT_FRAME_THICKNESS - EXTERNAL_FRAME_THICKNESS,
                                                    GRADIENT_FRAME_THICKNESS + EXTERNAL_FRAME_THICKNESS,
                                                    GRADIENT_FRAME_THICKNESS,
                                                    SCREEN_HEIGHT - 2*GRADIENT_FRAME_THICKNESS - 2*EXTERNAL_FRAME_THICKNESS))

    # Dibujar el marco
    pygame.display.flip()  # Actualizar pantalla

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:  # Cambiar entre pantalla completa y ventana
                fullscreen = not fullscreen
                if fullscreen:
                    SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                else:
                    SCREEN_WIDTH = 1200
                    SCREEN_HEIGHT = 675
                    screen = pygame.display.set_mode((1200, 675))  # Modo ventana con tamaño fijo

pygame.quit()
