import numpy as np
import math as m


def lerp(a, b, x):
    return a + x * (b - a)


def fade(f):
    return 6 * f ** 5 - 15 * f ** 4 + 10 * f ** 3


def gradient(c, x, y):
    vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    x_coff = vectors[c % 4][0]
    y_coff = vectors[c % 4][1]
    return x_coff * x + y_coff * y


def build_permutation(seed, size):
    np.random.seed(seed)
    ptable = np.arange(size ** 2, dtype=int)
    np.random.shuffle(ptable)
    return np.stack([ptable, ptable]).flatten()


def perlin_with_table(x, y, ptable, size):
    xi, yi = m.floor(x % size), m.floor(y % size)

    xg, yg = x - m.floor(x), y - m.floor(y)
    xf, yf = fade(xg), fade(yg)

    n00 = gradient(ptable[ptable[xi] + yi], xg, yg)
    n01 = gradient(ptable[ptable[xi] + yi + 1], xg, yg - 1)
    n11 = gradient(ptable[ptable[xi + 1] + yi + 1], xg - 1, yg - 1)
    n10 = gradient(ptable[ptable[xi + 1] + yi], xg - 1, yg)

    x1 = lerp(n00, n10, xf)
    x2 = lerp(n01, n11, xf)
    return lerp(x1, x2, yf)


def perlin(x, y, seed, size):
    ptable = build_permutation(seed, size)
    return perlin_with_table(x, y, ptable, size)


def mult_perlin(x, y, seed=0, size=16):
    ptable = build_permutation(seed, size)
    h, w = x.shape
    res = np.zeros((h, w))

    for i in range(h):
        for j in range(w):
            res[i, j] = perlin_with_table(x[i, j], y[i, j], ptable, size)

    return res


def normalize_matrix(mat):
    mat = np.array(mat, dtype=float)
    min_val = mat.min()
    max_val = mat.max()

    if max_val - min_val == 0:
        return np.zeros_like(mat)

    return (mat - min_val) / (max_val - min_val)


def fractal_perlin(x, y, seed=0, size=16, octaves=4, persistence=0.5, lacunarity=2.0):
    h, w = x.shape
    result = np.zeros((h, w), dtype=float)

    amplitude = 1.0
    frequency = 1.0
    amplitude_sum = 0.0

    for octave in range(octaves):
        octave_seed = seed + octave
        octave_size = max(2, int(round(size * frequency)))
        octave_noise = mult_perlin(x * frequency, y * frequency, seed=octave_seed, size=octave_size)

        result += octave_noise * amplitude
        amplitude_sum += amplitude

        frequency *= lacunarity
        amplitude *= persistence

    if amplitude_sum != 0:
        result /= amplitude_sum

    return normalize_matrix(result)