import numpy as np
import math


class OpenSimplex:
    def __init__(self, seed=0):
        self.perm = np.arange(256, dtype=int)
        np.random.seed(seed)
        np.random.shuffle(self.perm)
        self.perm = np.concatenate([self.perm, self.perm])

        self.gradients = np.array([
            [1, 1], [-1, 1], [1, -1], [-1, -1],
            [1, 0], [-1, 0], [0, 1], [0, -1]
        ], dtype=float)

        # нормализация
        self.gradients /= np.linalg.norm(self.gradients, axis=1, keepdims=True)
        print(f"perm={self.perm}")
        print(f"grads={self.gradients}")

    def dot(self, g, x, y):
        return g[0] * x + g[1] * y

    def noise2d(self, x, y):
        # Skew
        F2 = 0.5 * (math.sqrt(3.0) - 1.0)
        s = (x + y) * F2
        i = math.floor(x + s)
        j = math.floor(y + s)
        print(f"skewed={i},{j}")
        # Unskew
        G2 = (3.0 - math.sqrt(3.0)) / 6.0
        print(f"F+g= {F2}  , {G2}")
        t = (i + j) * G2
        X0 = i - t
        Y0 = j - t

        x0 = x - X0
        y0 = y - Y0

        # Определяем треугольник
        if x0 > y0:
            i1, j1 = 1, 0
        else:
            i1, j1 = 0, 1

        x1 = x0 - i1 + G2
        y1 = y0 - j1 + G2
        x2 = x0 - 1 + 2 * G2
        y2 = y0 - 1 + 2 * G2

        ii = i & 255
        jj = j & 255

        gi0 = self.perm[ii + self.perm[jj]] % len(self.gradients)
        gi1 = self.perm[ii + i1 + self.perm[jj + j1]] % len(self.gradients)
        gi2 = self.perm[ii + 1 + self.perm[jj + 1]] % len(self.gradients)

        n0 = 0.0
        n1 = 0.0
        n2 = 0.0

        # вклад 1
        t0 = 0.5 - x0 * x0 - y0 * y0
        if t0 >= 0:
            t0 *= t0
            n0 = t0 * t0 * self.dot(self.gradients[gi0], x0, y0)

        # вклад 2
        t1 = 0.5 - x1 * x1 - y1 * y1
        if t1 >= 0:
            t1 *= t1
            n1 = t1 * t1 * self.dot(self.gradients[gi1], x1, y1)

        # вклад 3
        t2 = 0.5 - x2 * x2 - y2 * y2
        if t2 >= 0:
            t2 *= t2
            n2 = t2 * t2 * self.dot(self.gradients[gi2], x2, y2)

        # масштабирование
        return 70.0 * (n0 + n1 + n2)
    
def generate_open_simplex(size=100, scale=10, seed=0):
    noise = OpenSimplex(seed)

    lin = np.linspace(0, scale, size)
    x, y = np.meshgrid(lin, lin)

    result = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            result[i, j] = noise.noise2d(x[i, j], y[i, j])

    # нормализация
    result -= result.min()
    result /= result.max()

    return result