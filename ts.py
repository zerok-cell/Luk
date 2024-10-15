import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.title("Тема окна")


button = ttk.Button(root, text="Переключить тему", command=lambda: toggle_theme())
button.pack()

# Определяем текущую тему
is_light_theme = True


def toggle_theme():
    global is_light_theme
    print(is_light_theme)
    is_light_theme = not is_light_theme
    apply_theme()


def apply_theme():
    if is_light_theme:
        root.configure(bg="black")
        button.configureforeground=("black")
    else:
        root.configure(bg="white")
        button.configureforeground=("white")
        button.configureforeground=("white")


if root.cget("bg") == "gray":
    is_light_theme = False
    apply_theme()

root.mainloop()
# Юз глобал варов 