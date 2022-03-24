from cmath import sqrt
import numpy as np # importando numpy
import random
from turtle import color
import matplotlib.pyplot as plt
from scipy import stats # importando scipy.stats

valores = []
hi =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 

def funcion(rep, corr):
    for c in range(corr):
        valoresInt = []
        suma=0
        x = []
        y= []
        for i in range(rep):
            nRandom = random.randint (0,36)
            valoresInt.append(nRandom)
            suma += nRandom
            x.append(i+1)
            y.append(suma/(i+1))
        valores.append(np.mean(valoresInt))
        plt.plot(x,y)
    plt.xlabel("Nro probable")
    plt.ylabel("Resultado del tiro")
    plt.title("Simulacion ruleta")

    plt.show()
    return (valores) 


def funcionProm(corridas, valores):
    #Grafica de promedio de los promedios
    x = []
    y= []
    suma=0
    for i in range(corridas):
        suma += valores[i]
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

valores= funcion(rep, corr)

funcionProm(corr, valores)
#funcionHi(rep)
#funcionDesvio(rep, valores)
#funcionVarianza()
