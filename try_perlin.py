import Perlin
import matplotlib.pyplot as plot
import numpy as np
import math as m

Perlin.perlin(2.34, 13.07, 0)
# print(Perlin.perlin(2.34, 13.07, 0))

# print(Perlin.perlin(120.13, 27.11, seed=3))


lin_array = np.linspace(1, 16, 160, endpoint=False)
x, y = np.meshgrid(lin_array, lin_array)

res=np.array([])
for xi,yi in zip(x.flatten(), y.flatten()):
    res=np.append(res,Perlin.perlin(xi, yi, 2))

size=res.shape[0]
print(size)

res=res.reshape(int(m.sqrt(size)),int(m.sqrt(size)))
print(res)