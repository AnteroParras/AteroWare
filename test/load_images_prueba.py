import pygame

# Inicializar pygame
pygame.init()

# Cargar el sprite sheet
sprite_sheet = pygame.image.load("Sprytes/Bubble.png")  # Asegúrate de que la imagen esté en la misma carpeta

# Dimensiones originales del frame (ajusta según el sprite sheet)
frame_width = 32
frame_height = 32
num_frames = 6  # Número total de frames

# Dimensiones escaladas
scaled_width = 200
scaled_height = 180

# Extraer y escalar los frames
frames = []
for i in range(num_frames):
    frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
    frame = pygame.transform.scale(frame, (scaled_width, scaled_height))  # Escalar a 300x300
    frames.append(frame)

# Configurar la ventana de Pygame
WIDTH, HEIGHT = 1200, 675  # Tamaño de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pantalla Llena de Sprites")

# Distribuir los sprites en una cuadrícula
cols = WIDTH // scaled_width  # Cuántos sprites caben en X
rows = HEIGHT // scaled_height  # Cuántos sprites caben en Y

# Llenar la pantalla con los sprites
running = True
while running:
    screen.fill((0, 0, 0))  # Fondo negro

    # Dibujar los sprites en la cuadrícula
    for row in range(rows):
        for col in range(cols):
            sprite = frames[(row * cols + col) % num_frames]  # Selecciona sprites en orden
            x = col * scaled_width
            y = row * scaled_height
            screen.blit(sprite, (x, y))

    pygame.display.flip()  # Actualizar pantalla

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()


