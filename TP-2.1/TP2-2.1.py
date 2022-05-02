import random as ran
from heapq import heapify, heapreplace
from socketserver import UDPServer
from statistics import mean, quantiles
import matplotlib.pyplot as plt
import numpy as np # importando numpy
import networkx as nx
from tabulate import tabulate
from prettytable import PrettyTable
import pandas as pd
from mpl_toolkits import mplot3d
import plotly.express as px

#===============================================================================================
#                         Funciones generadoras aleatoridad
#===============================================================================================
def rendom():
    n1 = ran.random()                               # Random float 0.0 <= x < 1.0
    return n1
def iuniform():
    n2 = ran.uniform(2.5, 10.0)                     # Random float 2.5 <= x <= 10.0
    return n2
def expo():
    n3 = ran.expovariate(1/5)                       # Intervalo entre llegadas con promedio de 5 segundos
    return n3
def ranrange():
    n4 = ran.randrange(10)                          # Integer de 0 a 9 inclusive
    return n4
def chois():
    n5 = ran.choice(['win', 'lose', 'draw'])        # Unico elemento aleatorio de una secuencia
    return n5
def barajarLista():
    deck = 'ace two three four'.split()             # barajar una lista 
    ran.shuffle(deck)
    n6 = deck
    return n6
def sampel(baraja):
    n7 = ran.sample(baraja, 3)      # 4 muestras sin reemplazo
    return n7
def init():
    n8 = ran.randint(1,10)                          # Entero aleatorio a <= x <= b
    return n8

#===============================================================================================
#                         Ejemplos de simulaciones usando aleatoridad
#===============================================================================================
def simulaciones():
# 6 giros de la rueda de la ruleta (muestreo ponderado con reemplazo)
    sim = ran.choices(['rojo', 'negro', 'verde'], [18, 18, 1], k=6)
    print(f"La muestra da {sim}")
# Repartir 20 cartas sin reemplazo de una baraja de 52 naipes, y determinar la proporción de naipes
# con un valor de diez: 10, sota, reina o rey.
    reparto = ran.sample(['dieces', 'cartas bajas'], counts=[16,36], k=20)
    c = reparto.count('dieces')/20
    print(f"Reparto {c}")
# Estimar la probabildiad de obtener 5 o más caras en 7 giros de una moneda sesgada que sale 'cara' el 60% de las veces
    def moneda():
        return ran.choices('HT', cum_weights=(0.60, 1.00), k=7).count('H') >= 5
    estimado = sum(moneda() for i in range(10_000)) / 10_000
    print(f"Probabilidad estimada: {estimado}")
# Probabilidad de que la mediana de 5 muestras esté en los dos cuartiles centrales
    def med():
        return 2_500 <= sorted(ran.choices(range(10_000), k=5))[2] < 7_500
    mediana = sum(med() for i in range(10_000)) / 10_000
    print(f"Probabilidad de la mediana: {mediana}")
# simulacion de tiempos de llegada y entrega de servicios para una cola de multiples servidores
    intervalo_llegada_promedio = 5.6
    promedio_servicio_tiempo = 15.0
    desvstand_tiempo_servicio = 3.5
    num_servidores = 3
    esperas = []
    tiempo_llegada = 0.0
    servidores = [0.0] * num_servidores     # tiempo en que cada servidor se vuelve disponible
    heapify(servidores)
    for i in range(1_000_000):
        tiempo_llegada += ran.expovariate(1.0 / intervalo_llegada_promedio)
        siguiente_server_disponible = servidores[0]
        espera = max(0.0, siguiente_server_disponible - tiempo_llegada)
        esperas.append(espera)
        duracion_servicio = max(0.0, ran.gauss(promedio_servicio_tiempo, desvstand_tiempo_servicio))
        servicio_completado = tiempo_llegada + espera + duracion_servicio
        heapreplace(servidores, servicio_completado)
    print(f"Espera: {mean(esperas):.1f} Maxima espera: {max(esperas):1f}")
    print("Cuartiles: ", [round(cu, 1) for cu in quantiles(esperas)])

#===============================================================================================
#                                    Algunas gráficas
#===============================================================================================
def graficas():
    eleccion_Grafica = ""
    x = []; y = []
    print("==============================================")
    print("             MENÚ DE GRÁFICAS                 ")
    print("==============================================")
    while eleccion_Grafica != "8":
        eleccion_Grafica = input("\n\t1. Random()\n\t2. Uniform()\n\t3. Randint()\n\t4. Lluvia con seed rand.\n\t5. Lluvia sin seed rand\n\t6. Lluvia con seed randint.\n\t7. Lluvia sin seed randint\n\t8. Salir\n\tElija: ")
        if eleccion_Grafica == "1":
            for i in range(1000):
                x.append(i+1)
                y.append(rendom())
                plt.scatter(x,y)
            plt.xlabel("Numero de tiradas")
            plt.ylabel("Resultado aleatorio")
            plt.title("Evaluacion de ran.random()")
            plt.show()
        elif eleccion_Grafica == "2":
            for i in range(1000):
                x.append(i+1)
                y.append(rendom())
                plt.scatter(x,y)
            plt.xlabel("Numero de tiradas")
            plt.ylabel("Resultado aleatorio")
            plt.title("Evaluacion de ran.uniform(1,10)")
            plt.show()
        elif eleccion_Grafica == "3":
            z = np.random.randint(100, size=300)
            x = np.random.randint(80, size=300)
            y = np.random.randint(60, size=300)
            fig = plt.figure(figsize=(10,7))
            ax = plt.axes(projection="3d")
            ax.scatter3D(x,y,z, color = "darkorange")
            ax.set_xlabel("X-axis")
            ax.set_ylabel("Y-axis")
            ax.set_zlabel("Z-axis")
            plt.title("Representación de 300 números utilizando randint")
            plt.show()
        elif eleccion_Grafica == "4":   
            for i in range(3):          #Pongo 3 para hacer 3 graficas: con seed son iguales, sin seed son distintas
                np.random.seed(42)
                arreglo = np.random.rand(512, 512)      #512 x 512 numeros
                plt.figure()
                plt.imshow(arreglo, cmap="gray")
                plt.show()
        elif eleccion_Grafica == "5":
            for i in range(3):
                arreglo = np.random.rand(512, 512)
                plt.figure()
                plt.imshow(arreglo, cmap="gray")
                plt.show()
        elif eleccion_Grafica == "6":
            for i in range(3):
                np.random.seed(42)
                arreglo = np.random.randint(0, 500, size=(512, 512))
                plt.figure()
                plt.imshow(arreglo, cmap="gray")
                plt.show()
        elif eleccion_Grafica == "7":
            for i in range(3):
                arreglo = np.random.randint(0, 500, size=(512, 512))
                plt.figure()
                plt.imshow(arreglo, cmap="gray")
                plt.show()
