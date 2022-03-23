from cmath import sqrt
import numpy as np # importando numpy
import random
from turtle import color
import matplotlib.pyplot as plt
from scipy import stats # importando scipy.stats

valores = []
hi =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def funcion(rep):
    valnRandomor=0
    for i in range(rep):
        nRandom = random.randint (0,36)
        valores.append(nRandom)
        hi[nRandom] += 1
    return (valores)


def funcionProm(rep, valores):
    #Grafica de promedios
    c=0; suma=0; i=0
    x = []
    y= []
    for i in range(rep):
        suma += valores[i]
        x.append(i+1)
        y.append(suma/(i+1))

    plt.plot(x,y, color='r')
    x = [0, rep]
    y = [18, 18]
    plt.plot(x,y, color='b')

    plt.xlabel("Nro de tiro")
    plt.ylabel("Resultado del tiro")
    plt.title("Simulacion ruleta")
    plt.show()

def funcionHi(rep):
    #Grafica de frec relativa
    i=0; x = []; y= []; y1= []; frA = 0
    for i in range(36):
        x.append(i)
        y.append(hi[i]/rep)

    plt.plot(x,y, color='r')
    plt.xlabel("Nro de tiro")
    plt.ylabel("Frecuencia Relativa")
    plt.title("Simulacion ruleta")
    plt.show()

def funcionDesvio(rep, valores):
    #Grafica del desvio estandar

    x = [0,36]
    y = [np.std(valores), np.std(valores)]


#    i=0; x1 = []; y1= []; sum = 0
#    for i in range(36):
#        x1.append(i)
#        sum += (abs(valores[i] - 18)**2)
#    print (np.std(valores))
#    print (sqrt(sum/rep))
#    y1 = [sqrt(sum/rep), sqrt(sum/rep)]
#    plt.plot(x,y1, color='b')

    plt.plot(x,y, color='r')

    plt.xlabel("Nro de tiro")
    plt.ylabel("Desvio estandar")
    plt.title("Simulacion ruleta")
    #plt.show()

def funcionVarianza():
    #Grafica de la varinza

    x = [0,36]
    y = [np.var(valores), np.var(valores)]

    plt.plot(x,y, color='r')

    plt.xlabel("Nro de tiro")
    plt.ylabel("Varianza")
    plt.title("Simulacion ruleta")
    plt.show()

print("Ingrese la cantidad de repeticiones que quiere ejecutar: ", end=""); rep = int(input())

valores= funcion(rep)
print("El promedio es: ", np.mean(valores))

#funcionProm(rep, valores)
#funcionHi(rep)
#funcionDesvio(rep, valores)
#funcionVarianza()