import numpy as np
import matplotlib.pyplot as plt
import Cellar_automat as cell
import random

rows=100
cols=100

field=cell.create_start_matrix(rows,cols)
field_1=cell.generate_neighbours(field)
field_2=cell.next_generation_lands(field)
field_3=cell.next_generation_lands(field)

for i in range(400):
    field_3=cell.next_generation_lands(field_3)

fig, axs = plt.subplots(2, 2, figsize=(10, 4))

axs[0][0].imshow(field, origin="lower", cmap='gray')
axs[0][0].set_title("state ")

axs[0][1].imshow(field_1, origin="lower", cmap='gray')
axs[0][1].set_title("neighbours x1")

axs[1][0].imshow(field_2, origin="lower", cmap='gray')
axs[1][0].set_title("new state x1")

axs[1][1].imshow(field_3, origin="lower", cmap='gray')
axs[1][1].set_title("after 100 gens x1")

gg=cell.next_generation_lands(field)

plt.show()