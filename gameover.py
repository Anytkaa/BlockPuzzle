import tkinter as tk


class GameOverWindow:
    """Класс, отвечающий за отображение окна с сообщением о конце игры.
    Это окно включает информацию о счете и кнопки для начала новой игры."""

    def __init__(self, master, score, reset_callback):
        self.master = master
        self.score = score
        self.reset_callback = reset_callback
        self.window = tk.Toplevel(master)
        self.window.title("Конец игры")
        self.window.resizable(False, False)
        self.setup_window()
        self.load_content()

    def setup_window(self):
        window_width = 508
        window_height = 508
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    def load_content(self):
        background_image = tk.PhotoImage(
            file="assets/game_over.png")
        background_label = tk.Label(self.window, image=background_image)
        background_label.image = background_image  # Сохраняем ссылку на изображение
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        message = f"Игра окончена! Ваш счет: {self.score}"
        label = tk.Label(self.window, text=message, font=("Arial", 20), fg="red")
        label.pack(padx=10, pady=10)

        button = tk.Button(self.window, text="OK", command=self.close_window)
        button.pack(padx=70, pady=90)

    def close_window(self):
        self.window.destroy()
        self.reset_callback()
