import flet as ft
import flet_charts as fch
import seaborn as sns
import sys
import numpy as np
import matplotlib.pyplot as plt

def main(page: ft.Page):
	page.title="hh"
	size=64
	field=np.random.random(size=(size,size))

	fig, ax =plt.subplots()
	im=ax.imshow(field,cmap='gray')

	
	page.add(fch.MatplotlibChart(figure=fig))

ft.run(main)