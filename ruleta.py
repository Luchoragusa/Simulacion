from cmath import sqrt
import numpy as np # importando numpy
import random
from turtle import color
import matplotlib.pyplot as plt 
from scipy import stats # importando scipy.stats

conjuntoValores = []
fig, ax = plt.subplots(1, 2)

def funcion(rep, corr):
    for c in range(corr):
        valoresInt = []
        suma=0
        hi =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(rep):
            nRandom = random.randint (0,36)
            valoresInt.append(nRandom)
            hi[nRandom] += 1
        conjuntoValores.append(valoresInt)
    return (conjuntoValores) 



def funcionProm(repeticiones, corridas, valoresProm):
    #Grafica de promedio de los promedios
    x = []
    y= []
    suma=0
    for i in range(corridas):
        suma += valoresProm[i]
        x.append(i)
        y.append(suma/(i+1))
    plt.plot(x,y, color='r', marker='o')
    x = [0, corridas-1]
    y = [18, 18]
    plt.plot(x,y, color='b')
    plt.xlabel("Nro de corrida")
    plt.ylabel("Promedio")
    plt.title("Simulacion ruleta")
    plt.grid(True)
    plt.yticks(np.arange(17,20))
    plt.show()

print("Ingrese la cantidad de repeticiones que quiere ejecutar: ", end=""); rep = int(input())
print("Ingrese la cantidad de corridas que quiere ejecutar: ", end=""); corr = int(input())

conjuntoValores= funcion(rep, corr)

funcionProm(rep, corr, conjuntoValores)
#funcionHi(rep)
#funcionDesvio(rep, valoresProm)
#funcionVarianza()
