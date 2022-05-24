import random as ran
from math import log,exp
import matplotlib.pyplot as plt
from functools import partial
from typing import Callable, Iterable
import numpy

def mm1():
    titulo = 'Sistema de colas MM1'
    print(titulo.center(80, '='))
    promClientesHora = int(input('Ingrese el promedio de clientes =por hora: '))
    promServicioHora= int(input('Ingrese el promedio de clientes atendidos por hora: '))
    if promServicioHora > promClientesHora:
        Ls = promClientesHora/(promServicioHora-promClientesHora)
        Ws = 1/(promServicioHora-promClientesHora)
        Wsl = Ws*60
        Lq = Ls*promClientesHora/promServicioHora
        Wq = Ws*promClientesHora/promServicioHora
        Wql = Wq*60

        print(f'Clientes en el sistema: ${Ls} ')
        print(f'Tiempo en el sistema: ${Ws} Horas')
        print(f'Tiempo en el sistema: ${Wsl} minutos')
        print(f'Clientes en cola: ${Lq}')
        print(f'Tiempo en la cola: ${Wq} horas')
        print(f'Tiempo en la cola: ${Wql}')
    else: #No va a existir una cola adecuada para nuestro sistema
        titulo2 = 'Cola infinita'
        print(titulo2.center(80, '='))
        print("")
        opcion = 'Se puede hacer calculo de sistema sin cola'
        print(opcion.center(80, '*'))

        trafico = promClientesHora/promServicioHora
        Cperdidos = trafico/(trafico+1)
        print(f"Porcentaje de perdidos> ${Cperdidos*100} %")

        print("Si el horario de atencion consta de 8 horas")
        totalC = promClientesHora*8
        print(f"Aproximadamente la cantidad de clientes en un dia es: ${totalC}")

        peridas = totalC*Cperdidos
        print(f"Aproximadamente se perdieron: ${peridas} clientes")

        atendidos = totalC-peridas
        print(f"Aproximadamente se atendieron: ${atendidos} clientes")
mm1()

def lineaDeEspera():
    i = 0
    clientes = []
    tiempo_llegada = []
    tiempo_espera = []
    tiempo_servicios = []
    tiempo_ocio_servidor = []
    tiempo_salida_clientes = []
    num_clientes = 100

    while(i < num_clientes):
        if(i == 0):
            clientes.append(i)
            tiempo_llegada.append(i)
            tiempo_espera.append(i)
            tiempo_servicios.append(ran.random())
            tiempo_ocio_servidor.append(i)
            tiempo_ocio_servidor.append(tiempo_llegada[i] + tiempo_espera[i] + tiempo_servicios[i])
        if(i >= 1):
            clientes.append(i)
            tiempo_llegada.append(tiempo_llegada[i-1] + ran.random())
            tiempo_espera.append(max(tiempo_salida_clientes[i-1], tiempo_llegada[i])-tiempo_llegada[i])
            tiempo_servicios.append(ran.random())
            tiempo_ocio_servidor.append(max(tiempo_salida_clientes[i-1], tiempo_llegada[i])-tiempo_salida_clientes[i-1])
            tiempo_ocio_servidor.append(tiempo_llegada[i] + tiempo_espera[i] + tiempo_servicios[i])
        i += 1
        while (i < num_clientes):
            print(str(clientes[i]))