import numpy as np
import matplotlib.pyplot as plt
import SimplexNoise as Simplex
import random

grad=Simplex.gen_gradients(2)

p = list(range(256))
random.shuffle(p)
perm = p * 2

print(Simplex.SimplexNoise([4.55,6.07],perm,grad))

lin_array = np.linspace(0, 10, 10*10, endpoint=False)
x, y = np.meshgrid(lin_array, lin_array)

fig, axs = plt.subplots(2, 2, figsize=(10, 4))

aa0=Simplex.mult_Simplex(x,y,perm,grad)
aa1=np.array(aa0)
axs[0][0].imshow(aa1, origin="lower", cmap='gray')
axs[0][0].set_title("Simplex x1")

plt.show()
