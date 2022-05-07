from cgi import test
from numpy.random import Generator, MT19937, SeedSequence
import time
import matplotlib.pyplot as plt
import random as ran
from prettytable import PrettyTable

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
#GCL()

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



 ## Metodo del gcl
def gclHiperPlano():  
    xn = int(time.time()) #Semilla   
    numerosGenerados = []
    for i in range(32000):
        xn1 = (1103515245 * xn + 12345) % 32768
        xn = xn1    #xn es la nueva semilla    
        if xn1 in numerosGenerados:
            print(f"Se repite en posición del for: '{i}' con valor: '{xn1}'")
            break
        numerosGenerados.append(xn1)
    return numerosGenerados

 ## Metodo del xorshift
def xorshiftHiperPlano():  
    x = 123456789
    y = 362436069
    z = 521288629
    w = 88675123
    numerosGenerados = []
    while w not in numerosGenerados:
        if w != 88675123:
            numerosGenerados.append(w)
        t = x ^ ((x << 11) & int(time.time()))  # aca siempre hay q poner la seed manualmente pq lo toma con un string
        x, y, z = y, z, w
        w = (w ^ (w >> 19)) ^ (t ^ (t >> 8))
    print(len(numerosGenerados))
    return numerosGenerados

## genera el HiperPlano
def plotHiperPlanoXorshift():
    z = xorshiftHiperPlano()
    x = xorshiftHiperPlano()
    y = xorshiftHiperPlano()
    fig = plt.figure(figsize=(10,7))
    ax = plt.axes(projection="3d")
    ax.scatter3D(x,y,z, color = "darkorange", s=1)
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Z-axis")
    plt.title("Hiperplano")
    plt.show()

#plotHiperPlanoXorshift()

def testComparacion():
    '''
        En estadística y análisis preliminar de datos, las pruebas de aleatoriedad (o test de aleatoriedad), son pruebas estadísticas usadas para decidir si una determinada muestra o conjuntos de datos responde a un patrón o puede considerarse aleatoria
        El período de un generador congruencial se define como la longitud de un ciclo y dado que la semilla depende del modulo,
            entonces el período máximo puede ser, a lo súmo, su módulo 'm'. En ese caso, el GCL tiene un periodo completo.
        Aunque pasa las pruebas de aleatoridad, es sensible a la eleccion de parametros m, a, c.
        No deberian ser usados en aplicaciuones para las que se requiera aleatoridad de alta calidad.
        Se puede ver que la secuencia obtenida no es tan aleatoria y no llena todo el espacio de manera uniforme. Los parámetros del método de congruencia lineal son importantes.
    '''
    cantNGen = []
    semilla = 1651
    semillaH = hex(semilla)
    print(semillaH)

## MiddleSquare
    historial = []
    numero = semilla
    cont = 0
    miTabla = PrettyTable(["Contador", "Cuadrado", "Nueva Semilla"])
    while numero not in historial:
        if numero != semilla:
            cont += 1
            historial.append(numero)
        cuad = numero*numero
        numero = int(str(cuad).zfill(8)[2:6])      #zfill agrega relleno de ceros
        miTabla.add_row([f"{cont}", f"{cuad}", f"{numero}"])
    #print(miTabla)
    print(f"En el MiddleSquare con la Semilla: {semilla} la cantidad de numeros generados es: {len(historial)}")
    cantNGen.append(len(historial))

##GCL // sea la semilla q sea siempre es hasta 32768, ese es el  numero que deberiamos modificar
    xn = semilla #Semilla
    numerosGenerados = []
    while xn not in numerosGenerados:
        if numero != semilla:
            numerosGenerados.append(xn)
        xn = (1103515245 * xn + 12345) % 32768
    print(f"En el CGL con la Semilla: {semilla} la cantidad de numeros generados es: {len(numerosGenerados)}")
    #cantNGen.append(len(numerosGenerados))

##Xorshift
    x = 123456789
    y = 362436069
    z = 521288629
    w = 88675123
    numerosGenerados = []
    while w not in numerosGenerados:
        if w != 88675123:
            numerosGenerados.append(w)
        t = x ^ ((x << 11) & 0x673)  # aca siempre hay q poner la seed manualmente pq lo toma con un string
        x, y, z = y, z, w
        w = (w ^ (w >> 19)) ^ (t ^ (t >> 8))
    print(f"En el xorshift con la Semilla: {semillaH} la cantidad de numeros generados es: {len(numerosGenerados)}")
    cantNGen.append(len(numerosGenerados))

# 3 barras
    #plt.bar([1,2,3], cantNGen)
    #plt.show()

# 2 barras
    plt.bar([1,3], cantNGen) ## hay q comentar la linea 224
    plt.show()

# Este metodo permite mostrar, mediante una grafica de barras, la cantidad de numeros generados por MGNPA.
# Suponemos que el 0x... es la semilla del metodo xorshift.
# En la grafica, se puede apreciar la gran cantidad de numeros generados por XOR a comparacion del resto, dependiendo la 
    # semilla que se de y el modulo. No es posible una completa comparación porque el MS utiliza como semilla 4 digitos,
    # el GLC utiliza el modulo (cosa que el resto), y eso hace variar la cant num generados, y no la semilla,
    # y en el XOR suponemos que la semilla es 0x...

# PONER EN LA CONCLUSION EL LINK DEL UNICO CODIGO QUE GENERA BITMAP XORSHIFT (C++): https://codingforspeed.com/using-faster-psudo-random-generator-xorshift/
testComparacion() 
