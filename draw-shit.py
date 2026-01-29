import seaborn as sns
import sys
import numpy as np
import matplotlib.pyplot as plt

size=64
field=np.random.random(size=(size,size))


sns.heatmap(field, cmap="gray")
plt.show()
