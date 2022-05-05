from numpy.random import Generator, MT19937, SeedSequence
import time

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
def primerGCL():
    xn = int(time.time()) #Semilla
    numerosGenerados = []
    for i in range(40000):
        xn1 = (1103515245 * xn + 12345) % 32768
        xn = xn1    #xn es la nueva semilla    
        if xn1 in numerosGenerados:
            print(f"Se repite en posición del for: '{i}' con valor: '{xn1}'")
            break
        numerosGenerados.append(xn1)
primerGCL()

def segundoGCL():
    xn = int(time.time())
    total = []
    repetido = False
    while (not repetido):
        xn1 = (1103515245 * xn + 12345) % 32768
        xn = xn1 
        repetido = xn1 in total
        if (not repetido):
            total.append(xn1)
    print(total)
    print(len(total))
#segundoGCL()

def decimalGCL():
    xn = int(time.time())
    for i in range(10):
        xn1 = ((1103515245 * xn + 12345) % 32768) / 32768.00    #los .00 son un "truco" para imprimir el resultado con decimales
        print(xn1)
        xn = xn1
#decimalGCL()

#===============================================================================================
#                                            OTRO GCL
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