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

def graficas():
    eleccion_Grafica = ""
    x = []; y = []
    print("==============================================")
    print("============ MENÚ DE GRÁFICAS ================")
    print("==============================================")
    while eleccion_Grafica != "5":
        eleccion_Grafica = input("\n\t1. Random()\n\t2. Uniform()\n\t3. Randint()\n\t4. Salir\n\tElija: ")
        if eleccion_Grafica == "1":
            for i in range(300):
                x.append(i+1)
                y.append(rendom())
                plt.scatter(x,y)
            plt.xlabel("Numero de tiradas")
            plt.ylabel("Resultado aleatorio")
            plt.title("Evaluacion de ran.random()")
            plt.show()
        elif eleccion_Grafica == "2":
            for i in range(300):
                x.append(i+1)
                y.append(rendom())
                plt.scatter(x,y)
            plt.xlabel("Numero de tiradas")
            plt.ylabel("Resultado aleatorio")
            plt.title("Evaluacion de ran.uniform(1,10)")
            plt.show()
        elif eleccion_Grafica == "3":
            z = np.random.randint(100, size=200)
            x = np.random.randint(80, size=200)
            y = np.random.randint(60, size=200)
            fig = plt.figure(figsize=(10,7))
            ax = plt.axes(projection="3d")
            ax.scatter3D(x,y,z, color = "darkorange")
            ax.set_xlabel("X-axis")
            ax.set_ylabel("Y-axis")
            ax.set_zlabel("Z-axis")
            plt.title("Representación de 100 números utilizando randint")
            plt.show()
graficas()

#Método de la parte media del cuadrado de Jon Von Neuman
def middleSquare():
    semilla = int(input("\n\tIngrese una semilla de 4 digitos: "))
    miTabla = PrettyTable(["Contador", "Nueva Semilla", "Valor"])
    numero = semilla
    historial = []
    loop = []
    cont = 0
    eleccion_metodo = input("\n\t1. Aparezca semilla repetida.\n\t2. No aparezca semilla repetida\n\tElija: ")
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
            miTabla.add_row([f"{cont}", f"{numero}", f"{cuad}"])
            plt.scatter(cont, numero)
        print(miTabla)
        print(f"\n\tEmpezamos con semilla = '{semilla}', hemos repetido el proceso '{cont}' veces, y el loop lo genera '{apariciones}'")
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

#Mismo método de la parte media pero ploteado para que aparezca la gráfica
def tableMiddleSquare():
    fig, ax =plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    column_labels=["Contador", "Valor", "Nueva Semilla"]
    data = []
    semilla = int(input("Ingrese una semilla de 4 digitos: "))
    numero = semilla
    historial = []
    cont = 0
    while numero not in historial:
        cont += 1
        historial.append(numero)
        cuad = numero*numero
        numero = int(str(cuad).zfill(8)[2:6])      #zfill agrega relleno de ceros
        #print(f"#{cont}:\nvalor = '{cuad}', new seed = {numero}")
        data = [[cont, cuad, numero],
                [cont, cuad, numero],
                [cont, cuad, numero]]
        df=pd.DataFrame(data,columns=column_labels)
        ax.axis('tight')
        ax.axis('off')
    ax.table(cellText=df.values,
            colLabels=df.columns,
            rowLabels=["A","B","C"],
            rowColours =["yellow"] * 3,  
            colColours =["yellow"] * 3,
            loc="center")
    plt.show()
#tableMiddleSquare()

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