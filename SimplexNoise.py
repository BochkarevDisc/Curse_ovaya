import numpy as np
import matplotlib.pyplot as plot
import math as m

def get_1_vect(li):
    return [0 if i=="*" else i  and -1 if i=="0" else i   and 1 if i=="1" else i for i in li]

def gen_gradients(n=2):
    bins=[   (bin(i)[2:]).zfill(n-1) for i in range(pow(2,n-1))]
    result=[]
    for item in bins:
        smth='*'+item
        result.append(smth)
    for i in range(1,n):
        for item in bins:
            smth=item[:i]+"*"+item[i:]
            result.append(smth)
    res=[get_1_vect(list(i)) for i in result]
    return res

def get_distances(point,F,G):
    n=len(point)
    s=np.sum(point)*F
    skewed_point=np.floor(point+s)
    t=np.sum(skewed_point)*G
    unskewed_point=skewed_point-t
    distances=point-unskewed_point
    return distances,skewed_point   ##x0,y0,i,j

def get_grad(perm,li):
    if len(li)==1:
        return perm[li[0]]
    else:
        return perm[li[0]+get_grad(perm,li[1:])]


def SimplexNoise(coords,permutation,grad):
    n=len(coords)
    result_factor=0
    match(n):
        case 2:
            result_factor=70          
        case 3:
            result_factor=32
        case 4:
            result_factor=27
        case _:
            result_factor=m.floor(33/2 * (n**2) - 241/2 * n +245)
    
    F=(m.sqrt(n+1)-1)/n
    G=(1-(1/m.sqrt(n+1)))/n

    distances, skewed_point=get_distances(coords,F,G)

    # print(distances)

    order=np.argsort(distances)[::-1]
    vertices=[] #порядок обхода вершин
    vertices.append(np.array([0,0]))

    starter=np.zeros((1,n),dtype=int)[0]
    for i in order:
        starter[i]=1
        vertices.append(  starter.copy()  )

    # print(f"vertices= {vertices}")
    
    corners=[] # действительно вершины симплекса
    corners.append(distances)
    for i in range(n):
        smth=distances-vertices[i]+(i+1)*G
        corners.append(smth)

  #  print(f"corners= {corners}")
    

    #print(f'{skewed_point}')
    skewed_point=[int(i) for i in skewed_point] #для корректности работы
    skewed_point=[ i & 255 for i in skewed_point ]

    new_vert=vertices+np.array(skewed_point)

    gradients=[]
    for item in new_vert:
        gradients.append(grad[get_grad(permutation,item) % (n*pow(2,n-1))])

        

   # corners=[i[0] for i in corners]  #ubrat vloghennost
    #print(corners)
    res=[] #n0,n1,n2

    for i in range(len(corners)):
        temp=0.5-np.sum(corners[i]**2)
        if temp <0:
            res.append(0.)
        else:
            temp *=temp
            vklad= temp**2 *(gradients[i] @ corners[i])
            res.append(vklad)
    
    return result_factor*np.sum(res)

def mult_Simplex(x,y,permutation,grad):
   res=np.array([])
   for xi,yi in zip(x.flatten(), y.flatten()):
      res=np.append(res, SimplexNoise([xi, yi], permutation,grad))

   sizeo=res.shape[0]
   # print(size)

   res=res.reshape(int(m.sqrt(sizeo)),int(m.sqrt(sizeo)))
   return res
   # print(res)