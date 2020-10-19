"""
---------------------------------------------------------------
linearAlgebra.py
Conjunto de algoritmos que se encargan de calcular operaciones
de álgebra lineal en mi render.
----------------------------------------------------------------
"""

pi = 3.141592653589793

def sumarVectores(v1, v2):
    suma = [v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]]
    return suma

def restarVectores(v1, v2):
    resta = [v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]]
    return resta

def multiplicarVectores(v1, v2):
    multiplicar = [v1[0] * v2[0], v1[1] * v2[1], v1[2] * v2[2]]
    return multiplicar

def dividirVectores(v1, v2):
    dividir = [v1[0] / v2[0], v1[1] / v2[1], v1[2] / v2[2]]
    return dividir

def dot(v0, v1):
    return ((v0[0] * v1[0]) + (v0[1] * v1[1]) + (v0[2] * v1[2]))
    
def cruz(v0, v1):
    cruz = [v0[1] * v1[2] - v1[1] * v0[2], -(v0[0] * v1[2] - v1[0] * v0[2]), v0[0] * v1[1] - v1[0] * v0[1]]
    return cruz

# Multiplicacion de un escalar con un vector de 3 elementos
def multiplicarPorEscalar(n, v):
    multiplicarEscalars = [n * v[0], n * v[1], n * v[2]]
    return multiplicarEscalars

def divVN(v, n):
    arrDiv = []
    arrDiv.extend((v[0] / n, v[1] / n, v[2] / n))
    return arrDiv

def norma(v0):
    return((v0[0]**2 + v0[1]**2 + v0[2]**2)**(1/2))

def normalizado(v):
    lon = norma(v)
    return [v[0]/lon , v[1]/lon , v[2]/lon]

def matrizVacia(r, c):
    m = []
    while len(m) < r:
        m.append([])
        while len(m[-1]) < c:
            m[-1].append(0.0)

    return m

def matrix_multiply(m1, m2):
    rowsM1 = len(m1)
    colsM1 = len(m1[0])
    colsM2 = len(m2[0])
    c = matrizVacia(rowsM1, colsM2)
    for i in range(rowsM1):
        for j in range(colsM2):
            total = 0
            for k in range(colsM1):
                total += m1[i][k] * m2[k][j]
            c[i][j] = total
    return c

def multiplicarVM(v, m):
    result = []
    for i in range(len(m)):
        total = 0
        for j in range(len(v)):
            total += m[i][j] * v[j]
        result.append(total)
    return result  

# Grados a radianes
def degToRad(number):
    return number * (pi/180)

# Funciones para la inversa 
def eliminate(r1, r2, col, target=0):
    fac = (r2[col]-target) / r1[col]
    for i in range(len(r2)):
        r2[i] -= fac * r1[i]

def gauss(a):
    for i in range(len(a)):
        if a[i][i] == 0:
            for j in range(i+1, len(a)):
                if a[i][j] != 0:
                    a[i], a[j] = a[j], a[i]
                    break
            else:
                return -1
        for j in range(i+1, len(a)):
            eliminate(a[i], a[j], i)
    for i in range(len(a)-1, -1, -1):
        for j in range(i-1, -1, -1):
            eliminate(a[i], a[j], i)
    for i in range(len(a)):
        eliminate(a[i], a[i], i, target=1)
    return a

def inverse(a):
    tmp = [[] for _ in a]
    for i,row in enumerate(a):
        assert len(row) == len(a)
        tmp[i].extend(row + [0]*i + [1] + [0]*(len(a)-i-1))
    gauss(tmp)
    ret = []
    for i in range(len(tmp)):
        ret.append(tmp[i][len(tmp[i])//2:])
    return ret

def baryCoords(Ax, Bx, Cx, Ay, By, Cy, Px, Py):
    try:
        u = ( ((By - Cy)*(Px - Cx) + (Cx - Bx)*(Py - Cy) ) /
              ((By - Cy)*(Ax - Cx) + (Cx - Bx)*(Ay - Cy)) )

        v = ( ((Cy - Ay)*(Px - Cx) + (Ax - Cx)*(Py - Cy) ) /
              ((By - Cy)*(Ax - Cx) + (Cx - Bx)*(Ay - Cy)) )

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w
