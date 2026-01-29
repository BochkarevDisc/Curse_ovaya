import Perlin
import matplotlib.pyplot as plot
import numpy as np

# генерация равномерно распределенных координат для функции perlin
lin_array = np.linspace(1, 16, 160, endpoint=False)
x, y = np.meshgrid(lin_array, lin_array)

print(x)

print(x*2)
# вывод графика pyplot

# Create a subplot
# fig1 = plot.figure()
# ax0, ax1, ax2 = fig1.subplots(1, 3)
seed=int(input("Enter seed:  "))

# ax0.plot(plot.imshow(Perlin.perlin(x, y, seed=seed), origin='upper'))
# ax0.set_title('normal')

# ax0.plot.imshow(Perlin.perlin(x, y, seed=seed), origin='upper')
# ax0.set_title('double Freq')

# ax0.plot.imshow(Perlin.perlin(x, y, seed=seed), origin='upper')
# ax0.set_title('quadra Freq')



fig, axs = plot.subplots(1, 3, figsize=(10, 4))

aa0=np.array(Perlin.perlin(x, y, seed=seed))
size0=aa0.shape
axs[0].imshow(aa0, origin="upper")
axs[0].set_title("Perlin x1")

aa1=np.array(Perlin.perlin(x * 2, y * 2, seed=seed))
axs[1].imshow(aa1, origin="upper")
axs[1].set_title("Perlin x2")

aa2=((aa0.flatten()+aa1.flatten())/2).reshape((160,160))
print(aa2)
axs[1].imshow(aa2, origin="upper")
axs[1].set_title("Perlin x3")

# plot.tight_layout()
plot.show()

print(120.13%16)

print(Perlin.perlin(120.13, 27.11, seed=3))
