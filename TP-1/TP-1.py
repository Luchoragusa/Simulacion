import numpy as np 
import random as ran
import matplotlib.pyplot as plt

conjuntoValores = []
conjuntoValoresHi = []

def funcion(rep, corr): 
    for c in range(corr):
        valoresInt = []
        hi =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # arreglo de frecuencias relativas de cada numero de la ruleta
        for i in range(rep):
            nRandom = ran.randint (0,36)    # genera un numero aleatorio entre 0 y 36
            valoresInt.append(nRandom)      # agrega el numero aleatorio a un arreglo
            hi[nRandom] += 1                # aumenta la frecuencia relativa del numero aleatorio
        conjuntoValores.append(valoresInt)  # se le agrega a conjuntoValores los valores aleatorios de cada corrida
        conjuntoValoresHi.append(hi)        # aca se guardan los arreglos de cantidad de repeticion de un valor por corrida

def funcionProm(repeticiones, corridas, conjuntoValores):   # Grafica de los promedios
    for c in range(corridas):
        x = []; y= []
        suma=0
        valoresxCorrida = conjuntoValores[c]        
        for i in range(repeticiones):
            suma += valoresxCorrida[i]  # suma los valores de cada corrida
            x.append(i)             
            y.append(suma/(i+1))        # suma/(i+1) es el promedio de los valores de la corrida
        plt.plot(x,y)                   # grafica el promedio de los valores de la corrida
    plt.xlabel("Numero de tiradas")
    plt.ylabel("Promedio")
    plt.title("Evaluacion del promedio sobre el conjunto de valores aleatorios")
    plt.axhline(y=18, color = "r")  
    plt.ylim([12, 25]) # esta ponderada la medicion

def funcionPromProm(corridas, conjuntoValores): # Grafica del promedio de los promedios
    x = []; y= []
    for c in range(corridas):
        valoresxCorrida = conjuntoValores[c]
        x.append(c)
        y.append(np.mean(valoresxCorrida)) # esta funcion hace el promedio del arreglo de valores
        plt.plot(x,y, marker='o')
    plt.xlabel("Numero de tiradas")
    plt.ylabel("Promedio")
    plt.title("Evaluacion de la media aritmetica sobre el conjunto de valores aleatorios")
    plt.axhline(y=18, color = "black")  
    plt.grid() 
    plt.plot(x,y, color='r')

def funcionHi(repeticiones, corridas, conjuntoValoresHi):   # Grafica de las frecuencias relativas
    for c in range(corridas):
        x = []; y= []
        valoresxCorrida = conjuntoValoresHi[c]  
        for i in range(36):
            x.append(i)
            y.append(valoresxCorrida[i]/repeticiones) # divido la cantidad de veces que salio un numero por la cantidad de repeticiones de la corrida
        plt.bar(x,y, alpha=0.4) # grafica las frecuencias relativas de cada numero de la ruleta en cada corrida
    plt.xlabel("Numero de tiradas")
    plt.ylabel("Frecuencia Relativa")
    plt.title("Evaluacion de la frecuencia relativa sobre el conjunto de valores aleatorios")
    plt.axhline(y=0.027, color = "r")  
    plt.ylim([0.01, 0.0425]) # está ponderada

def funcionPuntos(repeticiones, corridas, conjuntoValores): # Grafica de las frecuencias relativas de puntos
    for c in range(corridas):
        x = []; y= []
        valoresxCorrida = conjuntoValores[c]
        for i in range(repeticiones):
            x.append(i)
            y.append(valoresxCorrida[i]) # grafica el numero que salio en cada tirada de la corrida para cada corrida
        plt.scatter(x,y)
    plt.xlabel("Numero de tiradas")
    plt.ylabel("Frecuencia Relativa")
    plt.title("Evaluacion de los resultados aleatorios sobre el conjunto de valores aleatorios")

def RuletaVarianza(tir, corr, conjuntoValores):
    for c in range(corr):
        y = []; x = []; valoresi = []   
        valoresxCorrida = conjuntoValores[c]    
        for i in range(tir):
            valoresi.append(valoresxCorrida[i])    
            x.append(i+1)  
            y.append(np.var(valoresi)) # esta funcion hace la varianza del arreglo de valores
        plt.plot(x, y)
    plt.xlabel("Numero probable")
    plt.ylabel("Resultados del tiro")   
    plt.axhline(y=114, color = "black")  
    plt.title("Evaluacion de la varianza sobre el conjunto de valores aleatorios")
    plt.ylim([70, 150]) # esta ponderada la medicion
    plt.show()

def RuletaDesvio(tir, corr, conjuntoValores):
    for c in range(corr):
        y = []; x = []; valoresi = []
        valoresxCorrida = conjuntoValores[c]
        for i in range(tir):
            valoresi.append(valoresxCorrida[i])
            x.append(i+1)  
            y.append(np.std(valoresi)) # esta funcion hace el desvio del arreglo de valores
        plt.plot(x, y)
    plt.xlabel("Numero probable")
    plt.ylabel("Resultados del tiro")   
    plt.axhline(y=np.sqrt(114), color = "black")    
    plt.title("Evaluacion del desvio estandar sobre el conjunto de valores aleatorios")
    plt.ylim([5, 16]) # esta ponderada la medicion
    plt.show()

#Inputs
rep = int(input("Ingrese la cantidad de TIRADAS que quiere ejecutar: "))
corr = int(input("Ingrese las CORRIDAS: "))

#Generar conjuntos de valores random 
funcion(rep, corr)

#Graficas
funcionProm(rep, corr, conjuntoValores)
plt.show()
funcionPromProm(corr, conjuntoValores)
plt.show()
funcionHi(rep, corr, conjuntoValoresHi)
plt.show()
funcionPuntos(rep, corr, conjuntoValores)
plt.show()
RuletaVarianza(rep, corr, conjuntoValores)
RuletaDesvio(rep, corr, conjuntoValores)