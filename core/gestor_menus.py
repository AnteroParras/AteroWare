import pygame
from math import sin, radians
import sys

from core.gestor_audio import Audio
from core.gestor_sprites import GIFSprite
from core.config import Config  # Asegúrate de tener la clase Config como en la respuesta anterior
from core.utils import ruta_recurso


class Menu:
    def __init__(self, screen):
        self.screen = screen

    def dividir_texto(self, texto, fuente, ancho_maximo):
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

    def mostrar_opciones(self, screen):
        fondo_gif = GIFSprite(ruta_recurso(ruta_recurso("assets/menu/menu.gif")), screen.get_width(), screen.get_height())
        font = pygame.font.Font(None, 50)
        texto_opciones = "Opciones"
        lineas_texto = self.dividir_texto(texto_opciones, font, screen.get_width() - 40)

        # Botón ayuda ON/OFF
        ayuda_rect = pygame.Rect(screen.get_width() // 2 - 100, 250, 200, 60)

        # Botón atrás
        boton_atras = {"texto": "Atrás", "rect": None, "angulo": 0}
        boton_atras["superficie"] = font.render(boton_atras["texto"], True, (255, 255, 255))
        boton_atras["rect"] = boton_atras["superficie"].get_rect(
            center=(screen.get_width() // 2, screen.get_height() - 100))

        angulo_incremento = 1.5
        reloj = pygame.time.Clock()

        while True:
            fondo_gif.update()
            fondo_gif.dibujar(screen)

            # Título con animación
            y_offset = 100
            for linea in lineas_texto:
                superficie_texto = font.render(linea, True, (255, 255, 255))
                superficie_rotada = pygame.transform.rotate(superficie_texto,
                                                            sin(pygame.time.get_ticks() / 200) * 2)
                texto_rect = superficie_rotada.get_rect(center=(screen.get_width() // 2, y_offset))
                screen.blit(superficie_rotada, texto_rect)
                y_offset += 50

            # Botón ayuda ON/OFF
            color_ayuda = (0, 200, 0) if Config.mostrar_ayuda else (200, 0, 0)
            pygame.draw.rect(screen, color_ayuda, ayuda_rect, border_radius=15)
            texto_ayuda = "Ayuda: ON" if Config.mostrar_ayuda else "Ayuda: OFF"
            surf_ayuda = font.render(texto_ayuda, True, (255, 255, 255))
            screen.blit(surf_ayuda, surf_ayuda.get_rect(center=ayuda_rect.center))

            # Botón atrás con animación
            boton_atras["angulo"] += angulo_incremento
            boton_atras["angulo"] %= 360
            superficie_rotada = pygame.transform.rotate(boton_atras["superficie"],
                                                        sin(pygame.time.get_ticks() / 200) * 10)
            rect_rotado = superficie_rotada.get_rect(center=boton_atras["rect"].center)
            screen.blit(superficie_rotada, rect_rotado)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if ayuda_rect.collidepoint(event.pos):
                        Config.mostrar_ayuda = not Config.mostrar_ayuda
                    elif boton_atras["rect"].collidepoint(event.pos):
                        return

            reloj.tick(60)

    def mostrar_creditos(self, screen):
        fondo_gif = GIFSprite(ruta_recurso("assets/menu/menu.gif"), screen.get_width(), screen.get_height())
        font = pygame.font.Font(None, 50)
        font_nombre = pygame.font.Font(None, 44)
        texto_creditos = "Trabajo hecho por Antero y Alejandro UwU"
        lineas_texto = self.dividir_texto(texto_creditos, font, screen.get_width() - 40)

        img1 = pygame.image.load(ruta_recurso("assets/menu/pacoFiestas.jpg")).convert_alpha()
        img2 = pygame.image.load(ruta_recurso("assets/menu/jaime.jpg")).convert_alpha()
        img1 = pygame.transform.scale(img1, (280, 280))
        img2 = pygame.transform.scale(img2, (280, 280))

        x1 = screen.get_width() // 2 - 180
        x2 = screen.get_width() // 2 + 180
        y_img = 320

        boton_atras = {"texto": "Atrás", "rect": None, "angulo": 0}
        boton_atras["superficie"] = font.render(boton_atras["texto"], True, (255, 255, 255))
        boton_atras["rect"] = boton_atras["superficie"].get_rect(
            center=(screen.get_width() // 2, screen.get_height() - 100))

        angulo_incremento = 2
        reloj = pygame.time.Clock()

        while True:
            fondo_gif.update()
            fondo_gif.dibujar(screen)

            # Texto con bamboleo
            y_offset = 100
            for linea in lineas_texto:
                superficie_texto = font.render(linea, True, (255, 255, 255))
                superficie_rotada = pygame.transform.rotate(superficie_texto, sin(pygame.time.get_ticks() / 200) * 10)
                texto_rect = superficie_rotada.get_rect(center=(screen.get_width() // 2, y_offset))
                screen.blit(superficie_rotada, texto_rect)
                y_offset += 50

            t = pygame.time.get_ticks()
            offset1 = int(20 * sin(t / 400))
            offset2 = int(20 * sin(t / 400 + 2))

            # Reborde arcoíris animado
            for i, (x, offset) in enumerate([(x1, offset1), (x2, offset2)]):
                color = (
                    int(128 + 127 * sin(t / 300 + i)),
                    int(128 + 127 * sin(t / 300 + 2 + i)),
                    int(128 + 127 * sin(t / 300 + 4 + i))
                )
                rect = pygame.Rect(0, 0, 290, 290)
                rect.center = (x, y_img + offset)
                pygame.draw.rect(screen, color, rect, border_radius=30, width=8)

            screen.blit(img1, img1.get_rect(center=(x1, y_img + offset1)))
            screen.blit(img2, img2.get_rect(center=(x2, y_img + offset2)))

            # Nombres con color animado
            color1 = (
                int(128 + 127 * sin(t / 400)),
                int(128 + 127 * sin(t / 400 + 2)),
                int(128 + 127 * sin(t / 400 + 4))
            )
            color2 = (
                int(128 + 127 * sin(t / 400 + 1)),
                int(128 + 127 * sin(t / 400 + 3)),
                int(128 + 127 * sin(t / 400 + 5))
            )
            nombre1 = font_nombre.render("Antero", True, color1)
            nombre2 = font_nombre.render("Alejandro", True, color2)
            nombre1_rot = pygame.transform.rotate(nombre1, sin(t / 400) * 5)
            nombre2_rot = pygame.transform.rotate(nombre2, sin(t / 400 + 2) * 5)
            rect1 = nombre1_rot.get_rect(center=(x1, y_img + 160 + offset1))
            rect2 = nombre2_rot.get_rect(center=(x2, y_img + 160 + offset2))
            screen.blit(nombre1_rot, rect1)
            screen.blit(nombre2_rot, rect2)

            # Botón "Atrás" con animación
            boton_atras["angulo"] += angulo_incremento
            boton_atras["angulo"] %= 360
            superficie_rotada = pygame.transform.rotate(boton_atras["superficie"],
                                                        sin(pygame.time.get_ticks() / 200) * 10)
            rect_rotado = superficie_rotada.get_rect(center=boton_atras["rect"].center)
            screen.blit(superficie_rotada, rect_rotado)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if boton_atras["rect"].collidepoint(event.pos):
                        return

            reloj.tick(60)


    def mostrar_menu(self, screen):
        """Muestra el menú principal con animación de rotación en los botones y cambio de color en el título."""
        # Cargar GIF de fondo (Funciona, pero pilla el path de scr no se porqué)
        fondo_gif = GIFSprite(ruta_recurso("assets/menu/menu.gif"), screen.get_width(), screen.get_height())

        # Cargar fuente personalizada
        fuente_personalizada = ruta_recurso("assets/fuentes/SuperMario256.ttf")  # Ruta al archivo de fuente
        font_titulo = pygame.font.Font(fuente_personalizada, 100)  # Fuente para el título
        font_botones = pygame.font.Font(fuente_personalizada, 74)  # Fuente para los botones, por ahora no se usa

        # Configurar fuente y texto del título
        titulo_text = "AteroWare"

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
        boton_atras["rect"] = boton_atras["superficie"].get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2 + 100))

        font_botones = pygame.font.Font(None, 74)
        botones = [
            {"texto": "Jugar", "rect": None, "angulo": 0},
            {"texto": "Seleccionar juego", "rect": None, "angulo": 0},
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
            (screen.get_width() // 2, screen.get_height() // 2 + 250),
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
            # screen.blit(fondo, (0, 0))

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
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for boton in botones:
                        if boton["rect"].collidepoint(event.pos):
                            if boton["texto"] == "Jugar":
                                return True # Salir del menú y comenzar el juego
                            elif boton["texto"] == "Opciones":
                                self.mostrar_opciones(screen)
                            elif boton["texto"] == "Créditos":
                                self.mostrar_creditos(screen)
                            elif boton["texto"] == "Seleccionar juego":
                                self.mostrar_selector_microjuegos(screen)
                            elif boton["texto"] == "Salir":
                                pygame.quit()
                                sys.exit()
            reloj.tick(60)


    def mostrar_selector_microjuegos(self, screen):
            """
            Muestra un selector de microjuegos con pestañas y animación de bamboleo en los títulos.
            :param screen: pantalla donde se dibuja el menú
            """
            import pygame
            from math import sin
            from core.gestor_sprites import GIFSprite
            from core.gestor_audio import Audio

            # Import dinámico de clases de juego
            from microgames.macro_pong4D import Pong4D
            from microgames.microgame_diana import MicrojuegoDispararFlecha
            from microgames.microgame_hankujas import MicrojuegoExplotarBurbujas
            from microgames.microgame_snake import SnakeGame
            from microgames.microgame_tetris import Tetris
            from microgames.microgame_pollovolador import MicrojuegoFlappyBird

            # Definimos las tres pestañas y sus juegos
            categorias = [
                {"nombre": "Microjuegos", "lista": [
                    {"nombre": "Explota", "clase": MicrojuegoExplotarBurbujas,
                     "imagen": ruta_recurso("assets/thumbnails/good_title.png")},
                    {"nombre": "Flecha", "clase": MicrojuegoDispararFlecha,
                     "imagen": ruta_recurso("assets/thumbnails/arrow_title.png")},
                    {"nombre": "Snake", "clase": SnakeGame,
                     "imagen": ruta_recurso("assets/thumbnails/snake_title_2.png")},
                    {"nombre": "Tetris", "clase": Tetris,
                     "imagen": ruta_recurso("assets/thumbnails/tetris_title.jpg")},
                    {"nombre": "Pollovolador", "clase": MicrojuegoFlappyBird,
                     "imagen": ruta_recurso("assets/thumbnails/flappy_title.jpg")},
                ]},
                {"nombre": "Macrojuegos", "lista": [
                    {"nombre": "Pong4D", "clase": Pong4D, "imagen": ruta_recurso("assets/thumbnails/pong4d_title.jpg")},
                ]},
                {"nombre": "Juegos especiales", "lista": [
                    {"nombre": "Snake clasico", "clase": SnakeGame, "imagen": ruta_recurso("assets/thumbnails/snake_title_2.png")},
                    {"nombre": "Tetris clasico", "clase": Tetris, "imagen": ruta_recurso("assets/thumbnails/tetris_title.jpg")},
                    {"nombre": "Flappy Bird infinito", "clase": MicrojuegoFlappyBird, "imagen": ruta_recurso("assets/thumbnails/flappy_title.jpg")},
                ]},
            ]

            # Pre-carga de thumbnails y surfaces de texto
            font = pygame.font.Font(None, 36)
            for cat in categorias:
                for mj in cat["lista"]:
                    img = pygame.image.load(mj["imagen"]).convert_alpha()
                    mj["img"] = pygame.transform.scale(img, (150, 150))
                    mj["surf"] = font.render(mj["nombre"], True, (255, 255, 255))

            # Variables de UI
            tabs = [cat["nombre"] for cat in categorias]
            active_tab = 0
            tab_font = pygame.font.Font(None, 48)
            title_font = pygame.font.Font(None, 64)
            spacing = 20
            reloj = pygame.time.Clock()
            fondo_gif = GIFSprite(ruta_recurso("assets/menu/menu.gif"), screen.get_width(), screen.get_height())
            control_audio = Audio()

            while True:
                fondo_gif.update()
                fondo_gif.dibujar(screen)

                # Encabezado arcoíris
                t = pygame.time.get_ticks()
                rainbow_color = (
                    int(128 + 127 * sin(t / 200)),
                    int(128 + 127 * sin(t / 200 + 2)),
                    int(128 + 127 * sin(t / 200 + 4))
                )
                header = title_font.render("Selecciona un microjuego", True, rainbow_color)
                screen.blit(header, header.get_rect(center=(screen.get_width() // 2, 80)))

                # Dibujar pestañas
                x = spacing
                tab_rects = []
                for i, name in enumerate(tabs):
                    color = (255, 255, 255) if i == active_tab else (180, 180, 180)
                    surf = tab_font.render(name, True, color)
                    rect = surf.get_rect(topleft=(x, 140))
                    screen.blit(surf, rect)
                    tab_rects.append(rect)
                    x += rect.width + spacing

                # Dibujar grid de juegos de la pestaña activa
                juegos = categorias[active_tab]["lista"]
                cols, gap = 3, 40
                start_y = 200
                total_w = cols * 150 + (cols - 1) * gap
                offset_x = (screen.get_width() - total_w) // 2

                # Prepara factory individual para cada juego
                for idx, mj in enumerate(juegos):
                    mj["factory"] = mj["clase"]  # Por defecto

                    if categorias[active_tab]["nombre"] == "Juegos especiales":
                        if mj["nombre"] == "Snake clasico":
                            orig = mj["clase"]
                            mj["factory"] = lambda scr, tm, df, o=orig: o(scr, tm, df, infinity=True)
                        elif mj["nombre"] == "Tetris clasico":
                            orig = mj["clase"]
                            mj["factory"] = lambda scr, tm, df, o=orig: o(scr, tm, df, infinity=True)
                        elif mj["nombre"] == "Flappy Bird infinito":
                            orig = mj["clase"]
                            mj["factory"] = lambda scr, tm, df, o=orig: o(scr, tm, df, infinity=True)

                # Renderiza cada juego
                for idx, mj in enumerate(juegos):
                    row, col = divmod(idx, cols)
                    x = offset_x + col * (150 + gap)
                    y = start_y + row * (150 + 80)
                    img_rect = pygame.Rect(x, y, 150, 150)
                    pygame.draw.rect(screen, (30, 30, 30), img_rect.inflate(10, 10), border_radius=10)
                    if img_rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(screen, (255, 255, 255), img_rect.inflate(4, 4), 2, border_radius=10)
                    screen.blit(mj["img"], (x, y))

                    # Texto con bamboleo vertical
                    offset = int(5 * sin(pygame.time.get_ticks() / 300 + idx))
                    txt_rect = mj["surf"].get_rect(center=(x + 75, y + 170 + offset))
                    screen.blit(mj["surf"], txt_rect)
                    mj["rect"] = img_rect

                # Botón Atrás
                back_s = tab_font.render("Atrás", True, (255, 255, 255))
                back_r = back_s.get_rect(center=(screen.get_width() // 2, screen.get_height() - 30))
                screen.blit(back_s, back_r)

                pygame.display.flip()

                # Eventos
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                        # Cambio de pestaña
                        for i, r in enumerate(tab_rects):
                            if r.collidepoint(ev.pos):
                                active_tab = i
                        # Selección de juego
                        for mj in juegos:
                            if mj.get("rect") and mj["rect"].collidepoint(ev.pos):
                                control_audio.detener()
                                juego = mj["factory"](screen, 10, 1)
                                juego.ejecutar()
                                control_audio.reproducir(archivo="Menu.mp3", loop=True)
                        # Atrás
                        if back_r.collidepoint(ev.pos):
                            return

                reloj.tick(60)

    def mostrar_pausa(self, screen):
        """
        Menú de pausa con opciones:
         - Continuar: cierra este menú y devuelve el control al juego
         - Opciones: abre el sub‑menú de opciones
         - Salir: vuelve al menú principal
        """
        font_titulo = pygame.font.Font(None, 80)
        font_botones = pygame.font.Font(None, 50)

        opciones = [
            {"texto": "Continuar", "action": "continue"},
            {"texto": "Opciones",   "action": "options"},
            {"texto": "Salir",      "action": "exit"}
        ]
        # calcular rects centrados
        alto_total = len(opciones) * 60 + (len(opciones)-1)*20
        start_y = (screen.get_height() - alto_total)//2

        for i, opt in enumerate(opciones):
            surf = font_botones.render(opt["texto"], True, (255,255,255))
            rect = surf.get_rect(center=(screen.get_width()//2, start_y + i*80))
            opt["surf"], opt["rect"] = surf, rect

        clock = pygame.time.Clock()
        while True:
            # Dibujo semi‑transparente sobre el juego
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            screen.blit(overlay, (0,0))

            # Título “PAUSA”
            titulo_s = font_titulo.render("PAUSA", True, (255,255,255))
            titulo_r = titulo_s.get_rect(center=(screen.get_width()//2, start_y-80))
            screen.blit(titulo_s, titulo_r)

            # Dibujar botones
            for opt in opciones:
                screen.blit(opt["surf"], opt["rect"])

            pygame.display.flip()

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    # si aprieta ESC de nuevo, sale de pausa
                    return "continue"
                elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    for opt in opciones:
                        if opt["rect"].collidepoint(ev.pos):
                            return opt["action"]

            clock.tick(60)

