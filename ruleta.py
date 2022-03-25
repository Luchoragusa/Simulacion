from cmath import sqrt
import numpy as np # importando numpy
import random
from turtle import color
import matplotlib.pyplot as plt
from pyparsing import col 
from scipy import stats # importando scipy.stats

conjuntoValores = []

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



def funcionProm(repeticiones, corridas, conjuntoValores):
    #Grafica de promedio de los promedios
    for c in range(corridas):
        x = []; y= []
        suma=0
        valoresxCorrida = conjuntoValores[c]
        for i in range(repeticiones):
            suma += valoresxCorrida[i]
            x.append(i)
            y.append(suma/(i+1))
        plt.plot(x,y)
    plt.xlabel("Numero de tiradas")
    plt.ylabel("Promedio")
    plt.title("Evaluacion del promedio sobre el conjunto de valores aleatorios")
    x = [-1, rep]
    y = [18, 18]
    plt.plot(x,y, color = 'r')

#Main

print("Ingrese la cantidad de repeticiones que quiere ejecutar: ", end=""); rep = int(input())
print("Ingrese la cantidad de corridas que quiere ejecutar: ", end=""); corr = int(input())

conjuntoValores= funcion(rep, corr)

funcionProm(rep, corr, conjuntoValores)
#funcionHi(rep)
#funcionDesvio(rep, valoresProm)
#funcionVarianza()

plt.show()