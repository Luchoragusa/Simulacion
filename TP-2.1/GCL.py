from numpy.random import Generator, MT19937, SeedSequence
import time

#Link de donde lo saqué: https://www.victoriglesias.net/algoritmo-de-generacion-de-numeros-pseudoaleatorios/
def gcl():
    xn = int(time.time()) #Semilla
    for i in range(10):
        xn1 = (1103515245 * xn + 12345) % 32768
        print(xn1)
        xn = xn1
gcl()