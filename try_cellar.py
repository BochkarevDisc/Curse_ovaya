import numpy as np
import matplotlib.pyplot as plt
import Cellar_automat as cell
import random

rows=300
cols=300

field=cell.create_start_matrix(rows,cols)

fig, axs = plt.subplots(1, 1, figsize=(10, 4))

axs.imshow(field, origin="lower", cmap='gray')
axs.set_title("Simplex x1")

plt.show()