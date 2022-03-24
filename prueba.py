from cmath import sqrt
import random as ran
from turtle import color
import numpy as np
import matplotlib.pyplot as plt
import statistics 
from statistics import fmean

min = 0
max = 36
""" giros = 5000
X = 8 """

def girarRuleta(num_giros, X):
    resultados = []
    promX = []
    cont = 0
    fr = []
    varXtirada = []
    desvioXtirada = []
    
    for i in range(1,num_giros+1):
        resultados.append(float(ran.randint(min,max)))
        if (resultados[i-1] == X):
            cont+=1
        fr.append((cont/i))
        promX.append(statistics.fmean(resultados))

        varXtirada.append(np.var(resultados))
        desvioXtirada.append(np.std(resultados))
    return promX, fr, varXtirada, desvioXtirada

fig, ax = plt.subplots(nrows=2, ncols=2)

sim = int(input('Ingresar cantidad de simulaciones: '))
giros = int(input('Ingresar cantidad de tiradas: '))
X = int(input('Ingresar número a evaluar: '))

for i in range(0,sim):
    tirada = girarRuleta(giros, X)
    ax[0,0].plot(tirada[0])
    ax[0,1].plot(tirada[1])
    ax[1,0].plot(tirada[2])
    ax[1,1].plot(tirada[3])

ax[0,0].axhline(y=18, color='black')
ax[0,1].axhline(y=1/37, color='black')
ax[1,0].axhline(y=114, color='black')
ax[1,1].axhline(y=np.sqrt(114), color='black')
ax[0,0].set_ylim(0, 37)
ax[0,0].set_yticks(range(0,37,4))
ax[0,0].set_xlabel("Tiradas")
ax[0,0].set_ylabel("Media")
ax[0,1].set_xlabel("Tiradas")
ax[0,1].set_ylabel("Frecuencia relativa")
ax[1,0].set_xlabel("Tiradas")
ax[1,0].set_ylabel("Varianza matemática")
ax[1,1].set_xlabel("Tiradas")
ax[1,1].set_ylabel("Desvío estándar")
plt.show()