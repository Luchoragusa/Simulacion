from numpy.random import Generator, MT19937, SeedSequence
import time
import matplotlib.pyplot as plt

#===============================================================================================
#                                               GCL
#===============================================================================================
#Link de donde lo saqué: https://www.victoriglesias.net/algoritmo-de-generacion-de-numeros-pseudoaleatorios/
'''
    Se eligen cuatro números enteros: 
        - un modulo 'm'
        - un multiplicador 'a'
        - el incremento 'c'
        - la semilla 'x0'
    Estos numeros deben ser positivos mayores de 0. 
    Para 'a' se define = 1103515235 y m = 32768 segun POSIX,    [JUSTO CON ESE m, es lo que mayor cantidad de tiradas da]
        1. 1103515245 y 32768 son primos entre si.
        2. El único factor primo de 32768 es 2: 32768 = 215 y 1103515244 | 2 Además es eficiente al ser potencia de 2.
        3. Se cumple tanto 32768 | 4 como 1103515244 | 4
    Una semilla valida la pdoemos obtener del reloj interno de la CPU: el RTC.
    La formula es X(n+1) = (aXn + c) mod m

    Llegará un momento en que el resultado obtenido coincida con alguno de los resultados ya obtenidos. Cuando eso pase
        sabremos que la serie ha acabado y a continuacion se repetirán los mismos números. Por ejemplo con m=7, a=5, c=3 y x0=2
'''
def GCL():
    eleccion_Grafica = ""
    print("==============================================")
    print("             MENÚ DE GRAFICOS GCL's           ")
    print("==============================================")
    while eleccion_Grafica != "5":
        eleccion_Grafica = input("\n\t1. BARRAS\n\t2. SCATTER BUENO\n\t3. SCATTER MALO\n\t4. PLOT\n\t5. SALIR\n\tElija: ")
        if eleccion_Grafica == "1":
            ''' 
                EXPLICACION: un modulo grande no quiere decir muchos numeros aleatorios, no es directamente proporcional
                    sin embargo, con el valor de modulo en el que mas numeros aleatorios son generados, sin repeticion, es 32768.
                    y la cantidad de numeros generados es 32768.                  
            '''
            xn = int(time.time()) #Semilla
            cantNumA = []
            x=[]
            for j in range(100, 150):
                numerosGenerados = []
                x.append(j)
                for i in range(40000):
                    xn1 = (1103515245 * xn + 12345) % (j)
                    xn = xn1    #xn es la nueva semilla    
                    if xn1 in numerosGenerados:
                        break
                    numerosGenerados.append(xn1)
                print("Ya analizo el módulo: ", j)
                cantNumA.append(len(numerosGenerados))
            print(cantNumA)
            plt.bar(x, cantNumA)    #Grafica de barras
            plt.grid(True)
            plt.xlabel("Modulo")
            plt.ylabel("Cantidad de numeros generados")
            plt.title("Evaluacion de numeros generados de acuerdo al modulo")
            plt.show()
        elif eleccion_Grafica == "2":
            xn = int(time.time()) #Semilla
            numerosGenerados = []
            x = []; y = []
            for i in range(1000):
                xn1 = (1103515245 * xn + 12345) % 32768
                xn = xn1    #xn es la nueva semilla    
                if xn1 in numerosGenerados:
                    print(f"Se repite en posición del for: '{i}' con valor: '{xn1}'")
                    break
                numerosGenerados.append(xn1)
                x.append(i+1)
                y.append(xn1)
                plt.scatter(x,y)
            plt.xlabel("Numero de repeticiones")
            plt.ylabel("Numeros aleatorios generados")
            plt.title("Mapa de numeros aleatorios con GCL")
            plt.show()
        elif eleccion_Grafica == "3":
            xn = 5 #Semilla
            numerosGenerados = []
            x = []; y = []
            for i in range(1000):
                xn1 = (6 * xn + 7) % 23
                xn = xn1    #xn es la nueva semilla    
                if xn1 in numerosGenerados:
                    print(f"Se repite en posición del for: '{i}' con valor: '{xn1}'")
                    break
                numerosGenerados.append(xn1)
                x.append(i+1)
                y.append(xn1)
                plt.scatter(x,y)
            plt.xlabel("Numero de repeticiones")
            plt.ylabel("Numeros aleatorios generados")
            plt.title("Mapa de numeros aleatorios con GCL")
            plt.show()
        elif eleccion_Grafica == "4":
            xn = 165 #Semilla cualquiera
            numerosGenerados = []
            x = []; y = []
            for i in range(538):
                xn1 = (2 * xn + 0) % 199
                xn = xn1   
                numerosGenerados.append(xn1)
                x.append(i+1)
                y.append(xn1)
            plt.plot(x,y, marker='o')
            plt.xlabel("Numero de repeticiones")
            plt.ylabel("Numeros aleatorios generados")
            plt.title("Evaluacion de GCL")
            plt.show() #Link: https://demonstrations.wolfram.com/LinearCongruentialGenerators/
GCL()

#===============================================================================================
#                                            OTROS GCL
#===============================================================================================
def ingresarGCL():
    semilla = int(input("Ingrese la semilla: "))
    multiplicador = int(input("Ingrese el multiplicador (a): "))
    incremento = int(input("Ingrese el incremento (c): "))
    modulo = int(input("Ingrese el modulo (m): "))
    repeticiones = int(input("Cuantas numeros randoms quiere genera?: "))

    base = semilla
    arreglo = []
    arreglo_longitudes = []
    for j in range(10): 
        for i in range(repeticiones, 0, -1):
            rand = (multiplicador * base + incremento) % modulo
            arreglo.append(rand)
            arreglo_longitudes.append(j)
            base = rand
        print(arreglo)
        print(len(arreglo))
#ingresarGCL()

def decimalGCL():
    xn = int(time.time())
    for i in range(10):
        xn1 = ((1103515245 * xn + 12345) % 32768) / 32768.00    #los .00 son un "truco" para imprimir el resultado con decimales
        print(xn1)
        xn = xn1
#decimalGCL()