import random as ran
import statistics
from turtle import color
import numpy as np
import matplotlib.pyplot as plt
from statistics import fmean

def Ruleta(tiradas):
    rtdosAleatorios = []
    promedio = []
    varianzaTirada = []
    desvioTirada = []

    for i in range(1, tiradas+1):
        rtdosAleatorios.append(ran.randint(0, 36))
        promedio.append(statistics).fmean(rtdosAleatorios)
        varianzaTirada.append(np.var(rtdosAleatorios))
        desvioTirada.append(np.std(rtdosAleatorios))
    
    return varianzaTirada, desvioTirada


#Inputs
tiradas = int(input("Ingrese la cantidad de tiradas: "))
corrida = int(input("Ingrese corridas: "))

#Para graficar en una misma 8 veces
#Link de ayuda: https://www.delftstack.com/es/howto/matplotlib/plot-multiple-lines-matplotlib/

fig, ax = plt.subplots(nrows=1, ncols=2)

for i in range(0, corrida):
    giro = Ruleta(tiradas)
    ax[0,0].plot(giro[0])

plt.plot()