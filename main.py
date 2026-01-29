import flet as ft
import seaborn as sns
import sys
import numpy as np
import matplotlib.pyplot as plt

def main(page: ft.Page):
	page.title="hh"
	size=64
	field=np.random.random(size=(size,size))


	sns.heatmap(field, cmap="gray")
	smth=plt.show()
	page.add(ft.Image(src=smth))

ft.run(main)