import numpy as np

class BiomesType():
   LAND = 1
   SEA = 2
   SAND = 3
   SEA_SHORE = 4
   WOODS = 5

def create_start_matrix(rows,cols):
   matrix = np.random.randint(0,2, size=(rows,cols))
   return matrix

