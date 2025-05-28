import tkinter as tk
import random
from microgames.microgame_base import MicrojuegoBase
from core.gestor_audio import Audio


class Pong4D(MicrojuegoBase):
    """Microjuego de Pong 4D, una versión del clásico Pong con dos palas y una bola que rebota."""
    def __init__(self, time, screen, dificultad):
        super().__init__(screen, 400, dificultad=dificultad)

        # Inicializar el gestor de audio y la música del microjuego
        self.audio = Audio()
        self.music_file = "FinalBoss.mp3"

        # Inicializar la ventana de tkinter
        self.tk_root = tk.Tk()
        self.tk_root.withdraw()

        # Configuración de la pantalla y dimensiones del microjuego
        self.SCREEN_WIDTH = self.tk_root.winfo_screenwidth()
        self.SCREEN_HEIGHT = self.tk_root.winfo_screenheight()
        self.BALL_SIZE = 50
        self.PADDLE_WIDTH = 20
        self.PADDLE_HEIGHT = 100
        self.BALL_SPEED = 5
        self.PADDLE_SPEED = 10
        self.PADDLE_1_COLOR = "blue"
        self.PADDLE_2_COLOR = "green"
        self.FRAME_RATE = 8
        self.LEVEL = 2
        self.SPEED_INCREMENT = 1.1
        self.MAX_BALL_SPEED = 12
        self.MIN_BALL_SPEED = 4

        self._crear_ventanas()

        # Inicializar la bola y las palas
        self.ball_dx, self.ball_dy = random.choice([-self.BALL_SPEED, self.BALL_SPEED]), random.choice(
            [-self.BALL_SPEED, self.BALL_SPEED])
        self.paddle_left_y = self.SCREEN_HEIGHT // 2 - 50
        self.paddle_right_y = self.SCREEN_HEIGHT // 2 - 50
        self.paddle_left_moving = 0

        # Score_left : jugador
        # Score_right : bot
        self.score_left = 0
        self.score_right = 0
        self.win = False

        # Configurar la pala izquierda para recibir eventos de teclado
        self.paddle_left.bind('<KeyPress>', self._on_key_press)
        self.paddle_left.bind('<KeyRelease>', self._on_key_release)
        self.paddle_left.focus_force()

    def _on_key_press(self, event):
        """Maneja los eventos de pulsación de teclas para mover la pala izquierda."""
        if event.keysym == 'w':
            self.paddle_left_moving = -1
        elif event.keysym == 's':
            self.paddle_left_moving = 1

    def _on_key_release(self, event):
        """Maneja los eventos de liberación de teclas para detener el movimiento de la pala izquierda."""
        if event.keysym in ('w', 's'):
            self.paddle_left_moving = 0

    def move_paddle(self):
        """Mueve la pala izquierda según la tecla presionada."""
        if self.paddle_left_moving == -1 and self.paddle_left_y > 0:
            self.paddle_left_y -= self.PADDLE_SPEED
        elif self.paddle_left_moving == 1 and self.paddle_left_y < self.SCREEN_HEIGHT - self.PADDLE_HEIGHT:
            self.paddle_left_y += self.PADDLE_SPEED

        self.paddle_left.geometry(f"{self.PADDLE_WIDTH}x{self.PADDLE_HEIGHT}+50+{self.paddle_left_y}")
        self.paddle_left.after(self.FRAME_RATE, self.move_paddle)

    def _crear_ventanas(self):
        """Crea las ventanas necesarias para el microjuego."""
        self.ball = tk.Toplevel()
        self.ball.geometry(f"{self.BALL_SIZE}x{self.BALL_SIZE}+{self.SCREEN_WIDTH // 2}+{self.SCREEN_HEIGHT // 2}")
        self.ball.overrideredirect(True)
        self.ball.configure(bg="red")

        self.paddle_left = tk.Toplevel()
        self.paddle_left.geometry(f"{self.PADDLE_WIDTH}x{self.PADDLE_HEIGHT}+50+{self.SCREEN_HEIGHT // 2 - 50}")
        self.paddle_left.overrideredirect(True)
        self.paddle_left.configure(bg=self.PADDLE_1_COLOR)

        self.paddle_right = tk.Toplevel()
        self.paddle_right.geometry(
            f"{self.PADDLE_WIDTH}x{self.PADDLE_HEIGHT}+{self.SCREEN_WIDTH - 70}+{self.SCREEN_HEIGHT // 2 - 50}")
        self.paddle_right.overrideredirect(True)
        self.paddle_right.configure(bg=self.PADDLE_2_COLOR)

        self.score_window = tk.Toplevel()
        self.score_window.geometry(f"{200}x{100}+{self.SCREEN_WIDTH // 2 - 100}+{50}")
        self.score_window.overrideredirect(True)
        self.score_window.configure(bg="black")
        self.score_label = tk.Label(self.score_window, text="0 - 0", font=("Arial", 24), fg="white", bg="black")
        self.score_label.pack(expand=True)

    def move_ball(self):
        """Mueve la bola y maneja las colisiones con las paredes y las palas."""
        x, y = map(int, self.ball.geometry().split('+')[1:])
        x_new, y_new = int(x + self.ball_dx), int(y + self.ball_dy)

        if y_new <= 0 or y_new >= self.SCREEN_HEIGHT - self.BALL_SIZE:
            self.ball_dy *= -1

        if x_new <= 70 and self.paddle_left_y < y_new + self.BALL_SIZE and y_new < self.paddle_left_y + self.PADDLE_HEIGHT:
            self.ball_dx = abs(self.ball_dx) * self.SPEED_INCREMENT
            self.ball_dx = min(self.ball_dx, self.MAX_BALL_SPEED)
            self.ball_dy *= self.SPEED_INCREMENT
            self.ball_dy = max(min(self.ball_dy, self.MAX_BALL_SPEED), -self.MAX_BALL_SPEED)
            x_new = 71

        elif x_new + self.BALL_SIZE >= self.SCREEN_WIDTH - 70 and self.paddle_right_y < y_new + self.BALL_SIZE and y_new < self.paddle_right_y + self.PADDLE_HEIGHT:
            self.ball_dx = -abs(self.ball_dx) * self.SPEED_INCREMENT
            self.ball_dx = max(self.ball_dx, -self.MAX_BALL_SPEED)
            self.ball_dy *= self.SPEED_INCREMENT
            self.ball_dy = max(min(self.ball_dy, self.MAX_BALL_SPEED), -self.MAX_BALL_SPEED)
            x_new = self.SCREEN_WIDTH - 71 - self.BALL_SIZE

        if x_new <= 0:
            self.score_right += 1
            x_new, y_new = self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2
            self.ball_dx, self.ball_dy = random.choice([-self.BALL_SPEED, self.BALL_SPEED]), random.choice(
                [-self.BALL_SPEED, self.BALL_SPEED])
        elif x_new >= self.SCREEN_WIDTH - self.BALL_SIZE:
            self.score_left += 1
            x_new, y_new = self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2
            self.ball_dx, self.ball_dy = random.choice([-self.BALL_SPEED, self.BALL_SPEED]), random.choice(
                [-self.BALL_SPEED, self.BALL_SPEED])

        self.score_label.config(text=f"{self.score_left} - {self.score_right}")

        if self.score_left == 5:
            self.win = True
            self._mostrar_mensaje_victoria()
            self.tk_root.after(3000, self.tk_root.quit)
            return

        if self.score_right == 5:
            self.win = False
            self._mostrar_mensaje_derrota()
            self.tk_root.after(3000, self.tk_root.quit)
            return

        self.ball.geometry(f"{self.BALL_SIZE}x{self.BALL_SIZE}+{x_new}+{y_new}")
        self.ball.after(self.FRAME_RATE, self.move_ball)

    def _mostrar_mensaje_victoria(self):
        """Muestra un mensaje de victoria en una ventana emergente."""
        ventana_victoria = tk.Toplevel()
        ventana_victoria.geometry(f"400x200+{self.SCREEN_WIDTH // 2 - 200}+{self.SCREEN_HEIGHT // 2 - 100}")
        ventana_victoria.overrideredirect(True)
        ventana_victoria.configure(bg="black")
        mensaje = tk.Label(ventana_victoria, text="¡Ole que ole!", font=("Arial", 24), fg="white", bg="black")
        mensaje.pack(expand=True)

        def cerrar_todo():
            """Cierra todas las ventanas y finaliza el microjuego."""
            ventana_victoria.destroy()
            self.ball.destroy()
            self.paddle_left.destroy()
            self.paddle_right.destroy()
            self.score_window.destroy()
            self.tk_root.quit()

        ventana_victoria.after(3000, cerrar_todo)

    def _mostrar_mensaje_derrota(self):
        """Muestra un mensaje de derrota en una ventana emergente."""
        ventana_derrota = tk.Toplevel()
        ventana_derrota.geometry(f"400x200+{self.SCREEN_WIDTH // 2 - 200}+{self.SCREEN_HEIGHT // 2 - 100}")
        ventana_derrota.overrideredirect(True)
        ventana_derrota.configure(bg="black")
        mensaje = tk.Label(ventana_derrota, text="¡Has perdido!", font=("Arial", 24), fg="white", bg="black")
        mensaje.pack(expand=True)

    def move_bot(self):
        """Mueve la pala derecha (bot) para seguir la bola."""
        _, ball_y = map(int, self.ball.geometry().split('+')[1:])
        center_y = self.paddle_right_y + self.PADDLE_HEIGHT // 2

        if self.LEVEL == 1:
            reaction_speed = self.PADDLE_SPEED // 2
        elif self.LEVEL == 2:
            reaction_speed = self.PADDLE_SPEED * 2 // 3
        else:
            reaction_speed = self.PADDLE_SPEED

        if abs(ball_y - center_y) > 20:
            if ball_y > center_y and self.paddle_right_y < self.SCREEN_HEIGHT - self.PADDLE_HEIGHT:
                self.paddle_right_y += reaction_speed
            elif ball_y < center_y and self.paddle_right_y > 0:
                self.paddle_right_y -= reaction_speed

        self.paddle_right.geometry(
            f"{self.PADDLE_WIDTH}x{self.PADDLE_HEIGHT}+{self.SCREEN_WIDTH - 70}+{self.paddle_right_y}")
        self.paddle_right.after(self.FRAME_RATE, self.move_bot)

    def inicio_piringolo(self):
        """Inicializa el microjuego y muestra un mensaje de inicio."""
        self.paddle_left.withdraw()
        self.paddle_right.withdraw()
        self.score_window.withdraw()
        self.ball.withdraw()

        self.tk_root.after(1700, lambda: self.paddle_left.deiconify())
        self.tk_root.after(3300, lambda: self.paddle_right.deiconify())
        self.tk_root.after(5000, lambda: self.score_window.deiconify())
        self.tk_root.after(6000, lambda: self.ball.deiconify())

        def mostrar_mensaje():
            """Muestra un mensaje de inicio del juego."""
            ventana_mensaje = tk.Toplevel()
            ventana_mensaje.geometry(f"400x200+{self.SCREEN_WIDTH // 2 - 200}+{self.SCREEN_HEIGHT // 2 - 100}")
            ventana_mensaje.overrideredirect(True)
            ventana_mensaje.configure(bg="black")
            mensaje = tk.Label(ventana_mensaje, text="¡Que empiece el juego!", font=("Arial", 24), fg="white",
                               bg="black")
            mensaje.pack(expand=True)
            ventana_mensaje.after(1500, ventana_mensaje.destroy)

        self.tk_root.after(8000, mostrar_mensaje)

    def ejecutar(self):
        """Ejecuta el microjuego y maneja la lógica del juego."""
        self.audio.reproducir(archivo=self.music_file, loop=True)
        self.inicio_piringolo()
        self.tk_root.after(10000, self.move_paddle)
        self.tk_root.after(10000, self.move_ball)
        self.tk_root.after(10000, self.move_bot)
        self.tk_root.mainloop()
        self.audio.detener()
        return self.win
