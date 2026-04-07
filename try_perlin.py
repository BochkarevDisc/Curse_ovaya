import Perlin
import matplotlib.pyplot as plt
import numpy as np
import math as m

#Perlin.perlin(2.34, 13.07, 0)
# print(Perlin.perlin(2.34, 13.07, 0))

# print(Perlin.perlin(120.13, 27.11, seed=3))


lin_array = np.linspace(1, 16, 160, endpoint=False)
x, y = np.meshgrid(lin_array, lin_array)

res=Perlin.mult_perlin(x,y,16,16)


fig, axs = plt.subplots(1, 1, figsize=(10, 4))



axs.imshow(res, origin="lower", cmap='gray')

plt.show()

""" for xi,yi in zip(x.flatten(), y.flatten()):
    res=np.append(res,Perlin.perlin(xi, yi, 2))

size=res.shape[0]
print(size)

res=res.reshape(int(m.sqrt(size)),int(m.sqrt(size)))
print(res) """