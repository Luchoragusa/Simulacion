import random
from turtle import color
import matplotlib.pyplot as plt

x = []
y= []

def funcion(rep):
    c=0; suma=0; i=0
    for i in range(rep):
        suma = suma + random.randint (0,36)
        c +=1
        x.append(c)
        y.append(suma/c)
    return (suma/rep)

print("Ingrese la cantidad de repeticiones que quiere ejecutar: ", end=""); rep = int(input())

print("El promedio es: ", funcion(rep))

plt.plot(x,y, color='b')
plt.xlabel("Nro de tiro")
plt.ylabel("Resultado del tiro")
plt.title("Simulacion ruleta")

plt.savefig('grafico.png')

plt.show()