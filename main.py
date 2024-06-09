import tkinter as tk
from menu import MainMenu


def main():
    root = tk.Tk()
    menu = MainMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()
