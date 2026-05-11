import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
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

    def update_size_label():
        size_label.config(text=f"Size: {matrix.shape[0]} x {matrix.shape[1]}")


    def redraw_matrix(ax, canvas, matrix, title="Matrix"):
        ax.clear()
        ax.imshow(matrix, cmap='gray')
        ax.set_title(title)
        ax.axis("off")
        canvas.draw()
        update_size_label()


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
        nonlocal matrix, ax, canvas

        win = tk.Toplevel(root)
        win.title("Add Noise")

        preview_matrix = np.copy(matrix)

        add_main_frame = ttk.Frame(win)
        add_main_frame.pack(fill=tk.BOTH, expand=True)

        preview_frame = ttk.Frame(add_main_frame, width=500, height=500)
        preview_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        preview_frame.pack_propagate(False)

        control_frame_2 = ttk.Frame(add_main_frame, padding=10)
        control_frame_2.pack(side=tk.RIGHT, fill=tk.Y)


        fig2, ax2 = plt.subplots(figsize=(5, 5))
        ax2.imshow(preview_matrix, cmap='gray')
        ax2.set_title("matrix_2")
        ax2.axis("off")

        canvas2 = FigureCanvasTkAgg(fig2, master=preview_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        def redraw_preview(title="matrix_2"):
            nonlocal preview_matrix
            ax2.clear()
            ax2.imshow(preview_matrix, cmap='gray')
            ax2.set_title(title)
            ax2.axis("off")
            canvas2.draw()

        def redraw_preview_bw(border, title="matrix_2 BW"):
            nonlocal preview_matrix
            bw = (preview_matrix >= border).astype(int)
            ax2.clear()
            ax2.imshow(bw, cmap='gray')
            ax2.set_title(title)
            ax2.axis("off")
            canvas2.draw()

        def open_perlin_window_2():
            win2 = tk.Toplevel(win)
            win2.title("Perlin settings")

            entries = {}
            for label in ["x", "y", "tiles", "seed", "size"]:
                tk.Label(win2, text=label).pack()
                e = tk.Entry(win2)
                e.pack()
                entries[label] = e

            def generate():
                nonlocal preview_matrix
                x = int(entries["x"].get())
                y = int(entries["y"].get())
                tiles = int(entries["tiles"].get())
                seed = int(entries["seed"].get())
                size = int(entries["size"].get())

                lin_x = np.linspace(0, x, x * tiles)
                lin_y = np.linspace(0, y, y * tiles)
                xv, yv = np.meshgrid(lin_x, lin_y)

                preview_matrix = Perlin.mult_perlin(xv, yv, seed=seed, size=size)
                redraw_preview("Perlin")
                win2.destroy()

            tk.Button(win2, text="Generate", command=generate).pack()

        def open_cellar_window_2():
            win2 = tk.Toplevel(win)
            win2.title("Cellular Automaton")

            mode_var = tk.StringVar(value="Moore")

            tk.Label(win2, text="Mode").pack()
            tk.Radiobutton(win2, text="Moore", variable=mode_var, value="Moore").pack()
            tk.Radiobutton(win2, text="Neumann", variable=mode_var, value="Neumann").pack()

            tk.Label(win2, text="Distance").pack()
            dist_entry = tk.Entry(win2)
            dist_entry.pack()

            tk.Label(win2, text="Rule").pack()
            rule_entry = tk.Entry(win2)
            rule_entry.pack()

            def generate():
                nonlocal preview_matrix
                mode = 1 if mode_var.get() == "Moore" else 2
                distance = int(dist_entry.get())
                rule = rule_entry.get()

                preview_matrix = Cellar_automat.next_generation_lands_v2(
                    preview_matrix, mode, distance, rule
                )
                redraw_preview("Cellular")
                win2.destroy()

            tk.Button(win2, text="Generate", command=generate).pack()

        def open_diamond_window_2():
            win2 = tk.Toplevel(win)
            win2.title("Diamond Square")

            tk.Label(win2, text="n").pack()
            n_entry = tk.Entry(win2)
            n_entry.pack()

            tk.Label(win2, text="seed").pack()
            seed_entry = tk.Entry(win2)
            seed_entry.pack()

            tk.Label(win2, text="roughness").pack()
            rough_entry = tk.Entry(win2)
            rough_entry.pack()

            def generate():
                nonlocal preview_matrix
                n = int(n_entry.get())
                seed = int(seed_entry.get())
                rough = float(rough_entry.get())

                preview_matrix = DiamondSquare.diamond_square(n, seed, rough)
                redraw_preview("Diamond")
                win2.destroy()

            tk.Button(win2, text="Generate", command=generate).pack()

        def open_simplex_window_2():
            win2 = tk.Toplevel(win)
            win2.title("Simplex")

            tk.Label(win2, text="seed").pack()
            seed_entry = tk.Entry(win2)
            seed_entry.pack()

            tk.Label(win2, text="dimension (2-4)").pack()
            n_entry = tk.Entry(win2)
            n_entry.pack()

            entries = {}
            for label in ["x", "y", "z", "w"]:
                tk.Label(win2, text=label).pack()
                e = tk.Entry(win2)
                e.pack()
                entries[label] = e

            def generate():
                nonlocal preview_matrix

                seed = int(seed_entry.get())
                n = int(n_entry.get())

                grad = SimplexNoise.generate_gradients(n)

                p = list(range(256))
                random.seed(seed)
                random.shuffle(p)
                perm = p * 2

                x_size = int(entries["x"].get())
                y_size = int(entries["y"].get())

                lin_x = np.linspace(0, 5, x_size)
                lin_y = np.linspace(0, 5, y_size)
                xv, yv = np.meshgrid(lin_x, lin_y)

                result = np.zeros_like(xv)

                z = float(entries["z"].get() or 0)
                wv = float(entries["w"].get() or 0)

                for i in range(xv.shape[0]):
                    for j in range(xv.shape[1]):
                        coords = [xv[i, j], yv[i, j]]

                        if n >= 3:
                            coords.append(z)
                        if n == 4:
                            coords.append(wv)

                        result[i, j] = SimplexNoise.SimplexNoise(coords, perm, grad)

                preview_matrix = result
                redraw_preview("Simplex")
                win2.destroy()

            tk.Button(win2, text="Generate", command=generate).pack()

        def redraw_blocked_2():
            nonlocal preview_matrix
            preview_matrix = np.round(preview_matrix, 1)
            redraw_preview("block")

        def redraw_black_white_2():
            nonlocal preview_matrix

            win2 = tk.Toplevel(win)
            win2.title("Black & White")

            tk.Label(win2, text="border").pack()
            entry = tk.Entry(win2)
            entry.pack()

            def generate():
                nonlocal preview_matrix
                border = float(entry.get() or 0.5)
                preview_matrix = (preview_matrix >= border).astype(int)
                redraw_preview("Black & White")
                win2.destroy()

            tk.Button(win2, text="Generate", command=generate).pack()

        def apply_noise():
            nonlocal matrix, preview_matrix

            matrix_2 = preview_matrix
            if matrix_2.shape != matrix.shape:
                matrix_2 = resize_matrix(matrix_2, matrix.shape)

            matrix = (matrix + matrix_2) / 2
            redraw_matrix(ax, canvas, matrix, "Combined Noise")
            plt.close(fig2)
            win.destroy()

        ttk.Button(control_frame_2, text="Perlin", command=open_perlin_window_2).pack(fill=tk.X, pady=5)
        ttk.Button(control_frame_2, text="Cellar", command=open_cellar_window_2).pack(fill=tk.X, pady=5)
        ttk.Button(control_frame_2, text="Diamond_Square", command=open_diamond_window_2).pack(fill=tk.X, pady=5)
        ttk.Button(control_frame_2, text="Simplex", command=open_simplex_window_2).pack(fill=tk.X, pady=5)
        ttk.Button(control_frame_2, text="redraw_block", command=redraw_blocked_2).pack(fill=tk.X, pady=5)
        ttk.Button(control_frame_2, text="redraw_black_white", command=redraw_black_white_2).pack(fill=tk.X, pady=5)
        ttk.Button(control_frame_2, text="Apply", command=apply_noise).pack(fill=tk.X, pady=15)



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
    size_label = ttk.Label(control_frame, text="")
    size_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

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

        for label in ["x", "y", "tiles", "seed", "size","octaves"]:
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
            octaves = int(entries["octaves"].get())

            lin_x = np.linspace(0, x, x * tiles)
            lin_y = np.linspace(0, y, y * tiles)
            xv, yv = np.meshgrid(lin_x, lin_y)

            matrix = Perlin.fractal_perlin(xv, yv, seed=seed, size=size, octaves=octaves)
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

        tk.Label(win, text="octaves").pack()
        octaves_entry = tk.Entry(win)
        octaves_entry.pack()

        def generate():
            nonlocal matrix

            n = int(n_entry.get())
            seed = int(seed_entry.get())
            rough = float(rough_entry.get())
            octaves=int(octaves_entry.get())

            matrix = DiamondSquare.fractal_diamond_square(n, seed, rough,octaves)
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

        tk.Label(win, text="octaves").pack()
        octaves_entry = tk.Entry(win)
        octaves_entry.pack()

        def generate():
            nonlocal matrix

            seed = int(seed_entry.get())
            n = int(n_entry.get())

            grad = SimplexNoise.gen_gradients(n)

            p = list(range(256))
            random.seed(seed)
            random.shuffle(p)
            perm = p * 2

            octaves=int(octaves_entry.get())

            size = int(entries["x"].get())
            lin = np.linspace(0, 5, size)
            x, y = np.meshgrid(lin, lin)

            result = np.zeros_like(x)

            z = float(entries["z"].get() or 0)
            w = float(entries["w"].get() or 0)
            if n==2:
                matrix = SimplexNoise.fractal_simplex(x, y, seed=seed, n_dim=2, octaves=octaves)
            else:

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


    def redraw_matrix_BW(ax, canvas, matrix, border, title="Matrix"):
        bw_matrix = np.where(matrix < border, 0, 1)

        ax.clear()
        ax.imshow(bw_matrix, cmap='gray')
        ax.set_title(title)
        ax.axis("off")
        canvas.draw()

        return bw_matrix

    def redraw_black_white():
        nonlocal matrix, ax, canvas

        win = tk.Toplevel(root)
        win.title("Black & White")

        tk.Label(win, text="border").pack()

        border_var = tk.StringVar(value="0.5")
        entry = tk.Entry(win, textvariable=border_var)
        entry.pack()

        original_matrix = matrix.copy()
        preview_matrix = original_matrix.copy()

        def preview(*args):
            nonlocal preview_matrix

            try:
                border = float(border_var.get())
            except ValueError:
                return

            preview_matrix = np.where(original_matrix < border, 0, 1)

            ax.clear()
            ax.imshow(preview_matrix, cmap='gray')
            ax.set_title(f"Black & White preview: {border}")
            ax.axis("off")
            canvas.draw()

        def generate():
            nonlocal matrix, preview_matrix

            matrix = preview_matrix.astype(int)
            redraw_matrix(ax, canvas, matrix, "Black & White")
            win.destroy()

        border_var.trace_add("write", preview)

        tk.Button(win, text="Generate", command=generate).pack()

        preview()

    def generate_white_noise():
        nonlocal matrix
        matrix = np.random.randint(0, 2, size=(100, 100))
        redraw_matrix(ax, canvas, matrix, "White Noise")

    
    def save_matrix_png():
        nonlocal matrix

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )

        if not file_path:
            return

        # нормализация (важно!)
        mat = np.array(matrix, dtype=float)
        min_val = mat.min()
        max_val = mat.max()

        if max_val - min_val != 0:
            mat = (mat - min_val) / (max_val - min_val)

        plt.imsave(file_path, mat, cmap='gray')

    # кнопки
    buttons = [
    ("White Noise", generate_white_noise),
    ("Perlin", open_perlin_window),
    ("Cellar", open_cellar_window),

    ("Diamond_Square", open_diamond_window),
    ("Simplex", open_simplex_window),
    ("redraw_block", redraw_blocked),

    ("redraw_black_white", redraw_black_white),
    ("Add Noise", add_noise),
    ("Apply Mask", apply_mask),
    ("Save PNG", save_matrix_png)
]

    for index, (text, command) in enumerate(buttons):
        row = index // 3 + 1
        col = index % 3

        ttk.Button(
            control_frame,
            text=text,
            command=command
        ).grid(row=row, column=col, padx=4, pady=4, sticky="ew")

    for col in range(3):
        control_frame.columnconfigure(col, weight=1)

    update_size_label()
    root.mainloop()


if __name__ == "__main__":
    main()