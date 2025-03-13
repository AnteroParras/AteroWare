import pygame
import random

from Sprites_loaders import *
import globals_config as gc
from layout import draw_frame, show_text, fill_screen, WIDTH, HEIGHT, screen

from globals_config import clock


def microgame_press_space():
    """ Microjueg: presiona espacio antes de que acabe el tiempo """
    start_time = pygame.time.get_ticks()

    while True:
        fill_screen("WHITE")
        draw_frame()

        show_text("Presiona ESPACIO rápido!!")
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Finaliza el juego

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True  # Gana el minijuego

        # Verifica si se acabó el tiempo
        if (pygame.time.get_ticks() - start_time) / 1000 > gc.MINIGAME_TIME:
            return False  # Pierde el minijuego

        clock.tick(30)

def microgame_press_space_in_time():
    """ Microjuego: Presionar espacio en un tiempo concreto """
    start_time = pygame.time.get_ticks()
    start = random.randrange((int(gc.MINIGAME_TIME * 200)), int((gc.MINIGAME_TIME * 500)))
    interval = random.randrange(int(gc.MINIGAME_TIME*180), int(gc.MINIGAME_TIME*200))

    failed = False
    win = False

    while True:
        fill_screen("WHITE")
        draw_frame()

        if win:
            show_text( "Que crack")
        elif failed:
            show_text("Cagaste")
        else:
            if pygame.time.get_ticks() - start_time < start:
                show_text("Espera...")
            elif start <= pygame.time.get_ticks() - start_time < start + interval:
                show_text("AHORA")

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if start <= pygame.time.get_ticks() - start_time < start + interval:
                    win = True
                else:
                    failed = True

        if pygame.time.get_ticks() - start_time >= start + interval and not win:
            failed = True

        # Verifica si se acabó el tiempo
        if (pygame.time.get_ticks() - start_time) / 1000 > gc.MINIGAME_TIME:
            return win

        clock.tick(30)

