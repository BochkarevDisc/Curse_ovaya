import numpy as np


def normalize_matrix(mat):
    mat = np.array(mat, dtype=float)
    min_val = mat.min()
    max_val = mat.max()

    if max_val - min_val == 0:
        return np.zeros_like(mat)

    return (mat - min_val) / (max_val - min_val)


def resize_matrix(mat, new_shape):
    y_old, x_old = mat.shape
    y_new, x_new = new_shape

    y_idx = np.linspace(0, y_old - 1, y_new).astype(int)
    x_idx = np.linspace(0, x_old - 1, x_new).astype(int)

    return mat[np.ix_(y_idx, x_idx)]


def diamond_square(n: int, seed=None, roughness=1.0):
    if seed is not None:
        np.random.seed(seed)

    size = 2 ** n + 1
    height_map = np.zeros((size, size), dtype=float)

    height_map[0, 0] = np.random.rand()
    height_map[0, -1] = np.random.rand()
    height_map[-1, 0] = np.random.rand()
    height_map[-1, -1] = np.random.rand()

    step = size - 1
    scale = roughness

    while step > 1:
        half = step // 2

        for y in range(0, size - 1, step):
            for x in range(0, size - 1, step):
                avg = (
                    height_map[y, x]
                    + height_map[y, x + step]
                    + height_map[y + step, x]
                    + height_map[y + step, x + step]
                ) / 4.0

                offset = (np.random.rand() - 0.5) * scale
                height_map[y + half, x + half] = avg + offset

        for y in range(0, size, half):
            for x in range((y + half) % step, size, step):
                values = []

                if x - half >= 0:
                    values.append(height_map[y, x - half])
                if x + half < size:
                    values.append(height_map[y, x + half])
                if y - half >= 0:
                    values.append(height_map[y - half, x])
                if y + half < size:
                    values.append(height_map[y + half, x])

                avg = np.mean(values)
                offset = (np.random.rand() - 0.5) * scale
                height_map[y, x] = avg + offset

        step //= 2
        scale *= 0.5

    return normalize_matrix(height_map)


def fractal_diamond_square(n=8, seed=0, roughness=1.0, octaves=4, persistence=0.5, lacunarity=2.0):
    base_shape = (2 ** n + 1, 2 ** n + 1)
    result = np.zeros(base_shape, dtype=float)

    amplitude = 1.0
    frequency = 1.0
    amplitude_sum = 0.0

    for octave in range(octaves):
        octave_n = n + octave
        octave_roughness = roughness * amplitude

        octave_map = diamond_square(octave_n, seed + octave, octave_roughness)

        if octave_map.shape != base_shape:
            octave_map = resize_matrix(octave_map, base_shape)

        result += octave_map * amplitude
        amplitude_sum += amplitude

        frequency *= lacunarity
        amplitude *= persistence

    if amplitude_sum != 0:
        result /= amplitude_sum

    return normalize_matrix(result)