import numpy as np

def to_base(num,base):
        res=[]
        while num>0:
            temp=num//base
            digit=num%base
            res+=[digit]
            num=temp
        return res[::-1]

def to_base_v2(num,base,lenzz):
        res=[]
        while num>0:
            temp=num//base
            digit=num%base
            res+=[digit]
            num=temp
        return [0]*(lenzz-len(res))+res[::-1]

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

def generate_neighbours_v2(matrix,mode,distance):
   res=np.zeros(matrix.shape)
   if mode==1: ## Mura
      # vsego sosedey=(1+2*distance)^2-1
      print(((1+distance*2)**2))
      for i in range((1+distance*2)**2):
         gena=np.array(to_base_v2(i,1+2*distance,2))
         print(f"first gen=  {gena}")
         gena=gena-np.full(gena.shape,distance)
         print(f"second gen=  {gena}")
         res=res+np.roll(np.roll(matrix,gena[0],axis=0),gena[1],axis=1)

      return res-matrix

   if mode==2: ## Fon
      # vsego sosedey=2*(distance+1)*distance
      print(((1+distance*2)**2))
      for i in range((1+distance*2)**2):
         gena=np.array(to_base_v2(i,1+2*distance,2))
         print(f"first gen=  {gena}")
         
         gena=gena-np.full(gena.shape,distance)
         print(f"second gen=  {gena}")
         flag=np.abs(gena).sum()
         print(f"flag={flag}")
         if flag > distance:
             continue
         res=res+np.roll(np.roll(matrix,gena[0],axis=0),gena[1],axis=1)

      return res-matrix



def next_generation_lands_v2(matrix,mode,distance,rule):
   b_rule,s_rule=rule.split('/')
   b_rule=b_rule.split('.')[1:]
   s_rule=s_rule.split('.')[1:]
   b_rule=[int(z) for z in b_rule]
   s_rule=[int(z) for z in s_rule]

   next_matrix_count=generate_neighbours_v2(matrix,mode,distance)
   new_state=np.zeros(matrix.shape)
   for i in range(next_matrix_count.shape[0]):
      for j in range(next_matrix_count.shape[1]):
         #print(f"({i},{j})")
         new_state[i][j]= 1 if ((matrix[i][j]==0 and next_matrix_count[i][j] in b_rule) or (matrix[i][j]==1 and next_matrix_count[i][j] in s_rule)) else 0

   return new_state
   


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