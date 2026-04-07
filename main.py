import flet as ft
import flet_charts as fch
import numpy as np
import matplotlib.pyplot as plt


import Perlin
import SimplexNoise


def generate_perlin(size, scale=10, seed=0):
    x = np.linspace(0, scale, size)
    y = np.linspace(0, scale, size)
    xv, yv = np.meshgrid(x, y)
    return Perlin.mult_perlin(xv, yv, seed=seed, size=size)


def generate_simplex(size, scale=10, seed=0):
    np.random.seed(seed)
    permutation = np.arange(256)
    np.random.shuffle(permutation)
    permutation = np.stack([permutation, permutation]).flatten()

    grad = SimplexNoise.gen_gradients(2)

    x = np.linspace(0, scale, size)
    y = np.linspace(0, scale, size)
    xv, yv = np.meshgrid(x, y)

    return SimplexNoise.mult_Simplex(xv, yv, permutation, grad)


def main(page: ft.Page):
    page.title = "Noise Generator"

    size = 128

    fig, ax = plt.subplots()

    def update_noise(noise_type):
        ax.clear()

        if noise_type == "perlin":
            field = generate_perlin(size)
        elif noise_type == "simplex":
            field = generate_simplex(size)
        else:
            field = np.random.random((size, size))

        ax.imshow(field, cmap='gray')
        ax.set_title(noise_type)
        fig.canvas.draw_idle()
        chart.update()

    chart = fch.MatplotlibChart(figure=fig)

    dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("random"),
            ft.dropdown.Option("perlin"),
            ft.dropdown.Option("simplex"),
        ],
        value="random",
        #on_change=lambda e: update_noise(e.control.value)
    )

    page.add(dropdown, chart)

    update_noise("random")


ft.run(main)
