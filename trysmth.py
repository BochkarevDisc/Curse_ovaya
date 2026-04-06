import Perlin
import matplotlib.pyplot as plot
import numpy as np


data_size=4
lat_size=16
# генерация равномерно распределенных координат для функции perlin
lin_array = np.linspace(0, data_size, data_size*10, endpoint=False)
x, y = np.meshgrid(lin_array, lin_array)

print(x)
print(y[::-1])
# print(x*2)
# вывод графика pyplot

# Create a subplot
# fig1 = plot.figure()
# ax0, ax1, ax2 = fig1.subplots(1, 3)
# y=y[::-1]
seed=int(input("Enter seed:  "))

# np.random.seed(seed)
# ptable = np.arange(lat_size**2, dtype=int)
# # print(ptable)
# np.random.shuffle(ptable)
# ptable = np.stack([ptable, ptable]).flatten()
# print(ptable)

fig, axs = plot.subplots(2, 2, figsize=(10, 4))

aa0=Perlin.mult_perlin(x,y,seed=876876876,size=lat_size)
size0=aa0.shape
axs[0][0].imshow(aa0, origin="lower")
axs[0][0].set_title("Perlin x1")

aa1=Perlin.mult_perlin(x*2,y*2,seed=876876876,size=lat_size)
axs[0][1].imshow(aa1, origin="lower")
axs[0][1].set_title("Perlin x2")

aa1=Perlin.mult_perlin(x*4,y*4,seed=876876876,size=lat_size)
axs[1][0].imshow(aa1, origin="lower")
axs[1][0].set_title("Perlin x3")


aa2=aa0.flatten()+aa1.flatten()
aa2=aa2.reshape(data_size*10,data_size*10)


axs[1][1].imshow(aa2, origin="lower")
axs[1][1].set_title("Perlin together")

# plot.tight_layout()
plot.show()




