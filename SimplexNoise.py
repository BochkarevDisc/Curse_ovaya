import numpy as np
import matplotlib.pyplot as plot
import math as m
import itertools


def generate_gradients(n: int):
    
    grads = []

    # выбираем 2 координаты, которые будут ненулевыми
    for axes in itertools.combinations(range(n), 2):
        for signs in itertools.product([-1, 1], repeat=2):
            vec = np.zeros(n)

            vec[axes[0]] = signs[0]
            vec[axes[1]] = signs[1]

            grads.append(vec)

    grads = np.array(grads, dtype=float)

    # нормализация
    norms = np.linalg.norm(grads, axis=1, keepdims=True)
    grads = grads / norms

    return grads


def get_1_vect(li):
    return [0 if i=="*" else i  and -1 if i=="0" else i   and 1 if i=="1" else i for i in li]

def gen_gradients(n=2):
    bins=[   (bin(i)[2:]).zfill(n-1) for i in range(pow(2,n-1))]
    print(bins)
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

def get_grad(perm, li):
    result = 0
    for val in reversed(li):
        result = perm[(int(val) + result) & 255]
    return result


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
    #print(f"F+g= {F}  , {G}")


    distances, skewed_point=get_distances(coords,F,G)

    #print(f"distances={distances}")
    #print(f"skewed={skewed_point}")
    
    order=np.argsort(distances)[::-1]
    vertices=[] #порядок обхода вершин
    vertices.append(np.zeros(len(distances)))

    starter=np.zeros((1,n),dtype=int)[0]
    for i in order:
        starter[i]=1
        vertices.append(  starter.copy()  )

    #print(f"vertices= {vertices}")
    
    corners=[] # действительно вершины симплекса
    corners.append(distances)
    for i in range(n):
        #print(distances)
        #print(vertices)
        smth=distances-vertices[i+1]+(i+1)*G
        corners.append(smth)

    #print(f"corners_my= {corners}")
    

    #print(f'{skewed_point}')
    skewed_point=[int(i) for i in skewed_point] #для корректности работы
    skewed_point=[ i & 255 for i in skewed_point ]

    new_vert=vertices+np.array(skewed_point)

    gradients=[]
    #print(new_vert)
    for item in new_vert:
        gi = get_grad(permutation, item) % len(grad)
        gradients.append(grad[gi])
        #gradients.append(grad[get_grad(permutation,item) % (n*pow(2,n-1))])

        

   # corners=[i[0] for i in corners]  #ubrat vloghennost
    #print(corners)
    res=[] #n0,n1,n2
    #print(f"gradients={gradients}")
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

def mult_Simplex_fast(x, y, permutation, grad):
    h, w = x.shape
    res = np.zeros((h, w))

    for i in range(h):
        for j in range(w):
            res[i, j] = SimplexNoise([x[i, j], y[i, j]], permutation, grad)

    return res

def build_permutation(seed=0):
    p = list(range(256))
    rng = np.random.default_rng(seed)
    rng.shuffle(p)
    return p * 2


def normalize_matrix(mat):
    mat = np.array(mat, dtype=float)
    min_val = mat.min()
    max_val = mat.max()

    if max_val - min_val == 0:
        return np.zeros_like(mat)

    return (mat - min_val) / (max_val - min_val)


def fractal_simplex(x, y, seed=0, n_dim=2, octaves=4, persistence=0.5, lacunarity=2.0):
    if n_dim != 2:
        raise ValueError("fractal_simplex(x, y, ...) сейчас реализован только для 2D-сетки.")

    grad = generate_gradients(n_dim)

    h, w = x.shape
    result = np.zeros((h, w), dtype=float)

    amplitude = 1.0
    frequency = 1.0
    amplitude_sum = 0.0

    for octave in range(octaves):
        perm = build_permutation(seed + octave)
        octave_noise = mult_Simplex_fast(x * frequency, y * frequency, perm, grad)

        result += octave_noise * amplitude
        amplitude_sum += amplitude

        frequency *= lacunarity
        amplitude *= persistence

    if amplitude_sum != 0:
        result /= amplitude_sum

    return normalize_matrix(result)