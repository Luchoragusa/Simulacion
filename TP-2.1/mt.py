from numpy.random import Generator, MT19937, SeedSequence
import time
def ejemplo2():
    sg = SeedSequence(1234)
    bit_generator = MT19937(sg)
    rg = []
    coso = []
    for _ in range(10):
        rg.append(Generator(bit_generator))
        # Chain the BitGenerators
        bit_generator = bit_generator.jumped()
        coso.append(bit_generator)
    print(coso)

#estándar POSIX para C define a = 1103515245 y m = 32768 Con lo que a > m
def gcl():
    xn = int(time.time()) #Semilla
    for i in range(10):
        xn1 = (1103515245 * xn + 12345) % 32768
        print(xn1)
        xn = xn1
gcl()