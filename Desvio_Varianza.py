import random as ran
import statistics
from turtle import color
import numpy as np
import matplotlib.pyplot as plt
from statistics import fmean

def RuletaDesvio(tir, corr):
    for c in range(corr):
        rtdosAleatorios = []
        y = []
        x = []
        for i in range(tir):
            nRandom = ran.randint (0,36)
            rtdosAleatorios.append(nRandom)
            x.append(i+1)
            y.append(np.std(rtdosAleatorios))
        plt.plot(x, y)
    plt.xlabel("Numero probable")
    plt.ylabel("Resultados del tiro")   
    plt.axhline(y=np.sqrt(114), color = "black")  
    plt.title("Resultados probables del conjunto de valores sobre el desvio estandar")

    plt.show()

def RuletaVarianza(tir, corr):
    for c in range(corr):
        rtdosAleatorios = []
        y = []
        x = []
        for i in range(tir):
            nRandom = ran.randint (0,36)
            rtdosAleatorios.append(nRandom)
            x.append(i+1)
            y.append(np.var(rtdosAleatorios))
        plt.plot(x, y)
    plt.xlabel("Numero probable")
    plt.ylabel("Resultados del tiro")   
    plt.axhline(y=114, color = "black")  
    plt.title("Resultados probables del conjunto de valores sobre el desvio estandar")

    plt.show()

#Inputs
tiradas = int(input("Ingrese la cantidad de tiradas: "))
corridas = int(input("Ingrese corridas: "))

#Graficas
RuletaVarianza(tiradas, corridas)
RuletaDesvio(tiradas, corridas)