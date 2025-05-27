import pygame

COLORS = {
    "WHITE": (255, 255, 255),
    "RED": (200, 0, 0),
    "BLACK": (0, 0, 0),
    "EXTERNAL_FRAME_COLOR": (208, 144, 248),
    "GRADIENT_FRAME_COLOR": (224, 187, 248)
}

WIDTH, HEIGHT = 800, 692


def init():
    """
    Inicializa la pantalla y fuente
    """
    pygame.display.set_caption("AteroWare")
    font = pygame.font.Font(None, 36)


def draw_frame(screen, correction_x=0, correction_y=0):
    """
    Dibuja el marco de los minijuegos
    """
    EXTERNAL_FRAME_THICKNESS = 30  # Grosor del marco
    GRADIENT_FRAME_THICKNESS = 10

    if correction_x != 0:
        EXTERNAL_FRAME_THICKNESS += correction_x/2

    if correction_y != 0:
        EXTERNAL_FRAME_THICKNESS += correction_y/2

    pygame.draw.rect(screen, COLORS["EXTERNAL_FRAME_COLOR"], (0, 0, WIDTH, EXTERNAL_FRAME_THICKNESS))
    pygame.draw.rect(screen, COLORS["GRADIENT_FRAME_COLOR"],
                     (0, EXTERNAL_FRAME_THICKNESS, WIDTH, GRADIENT_FRAME_THICKNESS))

    pygame.draw.rect(screen, COLORS["EXTERNAL_FRAME_COLOR"], (0, 0, EXTERNAL_FRAME_THICKNESS, WIDTH))
    pygame.draw.rect(screen, COLORS["GRADIENT_FRAME_COLOR"], (EXTERNAL_FRAME_THICKNESS, EXTERNAL_FRAME_THICKNESS,
                                                              GRADIENT_FRAME_THICKNESS,
                                                              HEIGHT))

    pygame.draw.rect(screen, COLORS["EXTERNAL_FRAME_COLOR"], (0, HEIGHT - EXTERNAL_FRAME_THICKNESS,
                                                              WIDTH, EXTERNAL_FRAME_THICKNESS))
    pygame.draw.rect(screen, COLORS["GRADIENT_FRAME_COLOR"], (EXTERNAL_FRAME_THICKNESS,
                                                              HEIGHT - EXTERNAL_FRAME_THICKNESS - GRADIENT_FRAME_THICKNESS,
                                                              WIDTH, GRADIENT_FRAME_THICKNESS))

    pygame.draw.rect(screen, COLORS["EXTERNAL_FRAME_COLOR"], (WIDTH - EXTERNAL_FRAME_THICKNESS, 0,
                                                              WIDTH, HEIGHT))
    pygame.draw.rect(screen, COLORS["GRADIENT_FRAME_COLOR"],
                     (WIDTH - GRADIENT_FRAME_THICKNESS - EXTERNAL_FRAME_THICKNESS,
                      GRADIENT_FRAME_THICKNESS + EXTERNAL_FRAME_THICKNESS,
                      GRADIENT_FRAME_THICKNESS,
                      HEIGHT - 2 * GRADIENT_FRAME_THICKNESS - 2 * EXTERNAL_FRAME_THICKNESS))


def fill_screen(screen, color):
    """
    Rellena la pantalla con un color especificado
    :param screen:
    :param color:
    :return:
    """
    screen.fill(COLORS[color])



def show_text(screen, texto, size=36, justificacion='MIDDLE', color=(0, 0, 0), edge=False):
    """
    Muestra un texto en pantalla

    :param texto: El texto que se quiere mostrar ( permite /n para salto de linea )
    :param size: El tamaño del texto a mostrar ( por defecto 36 )
    :param justificacion: TOP - MIDDLE - BOTTOM , indica la alineacion vertical ( por defento MIDDLE )
    :param color: El color del texto ( por defecto negro )
    :param edge: Atributo que aun esta en desarrollo, es un reborde al texto

    """
    x = WIDTH // 2
    y = HEIGHT // 2

    fuente = pygame.font.Font(None, size)  # Usar fuente predeterminada
    lineas = texto.split('\n')  # Dividir el texto en líneas
    altura_total = len(lineas) * fuente.get_height()  # Altura total del texto

    # Calcular la posición Y según la justificación
    if justificacion == 'TOP':
        y_pos = 0 + altura_total  # Alineación superior
    elif justificacion == 'MIDDLE':
        y_pos = y - altura_total // 2  # Alineación media
    elif justificacion == 'BOTTOM':
        y_pos = HEIGHT - altura_total  # Alineación inferior
    else:
        raise ValueError("La justificación debe ser 'TOP', 'MIDDLE' o 'BOTTOM'.")

    # Dibujar cada línea de texto
    for i, linea in enumerate(lineas):
        texto_renderizado = fuente.render(linea, True, color)  # Texto en blanco
        x_pos = x - texto_renderizado.get_width() // 2  # Centrar horizontalmente
        screen.blit(texto_renderizado, (x_pos, y_pos + i * fuente.get_height()))  # Dibujar la línea


def inner_time_safe_life(screen, time, LIVES, TOTAL_LIVES=3):
    """
    Pantalla entre microjuegos

    :param time: El tiempo que se muestra
    """
    total_lives = ""
    limit = time + 1
    for i in range(LIVES):
        total_lives += " [V] "

    for i in range(TOTAL_LIVES - LIVES):
        total_lives += " [X] "

    start_time = pygame.time.get_ticks()
    while True:
        screen.fill(COLORS["BLACK"])

        show_text(screen, total_lives, justificacion='TOP', color=(255, 255, 255))
        show_text(screen, 'Preparate para el siguiente micro-juego!!\n\n' + str(time), color=(255, 255, 255))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        time = int(limit - (pygame.time.get_ticks() - start_time) / 1000)

        if (pygame.time.get_ticks() - start_time) / 1000 > limit - 1:
            return
