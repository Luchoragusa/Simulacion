import random as ran
from math import log,exp
import matplotlib.pyplot as plt
from functools import partial
from typing import Callable
import numpy

## Generadores de numeros aleatorios nuestros

def uniforme(a,b):
    r=ran.random()
    x=a+(b-a)*r
    return x

def exponencial(alfa):
    r=ran.random()
    x=-alfa*log(r)
    return x

def gamma(k,alfa):
    tr=0.1
    for i in range(k):
        r=ran.random()
        tr=tr*r
    x=-log(tr)/alfa
    return x

def normal(ex,stdx):
    sum=0.0
    for i in range(12):
        r=ran.random()
        sum=sum+r
    x=stdx*(sum-6.0)+ex
    return x

def pascal(k,q):
    tr=1.0
    qr=log(q)
    for i in range(k):
        r=ran.random()
        tr=tr*r
    nx=log(tr)/qr
    return nx

def binomial(n,p):
    x=0.0
    for i in range(n):
        r=ran.random()
        if (r<p):
            x=x+1.0
    return x

def hipergeometrica(tn,ns,p):
    x=0.0
    for i in range(ns):
        r=ran.random()
        if (r<p):
            s=1.0
            x=x+1.0
        else:
            s=0.0
        p=(tn*p-s)/(tn-1.0)
        tn=tn-1.0
    return x

def poisson(p):
    x=0.0
    b=exp(-p)
    tr=1.0
    r=ran.random()
    tr=tr*r
    while(tr>b):
        x=x+1.0
        r=ran.random()
        tr=tr*r
    return x

def markov(m,n,i,p):    #EMPIRICA DISCRETA      || p es una matrix 10x10 y x es una lista de 10     
# m --> columnas, n --> filas, i --> estado inicial, p --> matriz de transicion  
    x=[]
    for k in range(m):  
        x.append(0.0)
    for l in range(n):
        r=ran.random()
        for j in range(m):
            if (p[i][j]>r):
                break
        i=j
        x[i]=x[i]+1.0  
    return x      

def graficarprobabilidad(funcion:Callable,*args): # (funcion:Callable, *args) --> funciones variables con argumentos variables 
    y= []
    for i in range(5000):
        y.append(funcion(*args))
    y.sort()
    plt.hist(y,50,color='#64df38')
    plt.xlabel("x")
    plt.ylabel("P(x)")    
    plt.title("Distribución de Probabilidad "+nombrefuncionglobal)
    plt.show()

# Distribucion continua

nombrefuncionglobal="Uniforme"
graficarprobabilidad(partial(numpy.random.uniform,0,10))    # Grafica de la funcion uniforme de numpy
graficarprobabilidad(partial(uniforme,0,10))    # Grafica de la funcion uniforme traducida de fortran a python

nombrefuncionglobal="Exponencial"
graficarprobabilidad(partial(numpy.random.exponential,10))  # Grafica de la funcion exponencial de numpy
graficarprobabilidad(partial(exponencial,10))   # Grafica de la funcion exponencial traducida de fortran a python

nombrefuncionglobal="Normal"
graficarprobabilidad(partial(numpy.random.normal,4,2))  # Grafica de la funcion normal de numpy
graficarprobabilidad(partial(normal,4,2))   # Grafica de la funcion normal traducida de fortran a python

# Distribucion discreta

nombrefuncionglobal="Binomial"
graficarprobabilidad(partial(numpy.random.binomial,10,0.6)) # Grafica de la funcion binomial de numpy
graficarprobabilidad(partial(binomial,10,0.6))

nombrefuncionglobal="Poisson"
graficarprobabilidad(partial(numpy.random.poisson,10))
graficarprobabilidad(partial(poisson,10))

def graficarmatriz():
    x = []; y= []
    for i in range(500): 
        x.append(i)
        y.append(uniforme(0,20)) 
    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("Numero")    
    plt.title("Distribución de Probabilidad")
    plt.show()

matriz= [[0] * 10 for r in range(10)] 
for i in range(10):
    for j in range(10):
        matriz[i][j]=(ran.randint(0,100))

print(markov(5,6,7,matriz))
