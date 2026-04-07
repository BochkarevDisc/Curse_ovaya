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

def generate_neighbours(matrix):


   next_matrix_count = (
      np.roll(matrix, -1, axis=0) +
      np.roll(matrix,  1, axis=0) +
      np.roll(matrix, -1, axis=1) +
      np.roll(matrix,  1, axis=1) +
      np.roll(np.roll(matrix, -1, axis=0), -1, axis=1) +
      np.roll(np.roll(matrix, -1, axis=0),  1, axis=1) +
      np.roll(np.roll(matrix,  1, axis=0), -1, axis=1) +
      np.roll(np.roll(matrix,  1, axis=0),  1, axis=1)
   )
   return next_matrix_count

def next_generation_lands(matrix):


   next_matrix_count = (
      np.roll(matrix, -1, axis=0) +
      np.roll(matrix,  1, axis=0) +
      np.roll(matrix, -1, axis=1) +
      np.roll(matrix,  1, axis=1) +
      np.roll(np.roll(matrix, -1, axis=0), -1, axis=1) +
      np.roll(np.roll(matrix, -1, axis=0),  1, axis=1) +
      np.roll(np.roll(matrix,  1, axis=0), -1, axis=1) +
      np.roll(np.roll(matrix,  1, axis=0),  1, axis=1)
   )

   new_state=np.zeros(matrix.shape)

   for i in range(next_matrix_count.shape[0]):
      for j in range(next_matrix_count.shape[1]):
         #print(f"({i},{j})")
         new_state[i][j]= 1 if ((matrix[i][j]==0 and next_matrix_count[i][j] in [3,6,7,8]) or (matrix[i][j]==1 and next_matrix_count[i][j] in [3,4,6,7,8])) else 0

   return new_state