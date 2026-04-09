import matplotlib.pyplot as plt
import numpy as np
import math as m
import DiamondSquare as Diam


field=Diam.diamond_square(10,23,1.5)


fig, axs = plt.subplots(2, 2, figsize=(10, 4))

axs[0][0].imshow(field, origin="lower", cmap='gray')
axs[0][0].set_title("state ")

#axs[0][1].imshow(field_1, origin="lower", cmap='gray')
#axs[0][1].set_title("neighbours x1")

#axs[1][0].imshow(field_8, origin="lower", cmap='gray')
#axs[1][0].set_title("new state x1")

#axs[1][1].imshow(field_3, origin="lower", cmap='gray')
#axs[1][1].set_title("after 100 gens x1")



plt.show()