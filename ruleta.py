from cmath import sqrt
import numpy as np # importando numpy
import random
from turtle import color
import matplotlib.pyplot as plt
from pyparsing import col 
from scipy import stats # importando scipy.stats

conjuntoValores = []
conjuntoValoresHi = []

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
        conjuntoValoresHi.append(hi)



def funcionProm(repeticiones, corridas, conjuntoValores):
    #Grafica de los promedios
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
    plt.ylim([12, 25]) # esta ponderada la medicion

def funcionPromProm(corridas, conjuntoValores):
    #Grafica del promedio de los promedios
    x = []; y= []
    for c in range(corridas):
        valoresxCorrida = conjuntoValores[c]
        x.append(c)
        y.append(np.mean(valoresxCorrida))
        plt.plot(x,y, marker='o')
    plt.xlabel("Numero de tiradas")
    plt.ylabel("Promedio")
    plt.title("Evaluacion del promedio sobre el conjunto de valores aleatorios")
    x = [0, corridas-1]
    y = [18, 18]
    plt.grid()
    plt.plot(x,y, color='r')

def funcionHi(repeticiones, corridas, conjuntoValoresHi):
    #Grafica de las frec relativas
    for c in range(corridas):
        x = []; y= []
        valoresxCorrida = conjuntoValoresHi[c]
        for i in range(36):
            x.append(i)
            y.append(valoresxCorrida[i]/repeticiones)
        plt.bar(x,y, alpha=0.4)
    plt.xlabel("Numero de tiradas")
    plt.ylabel("Frecuencia Relativa")
    plt.title("Evaluacion de la frecuencia relativa sobre el conjunto de valores aleatorios")
    x = [-1, 36]
    y = [0.027, 0.027]
    plt.ylim([0.01, 0.0425]) # esta ponderada
    plt.plot(x,y, color = 'r')

def funcionPuntos(repeticiones, corridas, conjuntoValores):
    #Grafica de las frec relativas
    for c in range(corridas):
        x = []; y= []
        valoresxCorrida = conjuntoValores[c]
        for i in range(repeticiones):
            x.append(i)
            y.append(valoresxCorrida[i])
        plt.scatter(x,y)
    plt.xlabel("Numero de tiradas")
    plt.ylabel("Frecuencia Relativa")
    plt.title("Evaluacion de la frecuencia relativa sobre el conjunto de valores aleatorios")

#Main

print("Ingrese la cantidad de repeticiones que quiere ejecutar: ", end=""); rep = int(input())
print("Ingrese la cantidad de corridas que quiere ejecutar: ", end=""); corr = int(input())

funcion(rep, corr)

funcionProm(rep, corr, conjuntoValores)
plt.show()
funcionPromProm(corr, conjuntoValores)
plt.show()
funcionHi(rep, corr, conjuntoValoresHi)
plt.show()
funcionPuntos(rep, corr, conjuntoValores)
plt.show()


#funcionDesvio(rep, valoresProm)
#funcionVarianza()