def microgame_explotar_burbujas():
    start_time = pygame.time.get_ticks()
    desfase = 40
    num_of_targets = 3
    clicked_targets = set()

    # Calcular tamaño de los rectángulos para llenar la pantalla
    num_x = (WIDTH - desfase * 2) // 8  # Ancho de cada burbuja
    num_y = (HEIGHT - desfase * 2) // 4  # Alto de cada burbuja
    radius = min(num_x, num_y) // 2  # Radio del círculo de detección

    # Definir posiciones de burbujas
    targets = []
    bubbles = pygame.sprite.Group()

    for row in range(4):
        for col in range(8):
            x = col * num_x + desfase
            y = row * num_y + desfase
            targets.append((x + num_x // 2, y + num_y // 2))  # Centro del rectángulo

    selected_targets = set(random.sample(range(len(targets)), num_of_targets))  # Índices de burbujas seleccionadas

    # Crear los sprites
    for i, (x, y) in enumerate(targets):
        if i in selected_targets:
            bubble = Sprite("../assets/microgames/explotar_burbujas/bad.png",num_x, num_y)
        else:
            bubble = Sprite("../assets/microgames/explotar_burbujas/good.png", num_x, num_y)

        bubble.actualizar_posicion(x - num_x // 2, y - num_y // 2)  # Centrar la imagen
        bubbles.add(bubble)

    # Bucle principal
    while True:
        fill_screen("WHITE")

        # Dibujar los sprites en la pantalla
        bubbles.draw(screen)

        draw_frame()
        show_text("¡Haz a Hank feliz!", justificacion='TOP')
        pygame.display.flip()

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Salir del minijuego

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos  # Obtener coordenadas del clic
                for i, (x, y) in enumerate(targets):
                    if i in selected_targets and (mx - x) ** 2 + (my - y) ** 2 <= radius ** 2:
                        clicked_targets.add(i)
                        selected_targets.remove(i)

                        # Cambiar la imagen de la burbuja explotada
                        for bubble in bubbles:
                            if bubble.rect.collidepoint(mx, my):
                                bubble.image = pygame.image.load("../assets/microgames/explotar_burbujas/good.png")
                                bubble.image = pygame.transform.scale(bubble.image, (num_x, num_y))

                if len(selected_targets) == 0:  # Si se explotan todas las burbujas seleccionadas
                    return True

        # Verificar si se acabó el tiempo
        if (pygame.time.get_ticks() - start_time) / 1000 > gc.MINIGAME_TIME:
            return False  # Perder el minijuego

        pygame.display.flip()
        clock.tick(30)

#TODO implementar los restantes
'''
def minigame_click():
    """ Minijuego: haz clic antes de que acabe el tiempo """
    instructions = "¡Haz CLIC rápido!"
    start_time = pygame.time.get_ticks()
    num_clicks = 10
    while True:
        screen.fill(WHITE)
        º()
        show_text("Cliquea " + str(num_clicks) + " veces!!")
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                num_clicks -= 1

        if not num_clicks:
            return True

        if (pygame.time.get_ticks() - start_time) / 1000 > MINIGAME_TIME:
            return False  # Pierde el minijuego

        clock.tick(30)


def wrap_bubble():
    start_time = pygame.time.get_ticks()
    desfase = 40
    num_of_targets = 3
    clicked_targets = set()

    # Calcular tamaño de los rectángulos para llenar la pantalla
    num_x = (WIDTH - desfase * 2) // 8  # Ancho de cada rectángulo
    num_y = (HEIGHT - desfase * 2) // 4  # Alto de cada rectángulo
    radius = min(num_x, num_y) // 2  # Radio del círculo dentro del rectángulo

    # Definir targets (centros de los rectángulos)
    targets = []
    for row in range(4):
        for col in range(8):
            x = col * num_x + desfase
            y = row * num_y + desfase
            targets.append((x + num_x // 2, y + num_y // 2))  # Centro del rectángulo

    selected_targets = set(random.sample(range(len(targets)), num_of_targets))  # Índices de los targets seleccionados

    # Bucle principal
    while True:
        screen.fill(WHITE)
        # Dibujar los rectángulos
        cont = 0

        for row in range(4):
            for col in range(8):
                if cont in selected_targets:
                    color = (255, 165, 100)
                else:
                    color = (173, 216, 230)

                x = col * num_x + desfase
                y = row * num_y + desfase
                pygame.draw.rect(screen, color, (x, y, num_x, num_y))
                cont += 1
        draw_frame()
        show_text("¡Explota las burbujas!", justificacion='TOP')
        pygame.display.flip()
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Salir del minijuego

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos  # Obtener coordenadas del clic
                for i, (x, y) in enumerate(targets):
                    if (mx - x) ** 2 + (my - y) ** 2 <= radius ** 2:
                        clicked_targets.add(i)  # Marcar clickeado
                        selected_targets.remove(i)

                if len(selected_targets) == 0:  # Si se clickean todos
                    return True

        # Verificar si se acabó el tiempo
        if (pygame.time.get_ticks() - start_time) / 1000 > MINIGAME_TIME:
            return False  # Perder el minijuego

        pygame.display.flip()
        clock.tick(30)


def dartboard():
    global LEVEL
    start_time = pygame.time.get_ticks()
    speed = 0.5 * LEVEL  # Medido en pixeles/tick
    pos_dartboard = (WIDTH // 2, HEIGHT * 0.15)
    radius = min(WIDTH, HEIGHT) // 15
    pos_arrow = (WIDTH // 2, HEIGHT - EXTERNAL_FRAME_THICKNESS - GRADIENT_FRAME_THICKNESS - radius - 20)
    disparo = False
    direccion = False

    while True:
        screen.fill(WHITE)
        pygame.draw.circle(screen, RED, pos_dartboard, radius)
        pygame.draw.circle(screen, (0,0,255), pos_arrow, radius)
        draw_frame()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Finaliza el juego

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                disparo = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q and DEBUG_MODE:
                pos_arrow = (WIDTH // 2, HEIGHT * 0.9)

            #DEBUG SETTINGS
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w and DEBUG_MODE:
                LEVEL += 1
                speed = 0.5 + LEVEL
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s and DEBUG_MODE:
                LEVEL -= 1
                speed = 0.5 * LEVEL
        if disparo:
            pos_arrow = pos_arrow[0], pos_arrow[1] - 0.5

        if pos_arrow[1] == pos_dartboard[1] and pos_dartboard[0]-radius < pos_arrow[0] < pos_dartboard[0] + radius:
            return True

        if direccion:
            if pos_dartboard[0] + speed < WIDTH - radius - EXTERNAL_FRAME_THICKNESS - GRADIENT_FRAME_THICKNESS:
                pos_dartboard = (pos_dartboard[0] + speed, pos_dartboard[1])
            else:
                direccion = False
                pos_dartboard = (pos_dartboard[0] - speed, pos_dartboard[1])
        else:
            if pos_dartboard[0] - speed > radius + EXTERNAL_FRAME_THICKNESS + GRADIENT_FRAME_THICKNESS:
                pos_dartboard = (pos_dartboard[0] - speed, pos_dartboard[1])
            else:
                direccion = True
                pos_dartboard = (pos_dartboard[0] + speed, pos_dartboard[1])

        if (pygame.time.get_ticks() - start_time) / 1000 > MINIGAME_TIME:
            return False


def minigame_click_targets():
    """Minijuego: Clickea en los 4 círculos rojos antes de que acabe el tiempo"""
    start_time = pygame.time.get_ticks()
    num_of_targets = 4

    # Definir las posiciones de los círculos en función del tamaño de la pantalla
    radius = min(WIDTH, HEIGHT) // 15  # Radio proporcional al tamaño de la pantalla
    targets = [
        (WIDTH // 4, HEIGHT // 4),
        (3 * WIDTH // 4, HEIGHT // 4),
        (WIDTH // 2, HEIGHT // 2),
        (WIDTH // 4, 3 * HEIGHT // 4)
    ]
    clicked_targets = set()  # Para rastrear los círculos clickeados

    while True:
        screen.fill(WHITE)
        draw_frame()
        # Dibujar solo los círculos que aún no han sido clickeados
        for i, pos in enumerate(targets):
            if i not in clicked_targets:
                pygame.draw.circle(screen, RED, pos, radius)

        show_text("Clickea en los " + str(num_of_targets) + " circulos!!", justificacion='TOP')

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Finaliza el juego

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos  # Obtener coordenadas del clic
                for i, (x, y) in enumerate(targets):
                    # Verificar si el clic está dentro del círculo usando la distancia euclidiana
                    if (mx - x) ** 2 + (my - y) ** 2 <= radius ** 2:
                        num_of_targets -= 1
                        clicked_targets.add(i)  # Marcar círculo como clickeado

        # Si se han clickeado los 4 círculos, gana el minijuego
        if len(clicked_targets) == len(targets):
            return True

        # Verificar si se acabó el tiempo
        if (pygame.time.get_ticks() - start_time) / 1000 > MINIGAME_TIME:
            return False  # Pierde el minijuego

        clock.tick(30)


def movement(targets):
    for i in range(len(targets)):
        targets[i] = targets[i][0] + random.randint(0, 60), targets[i][1] + random.randint(0, 120)


def movile_targets():
    start_time = pygame.time.get_ticks()
    num_of_targets = 4

    # Definir las posiciones de los círculos en función del tamaño de la pantalla
    radius = min(WIDTH, HEIGHT) // 15  # Radio proporcional al tamaño de la pantalla
    targets = [
        (0, 0), (60, 12), (120, 50), (32, 270)
    ]
    clicked_targets = set()  # Para rastrear los círculos clickeados

    while True:
        screen.fill(WHITE)
        draw_frame()
        # Dibujar solo los círculos que aún no han sido clickeados
        for i, pos in enumerate(targets):
            if i not in clicked_targets:
                pygame.draw.circle(screen, RED, pos, radius)

        show_text("Clickea en los " + str(num_of_targets) + " circulos!!", justificacion='TOP')

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Finaliza el juego

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos  # Obtener coordenadas del clic
                for i, (x, y) in enumerate(targets):
                    # Verificar si el clic está dentro del círculo usando la distancia euclidiana
                    if (mx - x) ** 2 + (my - y) ** 2 <= radius ** 2:
                        num_of_targets -= 1
                        clicked_targets.add(i)  # Marcar círculo como clickeado

        for i in range(len(targets)):
            targets[i] = targets[i][0] + random.randint(0, 60), targets[i][1] + random.randint(0, 120)

        # Si se han clickeado los 4 círculos, gana el minijuego
        if len(clicked_targets) == len(targets):
            return True

        # Verificar si se acabó el tiempo
        if (pygame.time.get_ticks() - start_time) / 1000 > MINIGAME_TIME:
            return False  # Pierde el minijuego

        clock.tick(30)


def inner_time_safe_life(time):
    total_lives = ""
    limit = time + 1
    for i in range(LIVES):
        total_lives += " [V] "

    for i in range(TOTAL_LIVES - LIVES):
        total_lives += " [X] "

    start_time = pygame.time.get_ticks()
    while True:
        screen.fill(BLACK)

        show_text(total_lives, justificacion='TOP', color=(255, 255, 255))
        show_text('Preparate para el siguiente micro-juego!!\n\n' + str(time), color=(255, 255, 255))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        time = int(limit - (pygame.time.get_ticks() - start_time) / 1000)

        if (pygame.time.get_ticks() - start_time) / 1000 > limit-1:
            return

º'''

def all_microgames_list():
    """
    Devuele una lista con todas las funciones del archivo que empiecen por microgame
    :return: list[funciones]
    """
    return [func for name, func in globals().items() if callable(func) and name.startswith("microgame")]

