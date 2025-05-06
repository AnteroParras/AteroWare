import pygame
from math import sin, radians

from core.gestor_audio import Audio
from core.gestor_sprites import GIFSprite



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
        """Muestra la pantalla de opciones con animación de bamboleo en el texto y un botón para volver al menú principal."""
        fondo_gif = GIFSprite("Menu.gif", screen.get_width(), screen.get_height())
        font = pygame.font.Font(None, 50)
        texto_opciones = "Menú de opciones (por implementar, tened paciencia 👉👈)"
        lineas_texto = self.dividir_texto(texto_opciones, font, screen.get_width() - 40)

        boton_atras = {"texto": "Atrás", "rect": None, "angulo": 0}
        boton_atras["superficie"] = font.render(boton_atras["texto"], True, (255, 255, 255))
        boton_atras["rect"] = boton_atras["superficie"].get_rect(
            center=(screen.get_width() // 2, screen.get_height() - 100))

        angulo_incremento = 1.5  # Velocidad de rotación
        reloj = pygame.time.Clock()

        while True:
            fondo_gif.update()  # Actualizar el fotograma del GIF
            fondo_gif.dibujar(screen)  # Dibujar el GIF en la pantalla

            # Dibujar texto dividido en líneas con animación de bamboleo
            y_offset = 100
            for linea in lineas_texto:
                superficie_texto = font.render(linea, True, (255, 255, 255))
                superficie_rotada = pygame.transform.rotate(superficie_texto,
                                                            sin(pygame.time.get_ticks() / 200) * 2)  # Cambia el ángulo de rotación, mas grande = mas angulo duh
                texto_rect = superficie_rotada.get_rect(center=(screen.get_width() // 2, y_offset))
                screen.blit(superficie_rotada, texto_rect)
                y_offset += 50

            # Dibujar botón "Atrás" con animación de bamboleo
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
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if boton_atras["rect"].collidepoint(event.pos):
                        return  # Volver al menú principal

            reloj.tick(60)

    def mostrar_creditos(self, screen):
        """Muestra la pantalla de créditos con animación de bamboleo en el texto y un botón para volver al menú principal."""
        fondo_gif = GIFSprite("Menu.gif", screen.get_width(), screen.get_height())
        font = pygame.font.Font(None, 50)
        texto_creditos = "Trabajo hecho por Antero y Alejandro UwU"
        lineas_texto = self.dividir_texto(texto_creditos, font, screen.get_width() - 40)

        boton_atras = {"texto": "Atrás", "rect": None, "angulo": 0}
        boton_atras["superficie"] = font.render(boton_atras["texto"], True, (255, 255, 255))
        boton_atras["rect"] = boton_atras["superficie"].get_rect(
            center=(screen.get_width() // 2, screen.get_height() - 100))

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
            superficie_rotada = pygame.transform.rotate(boton_atras["superficie"],
                                                        sin(pygame.time.get_ticks() / 200) * 10)
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

    def mostrar_menu(self, screen):
        """Muestra el menú principal con animación de rotación en los botones y cambio de color en el título."""
        # Cargar imagen de fondo
        # fondo = pygame.image.load("../assets/microgames/explotar_burbujas/bad.png")
        # fondo = pygame.transform.scale(fondo, (screen.get_width(), screen.get_height()))

        # Cargar GIF de fondo (Funciona, pero pilla el path de scr no se porqué)
        fondo_gif = GIFSprite("../assets/menu/menu.gif", screen.get_width(), screen.get_height())

        # Cargar fuente personalizada
        fuente_personalizada = "../assets/fuentes/SuperMario256.ttf"  # Ruta al archivo de fuente
        font_titulo = pygame.font.Font(fuente_personalizada, 100)  # Fuente para el título
        font_botones = pygame.font.Font(fuente_personalizada, 74)  # Fuente para los botones, por ahora no se usa

        # Configurar fuente y texto del título
        # font_titulo = pygame.font.Font(None, 100)
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
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for boton in botones:
                        if boton["rect"].collidepoint(event.pos):
                            if boton["texto"] == "Jugar":
                                return  # Salir del menú y comenzar el juego
                            elif boton["texto"] == "Opciones":
                                self.mostrar_opciones(screen)
                            elif boton["texto"] == "Créditos":
                                self.mostrar_creditos(screen)
                            elif boton["texto"] == "Seleccionar juego":
                                self.mostrar_selector_microjuegos(screen)
                            elif boton["texto"] == "Salir":
                                pygame.quit()
                                exit()
            reloj.tick(60)

    def mostrar_selector_microjuegos(self, screen):
        font = pygame.font.Font(None, 36)
        from microgames.macro_pong4D import Pong4D
        from microgames.microgame_codigo import MicrojuegoEscribirCodigo
        from microgames.microgame_diana import MicrojuegoDispararFlecha
        from microgames.microgame_hankujas import MicrojuegoExplotarBurbujas
        from microgames.microgame_snake import SnakeGame
        from microgames.tetris import Tetris
        microjuegos = [
            {"nombre": "Tetris", "imagen": "../assets/thumbnails/tetris_title.jpg", "clase": Tetris},
            {"nombre": "Snake", "imagen": "../assets/thumbnails/snake_title_2.png", "clase": SnakeGame},
            {"nombre": "Flecha", "imagen": "../assets/thumbnails/arrow_title.png", "clase": MicrojuegoDispararFlecha},
            {"nombre": "Explota", "imagen": "../assets/thumbnails/good_title.png", "clase": MicrojuegoExplotarBurbujas},
            {"nombre": "Código", "imagen": "../assets/thumbnails/hacking_title.jpg", "clase": MicrojuegoEscribirCodigo},
            {"nombre": "Pong4D", "imagen": "../assets/thumbnails/pong4d_title.jpg", "clase": Pong4D},
        ]

        for mj in microjuegos:
            mj["img"] = pygame.image.load(mj["imagen"]).convert_alpha()
            mj["img"] = pygame.transform.scale(mj["img"], (150, 150))
            mj["texto_surf"] = font.render(mj["nombre"], True, (255, 255, 255))

        columnas = 3
        margen_vertical = 180
        espacio = 40
        ancho_total = columnas * 150 + (columnas - 1) * espacio
        offset_x = (screen.get_width() - ancho_total) // 2

        reloj = pygame.time.Clock()
        font_titulo = pygame.font.Font("../assets/fuentes/SuperMario256.ttf", 32)
        titulo = "Selecciona un microjuego"

        fondo_gif = GIFSprite("../assets/menu/menu.gif", screen.get_width(), screen.get_height())

        control_audio = Audio()  # Asegúrate de crear la instancia aquí también

        while True:
            fondo_gif.update()
            fondo_gif.dibujar(screen)

            # Título animado
            color_animado = (
                128 + int(127 * sin(pygame.time.get_ticks() / 400)),
                128 + int(127 * sin(pygame.time.get_ticks() / 500)),
                255
            )
            titulo_surf = font_titulo.render(titulo, True, color_animado)
            titulo_rect = titulo_surf.get_rect(center=(screen.get_width() // 2, 60))
            screen.blit(titulo_surf, titulo_rect)

            mouse_pos = pygame.mouse.get_pos()

            # Dibujar microjuegos
            for i, mj in enumerate(microjuegos):
                fila = i // columnas
                col = i % columnas
                x = offset_x + col * (150 + espacio)
                y = margen_vertical + fila * (150 + 60)

                rect_img = pygame.Rect(x, y, 150, 150)

                # Fondo de tarjeta
                pygame.draw.rect(screen, (30, 30, 30), rect_img.inflate(10, 10), border_radius=10)
                if rect_img.collidepoint(mouse_pos):
                    # Hover: dibujar borde
                    pygame.draw.rect(screen, (255, 255, 255), rect_img.inflate(4, 4), 2, border_radius=10)

                screen.blit(mj["img"], (x, y))
                # Añadir desplazamiento vertical animado al texto
                offset_animado = int(
                    5 * sin(pygame.time.get_ticks() / 300 + i))  # i para que cada uno tenga un desfase diferente
                texto_rect = mj["texto_surf"].get_rect(center=(x + 75, y + 170 + offset_animado))
                screen.blit(mj["texto_surf"], texto_rect)

                mj["rect"] = rect_img

            # Botón Atrás
            font_boton = pygame.font.Font(None, 50)
            boton_atras = font_boton.render("Atrás", True, (255, 255, 255))
            rect_atras = boton_atras.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
            screen.blit(boton_atras, rect_atras)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if rect_atras.collidepoint(event.pos):
                        return
                    for mj in microjuegos:
                        if mj["rect"].collidepoint(event.pos):
                            juego = mj["clase"](screen, 10, 1)
                            juego.ejecutar()

                            # Reproducir la música del menú después de terminar el microjuego
                            control_audio.reproducir(archivo="Menu.mp3", loop=True)

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
                    exit()
                elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    # si aprieta ESC de nuevo, sale de pausa
                    return "continue"
                elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    for opt in opciones:
                        if opt["rect"].collidepoint(ev.pos):
                            return opt["action"]

            clock.tick(60)

