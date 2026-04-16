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

    def redraw_matrix_blocked(ax, canvas, matrix, title="Matrix"):
        ax.clear()
        matrix=np.round(matrix,1)
        ax.imshow(matrix, cmap='gray')
        ax.set_title(title)
        ax.axis("off")

        canvas.draw()

    def resize_matrix(mat, new_shape):
        """
        Простейший рескейл через интерполяцию (без cv2)
        """
        y_old, x_old = mat.shape
        y_new, x_new = new_shape

        y_idx = np.linspace(0, y_old - 1, y_new).astype(int)
        x_idx = np.linspace(0, x_old - 1, x_new).astype(int)

        return mat[np.ix_(y_idx, x_idx)]
    
    def add_noise():
        nonlocal matrix

        # генерим второй шум (например Simplex)
        grad = SimplexNoise.generate_gradients(2)

        p = list(range(256))
        random.shuffle(p)
        perm = p * 2

        lin = np.linspace(0, 5, 80)  # другой размер специально
        x, y = np.meshgrid(lin, lin)

        matrix_2 = SimplexNoise.mult_Simplex(x, y, perm, grad)

        # рескейлим если надо
        if matrix_2.shape != matrix.shape:
            matrix_2 = resize_matrix(matrix_2, matrix.shape)

        matrix = (matrix + matrix_2) / 2

        redraw_matrix(ax, canvas, matrix, "Combined Noise")

    def island_mask(shape):
        h, w = shape

        x = np.linspace(0, w, w)
        y = np.linspace(0, h, h)

        xv, yv = np.meshgrid(x, y)

        cx = w / 2
        cy = h / 2

        mask = 1000 / ((xv - cx)**2 + (yv - cy)**2 + 1)

        # нормализация
        #mask -= mask.min()
        #mask /= mask.max()

        return mask
    
    def apply_mask():
        nonlocal matrix

        mask = island_mask(matrix.shape)

        matrix = matrix * mask

        redraw_matrix(ax, canvas, matrix, "Island Mask")

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
        x, y= np.meshgrid(lin_array, lin_array )
        matrix=SimplexNoise.mult_Simplex(x,y,perm,grad)
        aa1=np.array(matrix)
        redraw_matrix(ax,canvas,matrix)


    def open_perlin_window():
        win = tk.Toplevel(root)
        win.title("Perlin settings")

        entries = {}

        for label in ["x", "y", "tiles", "seed", "size"]:
            tk.Label(win, text=label).pack()
            e = tk.Entry(win)
            e.pack()
            entries[label] = e

        def generate():
            nonlocal matrix
            x = int(entries["x"].get())
            y = int(entries["y"].get())
            tiles = int(entries["tiles"].get())
            seed = int(entries["seed"].get())
            size = int(entries["size"].get())

            lin_x = np.linspace(0, x, x * tiles)
            lin_y = np.linspace(0, y, y * tiles)
            xv, yv = np.meshgrid(lin_x, lin_y)

            matrix = Perlin.mult_perlin(xv, yv, seed=seed, size=size)
            redraw_matrix(ax, canvas, matrix, "Perlin")

        tk.Button(win, text="Generate", command=generate).pack()

    def open_cellar_window():
        win = tk.Toplevel(root)
        win.title("Cellular Automaton")

        mode_var = tk.StringVar(value="Moore")

        tk.Label(win, text="Mode").pack()
        tk.Radiobutton(win, text="Moore", variable=mode_var, value="Moore").pack()
        tk.Radiobutton(win, text="Neumann", variable=mode_var, value="Neumann").pack()

        tk.Label(win, text="Distance").pack()
        dist_entry = tk.Entry(win)
        dist_entry.pack()

        tk.Label(win, text="Rule").pack()
        rule_entry = tk.Entry(win)
        rule_entry.pack()

        def generate():
            nonlocal matrix

            mode = 1 if mode_var.get() == "Moore" else 0
            distance = int(dist_entry.get())
            rule = rule_entry.get()

            matrix = Cellar_automat.next_generation_lands_v2(
                matrix, mode, distance, rule
            )

            redraw_matrix(ax, canvas, matrix, "Cellular")

        tk.Button(win, text="Generate", command=generate).pack()


    def open_diamond_window():
        win = tk.Toplevel(root)
        win.title("Diamond Square")

        tk.Label(win, text="n").pack()
        n_entry = tk.Entry(win)
        n_entry.pack()

        tk.Label(win, text="seed").pack()
        seed_entry = tk.Entry(win)
        seed_entry.pack()

        tk.Label(win, text="roughness").pack()
        rough_entry = tk.Entry(win)
        rough_entry.pack()

        def generate():
            nonlocal matrix

            n = int(n_entry.get())
            seed = int(seed_entry.get())
            rough = float(rough_entry.get())

            matrix = DiamondSquare.diamond_square(n, seed, rough)
            redraw_matrix(ax, canvas, matrix, "Diamond")

        tk.Button(win, text="Generate", command=generate).pack()

    def open_simplex_window():
        win = tk.Toplevel(root)
        win.title("Simplex")

        tk.Label(win, text="seed").pack()
        seed_entry = tk.Entry(win)
        seed_entry.pack()

        tk.Label(win, text="dimension (2-4)").pack()
        n_entry = tk.Entry(win)
        n_entry.pack()

        entries = {}
        for label in ["x", "y", "z", "w"]:
            tk.Label(win, text=label).pack()
            e = tk.Entry(win)
            e.pack()
            entries[label] = e

        def generate():
            nonlocal matrix

            seed = int(seed_entry.get())
            n = int(n_entry.get())

            grad = SimplexNoise.gen_gradients(n)

            p = list(range(256))
            random.seed(seed)
            random.shuffle(p)
            perm = p * 2

            size = int(entries["x"].get())
            lin = np.linspace(0, 5, size)
            x, y = np.meshgrid(lin, lin)

            result = np.zeros_like(x)

            z = float(entries["z"].get() or 0)
            w = float(entries["w"].get() or 0)

            for i in range(x.shape[0]):
                for j in range(x.shape[1]):
                    coords = [x[i, j], y[i, j]]

                    if n >= 3:
                        coords.append(z)
                    if n == 4:
                        coords.append(w)

                    result[i, j] = SimplexNoise.SimplexNoise(coords, perm, grad)

            matrix = result
            redraw_matrix(ax, canvas, matrix, "Simplex")

        tk.Button(win, text="Generate", command=generate).pack()


    """def on_perlin():
        pass

    def on_cellar():
        nonlocal matrix,ax,canvas
        matrix=Cellar_automat.next_generation_lands_v2(matrix,1,1,"B.3.6.7.8/S.3.4.6.7.8")
        redraw_matrix(ax,canvas,matrix)

    def on_diamond():
        nonlocal matrix,ax,canvas
        matrix=DiamondSquare.diamond_square(8,13,0.5)
        redraw_matrix(ax,canvas,matrix) """

    def redraw_blocked():
        nonlocal matrix,ax,canvas
        matrix = np.round(matrix,1)
        redraw_matrix_blocked(ax, canvas, matrix, "block")

    # кнопки
    ttk.Button(control_frame, text="Perlin", command=open_perlin_window).pack(fill=tk.X, pady=5)
    ttk.Button(control_frame, text="Cellar", command=open_cellar_window).pack(fill=tk.X, pady=5)
    ttk.Button(control_frame, text="Diamond_Square", command=open_diamond_window).pack(fill=tk.X, pady=5)
    ttk.Button(control_frame, text="Simplex", command=open_simplex_window).pack(fill=tk.X, pady=5)
    ttk.Button(control_frame, text="redraw_block", command=redraw_blocked).pack(fill=tk.X, pady=5)

    ttk.Button(control_frame, text="Add Noise", command=add_noise).pack(fill=tk.X, pady=5)
    ttk.Button(control_frame, text="Apply Mask", command=apply_mask).pack(fill=tk.X, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()