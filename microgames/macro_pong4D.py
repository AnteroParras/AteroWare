import tkinter as tk
import random
from microgames.microgame_base import MicrojuegoBase


class Pong4D(MicrojuegoBase):
    def __init__(self, time, screen, dificultad):
        super().__init__(screen, 400, dificultad=dificultad)

        # Configuración general
        self.tk_root = tk.Tk()
        self.tk_root.withdraw()  # Ocultar ventana principal

        # Parámetros configurables
        self.SCREEN_WIDTH = self.tk_root.winfo_screenwidth()
        self.SCREEN_HEIGHT = self.tk_root.winfo_screenheight()
        self.BALL_SIZE = 50
        self.PADDLE_WIDTH = 20
        self.PADDLE_HEIGHT = 100
        self.BALL_SPEED = 5
        self.PADDLE_SPEED = 10  # Reducida la velocidad de la paleta
        self.PADDLE_1_COLOR = "blue"
        self.PADDLE_2_COLOR = "green"
        self.FRAME_RATE = 8  # 60 FPS
        self.LEVEL = 3 # self.dificultad  # Nivel del bot (1: fácil, 2: medio, 3: difícil)
        self.SPEED_INCREMENT = 1.1  # Incremento de velocidad por cada rebote en la paleta
        self.MAX_BALL_SPEED = 12  # Velocidad máxima de la bola
        self.MIN_BALL_SPEED = 4  # Velocidad mínima de la bola

        # Crear ventanas
        self._crear_ventanas()

        # Variables de movimiento y puntaje
        self.ball_dx, self.ball_dy = random.choice([-self.BALL_SPEED, self.BALL_SPEED]), random.choice(
            [-self.BALL_SPEED, self.BALL_SPEED])
        self.paddle_left_y = self.SCREEN_HEIGHT // 2 - 50
        self.paddle_right_y = self.SCREEN_HEIGHT // 2 - 50
        self.paddle_left_moving = 0  # -1 para arriba, 1 para abajo, 0 para detenerse

        self.score_left = 0
        self.score_right = 0
        self.win = False

        # Enlazar teclas directamente a las ventanas de las paletas
        self.paddle_left.bind('<KeyPress>', self._on_key_press)
        self.paddle_left.bind('<KeyRelease>', self._on_key_release)

        # Forzar foco en las ventanas de las paletas
        self.paddle_left.focus_force()

    def _on_key_press(self, event):
        if event.keysym == 'w':
            self.paddle_left_moving = -1
        elif event.keysym == 's':
            self.paddle_left_moving = 1

    def _on_key_release(self, event):
        if event.keysym in ('w', 's'):
            self.paddle_left_moving = 0

    def move_paddle(self):
        if self.paddle_left_moving == -1 and self.paddle_left_y > 0:
            self.paddle_left_y -= self.PADDLE_SPEED
        elif self.paddle_left_moving == 1 and self.paddle_left_y < self.SCREEN_HEIGHT - self.PADDLE_HEIGHT:
            self.paddle_left_y += self.PADDLE_SPEED

        self.paddle_left.geometry(f"{self.PADDLE_WIDTH}x{self.PADDLE_HEIGHT}+50+{self.paddle_left_y}")
        self.paddle_left.after(self.FRAME_RATE, self.move_paddle)

    def _crear_ventanas(self):
        # Crear ventana de la bola
        self.ball = tk.Toplevel()
        self.ball.geometry(f"{self.BALL_SIZE}x{self.BALL_SIZE}+{self.SCREEN_WIDTH // 2}+{self.SCREEN_HEIGHT // 2}")
        self.ball.overrideredirect(True)
        self.ball.configure(bg="red")

        # Crear ventanas para las paletas
        self.paddle_left = tk.Toplevel()
        self.paddle_left.geometry(f"{self.PADDLE_WIDTH}x{self.PADDLE_HEIGHT}+50+{self.SCREEN_HEIGHT // 2 - 50}")
        self.paddle_left.overrideredirect(True)
        self.paddle_left.configure(bg=self.PADDLE_1_COLOR)

        self.paddle_right = tk.Toplevel()
        self.paddle_right.geometry(
            f"{self.PADDLE_WIDTH}x{self.PADDLE_HEIGHT}+{self.SCREEN_WIDTH - 70}+{self.SCREEN_HEIGHT // 2 - 50}")
        self.paddle_right.overrideredirect(True)
        self.paddle_right.configure(bg=self.PADDLE_2_COLOR)

        # Crear ventana para el marcador
        self.score_window = tk.Toplevel()
        self.score_window.geometry(f"{200}x{100}+{self.SCREEN_WIDTH // 2 - 100}+{50}")
        self.score_window.overrideredirect(True)
        self.score_window.configure(bg="black")
        self.score_label = tk.Label(self.score_window, text="0 - 0", font=("Arial", 24), fg="white", bg="black")
        self.score_label.pack(expand=True)

    def move_ball(self):
        x, y = map(int, self.ball.geometry().split('+')[1:])
        x_new, y_new = int(x + self.ball_dx), int(y + self.ball_dy)

        # Rebote en los bordes superior e inferior
        if y_new <= 0 or y_new >= self.SCREEN_HEIGHT - self.BALL_SIZE:
            self.ball_dy *= -1

        if x_new <= 70 and self.paddle_left_y < y_new + self.BALL_SIZE and y_new < self.paddle_left_y + self.PADDLE_HEIGHT:
            self.ball_dx = abs(self.ball_dx) * self.SPEED_INCREMENT  # Incrementar velocidad
            self.ball_dx = min(self.ball_dx, self.MAX_BALL_SPEED)  # Limitar velocidad máxima
            self.ball_dy *= self.SPEED_INCREMENT
            self.ball_dy = max(min(self.ball_dy, self.MAX_BALL_SPEED), -self.MAX_BALL_SPEED)
            x_new = 71  # Ajustar posición para evitar múltiples colisiones

            # Detectar colisión con la paleta derecha
        elif x_new + self.BALL_SIZE >= self.SCREEN_WIDTH - 70 and self.paddle_right_y < y_new + self.BALL_SIZE and y_new < self.paddle_right_y + self.PADDLE_HEIGHT:
            self.ball_dx = -abs(self.ball_dx) * self.SPEED_INCREMENT  # Incrementar velocidad
            self.ball_dx = max(self.ball_dx, -self.MAX_BALL_SPEED)  # Limitar velocidad máxima
            self.ball_dy *= self.SPEED_INCREMENT
            self.ball_dy = max(min(self.ball_dy, self.MAX_BALL_SPEED), -self.MAX_BALL_SPEED)
            x_new = self.SCREEN_WIDTH - 71 - self.BALL_SIZE  # Ajustar posición para evitar múltiples colisiones

        # Pérdida y actualización de marcador
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

        # Actualizar marcador
        self.score_label.config(text=f"{self.score_left} - {self.score_right}")

        # Verificar si alguien ganó
        if self.score_left == 1:
            self.win = True
            self._mostrar_mensaje_victoria()
            print("Ganó el jugador izquierdo", self.win)
            return self.win

        if self.score_right == 5:
            return self.win

        self.ball.geometry(f"{self.BALL_SIZE}x{self.BALL_SIZE}+{x_new}+{y_new}")
        self.ball.after(self.FRAME_RATE, self.move_ball)

    def _mostrar_mensaje_victoria(self):
        ventana_victoria = tk.Toplevel()
        ventana_victoria.geometry(f"400x200+{self.SCREEN_WIDTH // 2 - 200}+{self.SCREEN_HEIGHT // 2 - 100}")
        ventana_victoria.overrideredirect(True)
        ventana_victoria.configure(bg="black")
        mensaje = tk.Label(ventana_victoria, text="¡Ole que ole!", font=("Arial", 24), fg="white", bg="black")
        mensaje.pack(expand=True)

        # Actualiza self.win y cierra la ventana después de 2 segundos
        ventana_victoria.after(2000, lambda: (setattr(self, 'win', True), self.tk_root.destroy()))

    def move_bot(self):
        _, ball_y = map(int, self.ball.geometry().split('+')[1:])
        center_y = self.paddle_right_y + self.PADDLE_HEIGHT // 2

        # Ajustar velocidad del bot según el nivel
        if self.LEVEL == 1:
            reaction_speed = self.PADDLE_SPEED // 2
        elif self.LEVEL == 2:
            reaction_speed = self.PADDLE_SPEED * 2 // 3
        else:
            reaction_speed = self.PADDLE_SPEED

        # Movimiento del bot con margen de tolerancia
        if abs(ball_y - center_y) > 20:  # Margen de tolerancia
            if ball_y > center_y and self.paddle_right_y < self.SCREEN_HEIGHT - self.PADDLE_HEIGHT:
                self.paddle_right_y += reaction_speed
            elif ball_y < center_y and self.paddle_right_y > 0:
                self.paddle_right_y -= reaction_speed

        self.paddle_right.geometry(
            f"{self.PADDLE_WIDTH}x{self.PADDLE_HEIGHT}+{self.SCREEN_WIDTH - 70}+{self.paddle_right_y}")
        self.paddle_right.after(self.FRAME_RATE, self.move_bot)

    def ejecutar(self):
        self.move_paddle()
        self.move_ball()
        self.move_bot()
        self.tk_root.mainloop()
        return self.win