#graficas()

#===============================================================================================
#                        #Método de la parte media del cuadrado de Jon Von Neuman (Funca)
#===============================================================================================
def middleSquare():
    semilla = int(input("\n\tIngrese una semilla de 4 digitos: "))
    miTabla = PrettyTable(["Contador", "Cuadrado", "Nueva Semilla"])
    numero = semilla
    historial = []
    loop = []
    cont = 0
    eleccion_metodo = input("\n\t1. No cortar if semilla repetida.\n\t2. Cortar if semilla repetida\n\tElija: ")
    if eleccion_metodo == "1":
        eleccion_repeticiones = int(input("\n\tCuantas repeticiones?: "))
        for i in range(eleccion_repeticiones):
            cont += 1
            if numero in historial and numero not in loop:
                loop.append(numero)
            historial.append(numero)
            cuad = numero*numero
            numero = int(str(cuad).zfill(8)[2:6])      #zfill agrega relleno de ceros
            #print(f"#{cont}:\nvalor = '{cuad}', new seed = {numero}")
            miTabla.add_row([f"{cont}", f"{cuad}", f"{numero}"])
            plt.scatter(cont, numero)
        print(miTabla)
        print(f"\n\tEmpezamos con semilla = '{semilla}', hemos repetido el proceso '{cont}' veces, y el loop lo genera '{loop}'")
        plt.xlabel("Numero de repeticiones")
        plt.ylabel("Numeros medios obtenidos del cuadrado")
        plt.title("Representación gráfica de nuevas semillas")
        plt.show()
    if eleccion_metodo == "2":
        while numero not in historial:
            cont += 1
            historial.append(numero)
            cuad = numero*numero
            numero = int(str(cuad).zfill(8)[2:6])      #zfill agrega relleno de ceros
            #print(f"#{cont}:\nvalor = '{cuad}', new seed = {numero}")
            miTabla.add_row([f"{cont}", f"{cuad}", f"{numero}"])
            plt.scatter(cont, numero)
        print(miTabla)
        print(f"\n\tEmpezamos con semilla = '{semilla}', hemos repetido el proceso '{cont}' veces, hasta que '{numero} apareció de nuevo en la tabla'")
        plt.xlabel("Numero de repeticiones")
        plt.ylabel("Numeros medios obtenidos del cuadrado")
        plt.title("Representación gráfica de nuevas semillas")
        plt.show()
#middleSquare()

def randu():
    n = 150000
    x = [[],[]]; u = [[],[]]
    x[1] = 4798373
    u[1] = x[1] / (2^31 - 1)
    print(x)
    print(u)
    for i in range(n):
        x.append(((2 ^ 16 + 3) * x[i-1]) % (2 ^ 31))
        u.append(x[i] / (2 ^ 31))
        plt.plot(x,u)
    plt.show()
#randu()

#===============================================================================================
#                                           Análisis de Seed
#===============================================================================================
def comparacion():
    eleccion_comparacion = ""
    while eleccion_comparacion != "3":
        eleccion_comparacion = input("\n\t1. Con seed.\n\t2. Sin seed\n\t3. Salir\n\tElija: ")
        if eleccion_comparacion == "1":   
            for i in range(3): 
                np.random.seed(8)       #Es el punto inicial del algoritmo. Es pseudo porque no es totalmente random, sino que se puede controlar
                x = np.random.randint(1,7,size=10)    #genera un numero del 1 al 6, y genera 1000 numeros
                print(f"\n\tConjunto de valores: {x}")
                print(f"\tPromedio del conjunto de valores: {np.mean(x)}")
        if eleccion_comparacion == "2":
            for i in range(3):
                #al borrarle el "np.random.seed(8)" el resultado va a ser distinto
                x = np.random.randint(1,7,size=10)   
                print(f"\n\tConjunto de valores: {x}")
                print(f"\tPromedio del conjunto de valores: {np.mean(x)}")
#comparacion()

#===============================================================================================
#                                  Cuantos intentos hasta que aparezca...
#===============================================================================================
def howmany():
    numeros_unicos = []
    for i in range(1000):     #1000 porque es mas probable que no aparezca a que si, probar con numeros más grandes que 1000
        x = np.random.randint(1, 100000)
        if x in numeros_unicos:
            print(f"El numero '{x}' se repite en la corrida '{i}'")
        numeros_unicos.append(x)
#howmany()   #PARECE QUE TIRA ERROR pero es la gracia...lo importante es la Exception que devuelve al ejecutar esta funcion
#tableMiddleSquare()
