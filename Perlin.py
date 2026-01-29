import numpy as np
import matplotlib.pyplot as plot
import math as m

def perlin(x, y, seed=0): # для одного числа
   # создание матрицы для шума и генерация случайного значения seed

   np.random.seed(seed)
   ptable = np.arange(256, dtype=int)
   print(ptable)
   np.random.shuffle(ptable)
   ptable = np.stack([ptable, ptable]).flatten()
   print(ptable)

   # для бесконечной сетки
  
   # целые числа
   xi, yi = m.floor(x%16), m.floor(y%16)

   # локальные координаты
   xg, yg = x-m.floor(x), y - m.floor(x)

   # применение функции затухания к координатам расстояний
   xf, yf = fade(xg), fade(yg)

    # вычисление градиентов в заданных интервалах
   print(ptable[ptable[xi] + yi])
   n00 = gradient(ptable[ptable[xi] + yi], xg, yg)
   n01 = gradient(ptable[ptable[xi] + yi + 1], xg, yg - 1)
   n11 = gradient(ptable[ptable[xi + 1] + yi + 1], xg - 1, yg - 1)
   n10 = gradient(ptable[ptable[xi + 1] + yi], xg - 1, yg)

   # линейная интерполяция градиентов n00, n01, n11, n10
   x1 = lerp(n00, n10, xf)
   x2 = lerp(n01, n11, xf)
   return lerp(x1, x2, yf)

def lerp(a, b, x):
   "функция линейной интерполяции"
   return a + x * (b - a)

# функция сглаживания
def fade(f):
   return 6 * f ** 5 - 15 * f ** 4 + 10 * f ** 3

# вычисление векторов градиента 
def gradient(c, x, y):
   vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
   x_coff=vectors[c % 4][0]
   y_coff = vectors[c % 4][1]
   return  x_coff*x+y_coff*y





#def FractalPerlin(x,y,seed=0, octaves=1, amplitude=1,):
  # res=0
  # maxamp=0
  # for i in range(octaves):
  #    curr_gen=perlin(x*,y)
      