import pygame
from core.gestor_audio import Audio
from core.gestor_microgames import GameManager
import globals_config as gc
from layout import init, inner_time_safe_life, show_text, fill_screen, screen
from core.gestor_sprites import GIFSprite

import pygame
from math import sin, radians

import pygame
from math import sin, radians

def dividir_texto(texto, fuente, ancho_maximo):
    """
    Divide un texto en varias líneas para que se ajuste al ancho máximo especificado.
    :param texto: El texto a dividir.
    :param fuente: La fuente utilizada para renderizar el texto.
    :param ancho_maximo: El ancho máximo permitido para el texto.
    :return: Una lista de líneas de texto.
    """
    palabras = texto.split(" ")
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        if fuente.size(linea_actual + palabra)[0] <= ancho_maximo:
            linea_actual += palabra + " "
        else:
            lineas.append(linea_actual.strip())
            linea_actual = palabra + " "

    if linea_actual:
        lineas.append(linea_actual.strip())

    return lineas

def mostrar_opciones(screen):
    """Muestra la pantalla de opciones con animación de bamboleo en el texto y un botón para volver al menú principal."""
    fondo_gif = GIFSprite("Menu.gif", screen.get_width(), screen.get_height())
    font = pygame.font.Font(None, 50)
    texto_opciones = "Menú de opciones (por implementar, tened paciencia 👉👈)"
    lineas_texto = dividir_texto(texto_opciones, font, screen.get_width() - 40)

    boton_atras = {"texto": "Atrás", "rect": None, "angulo": 0}
    boton_atras["superficie"] = font.render(boton_atras["texto"], True, (255, 255, 255))
    boton_atras["rect"] = boton_atras["superficie"].get_rect(center=(screen.get_width() // 2, screen.get_height() - 100))

    angulo_incremento = 1.5  # Velocidad de rotación
    reloj = pygame.time.Clock()

    while True:
        fondo_gif.update()  # Actualizar el fotograma del GIF
        fondo_gif.dibujar(screen)  # Dibujar el GIF en la pantalla

        # Dibujar texto dividido en líneas con animación de bamboleo
        y_offset = 100
        for linea in lineas_texto:
            superficie_texto = font.render(linea, True, (255, 255, 255))
            superficie_rotada = pygame.transform.rotate(superficie_texto, sin(pygame.time.get_ticks() / 200) *2) # Cambia el ángulo de rotación, mas grande = mas angulo duh
            texto_rect = superficie_rotada.get_rect(center=(screen.get_width() // 2, y_offset))
            screen.blit(superficie_rotada, texto_rect)
            y_offset += 50

        # Dibujar botón "Atrás" con animación de bamboleo
        boton_atras["angulo"] += angulo_incremento
        boton_atras["angulo"] %= 360
        superficie_rotada = pygame.transform.rotate(boton_atras["superficie"], sin(pygame.time.get_ticks() / 200) * 10)
        rect_rotado = superficie_rotada.get_rect(center=boton_atras["rect"].center)
        screen.blit(superficie_rotada, rect_rotado)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_atras["rect"].collidepoint(event.pos):
                    return  # Volver al menú principal

        reloj.tick(60)

def mostrar_creditos(screen):
    """Muestra la pantalla de créditos con animación de bamboleo en el texto y un botón para volver al menú principal."""
    fondo_gif = GIFSprite("Menu.gif", screen.get_width(), screen.get_height())
    font = pygame.font.Font(None, 50)
    texto_creditos = "Trabajo hecho por Antero y Alejandro UwU"
    lineas_texto = dividir_texto(texto_creditos, font, screen.get_width() - 40)

    boton_atras = {"texto": "Atrás", "rect": None, "angulo": 0}
    boton_atras["superficie"] = font.render(boton_atras["texto"], True, (255, 255, 255))
    boton_atras["rect"] = boton_atras["superficie"].get_rect(center=(screen.get_width() // 2, screen.get_height() - 100))

    angulo_incremento = 2  # Velocidad de rotación
    reloj = pygame.time.Clock()

    while True:
        fondo_gif.update()  # Actualizar el fotograma del GIF
        fondo_gif.dibujar(screen)  # Dibujar el GIF en la pantalla

        # Dibujar texto dividido en líneas con animación de bamboleo
        y_offset = 100
        for linea in lineas_texto:
            superficie_texto = font.render(linea, True, (255, 255, 255))
            superficie_rotada = pygame.transform.rotate(superficie_texto, sin(pygame.time.get_ticks() / 200) * 10)
            texto_rect = superficie_rotada.get_rect(center=(screen.get_width() // 2, y_offset))
            screen.blit(superficie_rotada, texto_rect)
            y_offset += 50

        # Dibujar botón "Atrás" con animación de bamboleo
        boton_atras["angulo"] += angulo_incremento
        boton_atras["angulo"] %= 360
        superficie_rotada = pygame.transform.rotate(boton_atras["superficie"], sin(pygame.time.get_ticks() / 200) * 10)
        rect_rotado = superficie_rotada.get_rect(center=boton_atras["rect"].center)
        screen.blit(superficie_rotada, rect_rotado)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_atras["rect"].collidepoint(event.pos):
                    return  # Volver al menú principal

        reloj.tick(60)

def mostrar_menu(screen):
    """Muestra el menú principal con animación de rotación en los botones y cambio de color en el título."""
    # Cargar imagen de fondo
    #fondo = pygame.image.load("../assets/microgames/explotar_burbujas/bad.png")
    #fondo = pygame.transform.scale(fondo, (screen.get_width(), screen.get_height()))

    # Cargar GIF de fondo (Funciona, pero pilla el path de scr no se porqué)
    fondo_gif = GIFSprite("../assets/menu/menu.gif", screen.get_width(), screen.get_height())

    # Cargar fuente personalizada
    fuente_personalizada = "../assets/fuentes/SuperMario256.ttf"  # Ruta al archivo de fuente
    font_titulo = pygame.font.Font(fuente_personalizada, 100)  # Fuente para el título
    font_botones = pygame.font.Font(fuente_personalizada, 74)  # Fuente para los botones, por ahora no se usa

    # Configurar fuente y texto del título
    #font_titulo = pygame.font.Font(None, 100)
    titulo_text = "AteroWare"
    titulo_rect = None

    # Colores para el título
    colores = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    color_index = 0
    color_actual = colores[color_index]
    color_siguiente = colores[(color_index + 1) % len(colores)]
    interpolacion = 0

    # Configurar botones

    font = pygame.font.Font(None, 74)
    texto_opciones = font.render("Opciones", True, (255, 255, 255))
    texto_rect = texto_opciones.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))

    boton_atras = {"texto": "Atrás", "rect": None}
    boton_atras["superficie"] = font.render(boton_atras["texto"], True, (255, 255, 255))
    boton_atras["rect"] = boton_atras["superficie"].get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))

    font_botones = pygame.font.Font(None, 74)
    botones = [
        {"texto": "Jugar", "rect": None, "angulo": 0},
        {"texto": "Opciones", "rect": None, "angulo": 0},
        {"texto": "Créditos", "rect": None, "angulo": 0},
        {"texto": "Salir", "rect": None, "angulo": 0},
    ]

    # Posiciones iniciales de los botones
    posiciones = [
        (screen.get_width() // 2, screen.get_height() // 2 - 150),
        (screen.get_width() // 2, screen.get_height() // 2 - 50),
        (screen.get_width() // 2, screen.get_height() // 2 + 50),
        (screen.get_width() // 2, screen.get_height() // 2 + 150),
    ]

    # Crear superficies de texto para los botones
    for i, boton in enumerate(botones):
        texto = font_botones.render(boton["texto"], True, (255, 255, 255))
        boton["superficie"] = texto
        boton["rect"] = texto.get_rect(center=posiciones[i])

    # Variables para animación
    angulo_incremento = 1.5  # Velocidad de rotación
    reloj = pygame.time.Clock()

    # Implementación de la música de fondo
    control_audio = Audio()
    control_audio.reproducir(archivo="Menu.mp3", loop=True)

    while True:
        # Dibujar fondo (Este lo usamos cuando el fondo sea una imagen)
        #screen.blit(fondo, (0, 0))

        # Actualizar el GIF de fondo (da un error, no "encuentra" el gif. Actualizo, si lo encuentra pero donde no toca [Ver arriba])
        fondo_gif.update()  # Actualizar el fotograma del GIF
        fondo_gif.dibujar(screen)  # Dibujar el GIF en la pantalla

        # Interpolar colores
        interpolacion += 0.01
        if interpolacion >= 1:
            interpolacion = 0
            color_index = (color_index + 1) % len(colores)
            color_actual = colores[color_index]
            color_siguiente = colores[(color_index + 1) % len(colores)]

        # Calcular color interpolado
        color_interpolado = (
            int(color_actual[0] + (color_siguiente[0] - color_actual[0]) * interpolacion),
            int(color_actual[1] + (color_siguiente[1] - color_actual[1]) * interpolacion),
            int(color_actual[2] + (color_siguiente[2] - color_actual[2]) * interpolacion),
        )

        # Dibujar título
        titulo_superficie = font_titulo.render(titulo_text, True, color_interpolado)
        titulo_rect = titulo_superficie.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(titulo_superficie, titulo_rect)

        # Dibujar y animar botones
        for boton in botones:
            boton["angulo"] += angulo_incremento
            boton["angulo"] %= 360  # Mantener el ángulo entre 0 y 360
            superficie_rotada = pygame.transform.rotate(boton["superficie"], sin(radians(boton["angulo"])) * 10)
            rect_rotado = superficie_rotada.get_rect(center=boton["rect"].center)
            screen.blit(superficie_rotada, rect_rotado)

        pygame.display.flip()

        # Manejar eventos
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for boton in botones:
                    if boton["rect"].collidepoint(event.pos):
                        if boton["texto"] == "Jugar":
                            return  # Salir del menú y comenzar el juego
                        elif boton["texto"] == "Opciones":
                            mostrar_opciones(screen)
                        elif boton["texto"] == "Créditos":
                            mostrar_creditos(screen)
                        elif boton["texto"] == "Salir":
                            pygame.quit()
                            exit()
        reloj.tick(60)

# Inicialización de pygame y variables
pygame.init()
init()

# Mostrar el menú principal
mostrar_menu(screen)

# Bucle principal del juego
running = True
games_played = 0
control_audio = Audio()
control_juegos = GameManager(screen=screen)

while running and gc.LIVES > 0 and not control_juegos.isTerminado():
    control_audio.reproducir(archivo="Pirim.mp3")
    inner_time_safe_life(2)
    control_audio.detener()

    result = control_juegos.ejecutar_microjuego(7)  # Ejecuta el minijuego

    games_played += 1

    if not result:
        gc.LIVES -= 1  # Pierde una vida si falla

    if gc.LIVES <= 0 or control_juegos.isTerminado():
        running = False  # Si no quedan minijuegos o vidas pierdes

if gc.LIVES > 0:
    fill_screen("WHITE")
    show_text("Ole ole los caracoles")
    pygame.display.flip()
    mostrar_menu(screen)

else:
    fill_screen("RED")
    pygame.display.flip()

pygame.time.wait(2000)  # Espera 2 segundos antes de cerrar
pygame.quit()
