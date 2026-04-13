import tkinter as tk
from tkinter import ttk
import random

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import Perlin
import SimplexNoise
import Cellar_automat
import DiamondSquare


def main():
    root = tk.Tk()
    root.title("Noise Viewer")

    def on_close():
        root.destroy()
        root.quit()   # важно!

    def redraw_matrix(ax, canvas, matrix, title="Matrix"):
        ax.clear()
        ax.imshow(matrix, cmap='gray')
        ax.set_title(title)
        ax.axis("off")

        canvas.draw()

    root.protocol("WM_DELETE_WINDOW", on_close)

    # --- основной контейнер ---
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # --- левая часть (график) ---
    plot_frame = ttk.Frame(main_frame, width=600, height=600)
    plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
    plot_frame.pack_propagate(False)  # фиксируем размер

    # создаём тестовую матрицу
    matrix = np.random.randint(0,2, size=(100,100))

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(matrix, cmap='gray')
    ax.set_title("Matrix")
    ax.axis("off")

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # --- правая часть (кнопки) ---
    control_frame = ttk.Frame(main_frame, padding=10)
    control_frame.pack(side=tk.RIGHT, fill=tk.Y)

    # пустые callback'и
    def on_simplex():
        nonlocal matrix,ax,canvas
        grad=SimplexNoise.gen_gradients(2)

        p = list(range(256))
        random.shuffle(p)
        perm = p * 2

        lin_array = np.linspace(0, 10, 10*10, endpoint=False)
        x, y, z = np.meshgrid(lin_array, lin_array, np.linspace(0, 10, 10*10, endpoint=False) )
        matrix=SimplexNoise.mult_Simplex(x,y,perm,grad)
        aa1=np.array(matrix)
        redraw_matrix(ax,canvas,matrix)


    def on_perlin():
        pass

    def on_cellar():
        nonlocal matrix,ax,canvas
        matrix=Cellar_automat.next_generation_lands_v2(matrix,1,1,"B.3.6.7.8/S.3.4.6.7.8")
        redraw_matrix(ax,canvas,matrix)

    def on_diamond():
        nonlocal matrix,ax,canvas
        matrix=DiamondSquare.diamond_square(8,13,0.5)
        redraw_matrix(ax,canvas,matrix)

    # кнопки
    ttk.Button(control_frame, text="Simplex", command=on_simplex).pack(fill=tk.X, pady=5)
    ttk.Button(control_frame, text="Perlin", command=on_perlin).pack(fill=tk.X, pady=5)
    ttk.Button(control_frame, text="Cellar", command=on_cellar).pack(fill=tk.X, pady=5)
    ttk.Button(control_frame, text="Diamond_Square", command=on_diamond).pack(fill=tk.X, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()