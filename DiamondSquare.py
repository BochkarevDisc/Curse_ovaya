import numpy as np


def diamond_square(n: int, seed=None, roughness=1.0):
    if seed is not None:
        np.random.seed(seed)

    size = 2 ** n + 1
    height_map = np.zeros((size, size))

    # Инициализация углов
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
                    height_map[y, x] +
                    height_map[y, x + step] +
                    height_map[y + step, x] +
                    height_map[y + step, x + step]
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
        scale *= 0.5  # уменьшение "шума"

    # нормализация (очень желательно)
    height_map -= height_map.min()
    height_map /= height_map.max()

    return height_map