import random as ran
from math import log,exp
import matplotlib.pyplot as plt
from functools import partial
from typing import Callable, Iterable
import numpy

def mm1():
    titulo = 'Sistema de colas MM1'
    print(titulo.center(80, '='))
    promClientesHora = int(input('Ingrese el promedio de clientes por hora: '))
    promServicioHora= int(input('Ingrese el promedio de clientes atendidos por hora: '))
    # Si es mayor, calcula para cola no infinita 
    if promServicioHora > promClientesHora:
        Ls = promClientesHora/(promServicioHora-promClientesHora)
        Ws = 1/(promServicioHora-promClientesHora)
        Wsl = Ws*60
        Lq = Ls*promClientesHora/promServicioHora
        Wq = Ws*promClientesHora/promServicioHora
        Wql = Wq*60
        print(f'Clientes en el sistema: {Ls} ')
        print(f'Tiempo en el sistema: {Ws} Horas')
        print(f'Tiempo en el sistema: {Wsl} minutos')
        print(f'Clientes en cola: {round(Lq)}')
        print(f'Tiempo en la cola: {round(Wq)} horas')
        print(f'Tiempo en la cola: {Wql}')
    # Si no se cumple la condicion, calcula para cola infinita
    else: #No va a existir una cola adecuada para nuestro sistema
        titulo2 = '\nCola infinita\n'
        print(titulo2.center(80, '='))
        opcion = 'Se puede hacer calculo de sistema sin cola\n'
        print(opcion.center(80, '*'))

        trafico = promClientesHora/promServicioHora
        Cperdidos = trafico/(trafico+1)
        print(f"Porcentaje de perdidos> {Cperdidos*100} %")

        print("Si el horario de atencion consta de 8 horas")
        totalC = promClientesHora*8
        print(f"Aproximadamente la cantidad de clientes en un dia es: {totalC}")

        peridas = totalC*Cperdidos
        print(f"Aproximadamente se perdieron: {round(peridas)} clientes")

        atendidos = totalC-peridas
        print(f"Aproximadamente se atendieron: {round(atendidos)} clientes")
#mm1()

'''
    Mediante el numero de clientes seteado, se puede ver por cada cliente:
        1. Su tiempo de llegada
        2. Su tiempo de espera
        3. Su tiempo de servicio
        4. Su tiempo de salida
'''
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
            tiempo_salida_clientes.append(tiempo_llegada[i] + tiempo_espera[i] + tiempo_servicios[i])
        if(i >= 1):
            clientes.append(i)
            tiempo_llegada.append(tiempo_llegada[i-1] + ran.random())
            tiempo_espera.append(max(tiempo_salida_clientes[i-1], tiempo_llegada[i]) - tiempo_llegada[i])
            tiempo_servicios.append(ran.random())
            tiempo_ocio_servidor.append(max(tiempo_salida_clientes[i-1], tiempo_llegada[i])-tiempo_salida_clientes[i-1])
            tiempo_salida_clientes.append(tiempo_llegada[i] + tiempo_espera[i] + tiempo_servicios[i])
        i = i + 1
    i = 0

    guion = '='
    while (i < num_clientes):
        print(f"\nCliente: {round(clientes[i], 2)} || Tiempo de llegada: {round(tiempo_llegada[i],2)} || Tiempo de espera: {round(tiempo_espera[i],2)} || Tiempo de servicio: {round(tiempo_servicios[i],2)} || Tiempo de salida: {round(tiempo_salida_clientes[i],2)}")
        print(guion.center(120, '='))
        i += 1
lineaDeEspera()