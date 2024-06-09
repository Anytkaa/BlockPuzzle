import tkinter as tk
from tkinter import Label, Button

from config import RULE_WINDOW_SIZE


class RulesWindow:
    def __init__(self, master):
        self.master = master
        self.setup_window()

    def setup_window(self):
        self.rules_window = tk.Toplevel(self.master)
        self.rules_window.title("Правила игры")
        self.rules_window.geometry(RULE_WINDOW_SIZE)
        self.rules_window.resizable(False, False)

        # Отображение изображения с правилами
        image_path = "assets/rules.png"
        self.rules_image = tk.PhotoImage(file=image_path)
        label = Label(self.rules_window, image=self.rules_image)
        label.pack(fill="both", expand=True)

        # Кнопка выхода
        exit_button = Button(self.rules_window, text="Выход", command=self.exit_rules, font=("helvetica", 20),
                             fg="black")
        exit_button.config(bg="white", width=15, height=2)
        exit_button.place(x=900, y=20)

        self.center_window(self.rules_window, offset_y=70)

    def center_window(self, window, offset_y=50):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2) - offset_y
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def exit_rules(self):
        self.rules_window.destroy()


def show_rules(master):
    RulesWindow(master)
