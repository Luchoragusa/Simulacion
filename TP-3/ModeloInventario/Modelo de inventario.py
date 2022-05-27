## https://www.youtube.com/watch?v=Kmu9DNQamLw
## https://www.youtube.com/watch?v=7LuN_6m7h2o
## https://towardsdatascience.com/make-your-inventory-simulation-in-python-9cb950da8cf3
## https://github.com/sethamit71/Simulation-Optimization-of-Inventory-Management- 
## https://github.com/khashayar-h/InventorySystem

## Otros

## https://github.com/wamuir/simpy-stockout
## https://github.com/safayetsohan/Simulation-of-Inventory-System-Newspaper-/blob/master/Simulation%20of%20Inventory%20System(Newspaper).py
## https://github.com/Samialabed52/Inventory-simulation/blob/main/HW2_Q2.py

#!/usr/bin/env python3

import itertools
import simpy
import numpy

"""
Discrete-Event Simulation of Single-Product inventario System (s,S)

This is a SimPy replication of the C program given by Law and Kelton
(2000, pp. 73--79) to simulate a single-product inventario system.

William Muir (2019)

"""


class Inventario(object):

    def __init__(self, env, db, parametros):
        self._env = env
        self._db = db
        self._lastEvent = self._env.now
        self._openOrder = False
        self._parametros = parametros
        self.level = parametros["cantidad_inicial_inventario"]

    def tomarPedido(self, size):
        """
        Tomar pedidos del inventario   
        """
        self.level -= size
        self.update_time_avg_stats()

    def recibirPedido(self, size):
        """
        Sumar pedidos recibidos al inventario
        """
        self.level += size
        self.update_time_avg_stats()

    def hacerPedido(self, order):
        """
        Hacerle un pedido de reorden
        """
        setup_cost = self._parametros["K"]
        incremental_cost = self._parametros["i"]
        if not self._openOrder:
            self._openOrder = True
            self._db["costo_de_orden"] += (
                setup_cost + incremental_cost * order.size
            )
            yield self._env.timeout(order.lag)
            self.recibirPedido(order.size)
            self._openOrder = False

    def update_time_avg_stats(self):
        """
        Corresponds to `update_time_avg_stats(void)`, p. 78
        """
        time_since_last_event = self._env.now - self._lastEvent
        if self.level < 0:
            self._db["area_faltante"] -= (
                self.level * time_since_last_event
            )
        elif self.level > 0:
            self._db["area_matenimiento"] += (
                self.level * time_since_last_event
            )
        self._lastEvent = self._env.now


class HacerPedido(object):
    """
    A class for reorders
    """
    def __init__(self, size, lag_range):
        self.size = size
        self.lag = numpy.random.uniform(*lag_range)


class Demand(object):
    """
    A class for demand
    """
    def __init__(self, size):
        self.size = size


def demand_generator(env, inventario, parametros):
    """
    Generador de numeros para al demanda con una distribucion exponencial, eso es lo que nosotros agarrabamos un numero
    y lo metiamos en la linea divida para determinar la demana que se hace.
    """
    sizes = [i + 1 for i in range(parametros["cantidad_max_demanda"])]
    probabilities = numpy.diff(
        (0, *parametros["niveles_demanda"])
    )
    while True:
        demand = Demand( ## aca se genera el tamano del pedido
            size=numpy.random.choice(a=sizes, size=1, p=probabilities)[
                0
            ]
        )
        tiempo_pedido = numpy.random.exponential( ## aca se genera el tiempo entre pedidos
            parametros["tiempo_demanda"]
        )
        yield env.timeout(tiempo_pedido) ## aca lo que se hace es evaluar el tiempo actual + el tiempo del nuevo pedido que es el tiempo_pedido, si es mayor a 1 entre en la evalucion de inventario
        inventario.tomarPedido(demand.size)


def evaluation_generator(env, inventario, policy): ## aca se hace la evaluacion de inventario
    """
    Aca se evalua el inventario teniendo en cuenta a los valores de "s" y "S"
    """
    while True:
        if inventario.level < policy["minimum"]:
            order = HacerPedido(
                size=policy["target"] - inventario.level,
                lag_range=parametros["rango_retraso_entrega"],
            )
            env.process(inventario.hacerPedido(order))
        yield env.timeout(0.3) ## aca se hace la evaluacion de inventario cada vez que se llega al segundo, es decir, cada 1 segundo


def report(row_format, parametros, policy, db):
    """
    Genera la info del reporte
    """
    length = parametros["tamano_simulacion"]
    aoc = db["costo_de_orden"] / length
    ahc = db["area_matenimiento"] * parametros["h"] / length
    asc = db["area_faltante"] * parametros["pi"] / length
    row = row_format.format(
        "({},{})".format(*[str(i).rjust(3) for i in policy.values()]),
        format(aoc, ".2f"),
        format(ahc, ".2f"),
        format(asc, ".2f"),
        format(aoc + ahc + asc, ".2f"),
    )
    print(row)


if __name__ == "__main__":

    """
    Estos son los parametros iniciales del ejercicio que esta en la pagina 102 // 30 del pdf del Law and Kelton
    """
    parametros = dict(
        cantidad_inicial_inventario=60, ## Esto es el inventario inicial
        cantidad_max_demanda=4, ## Esto es el numero de demandas que se pueden hacer, osea la cantidad de rangos entre los que tiene que caer le numero aleatorio
        niveles_demanda=( ## Esto es la funcion de distribucion de demandas, osea los rangos de los numeros aleatorios
            0.167,
            0.500,
            0.833,
            1.000,
        ),
        tiempo_demanda=0.10, ## Esto es el tiempo entre demandas
        rango_retraso_entrega=(0.50, 1.00), ## Tiempo de demora de la entrega, tiene distrubicion uniforme
        tamano_simulacion=120, ## Cantidad de repeticiones de la simulacion
        K=32.0, ## Es el precio del pedido en si, seria como una especia de evio
        i=3.0, ## Es el precio por unidad pedida
        h=1.0,
        pi=5.0,
        numero_politicas=9, ## Seria el numero de politicas
    )

    politicas = [ ## Son las politicas que menciona el ejericicio, osea evalua "s" contra "S", se deja fija "s" en 20 y se evaluan los valores de 20 en 20 de "S" hasta 100
        dict(minimum=s, target=S)
        for s, S in itertools.product([55, 40, 60], [40, 60, 80, 100])
        if s < S
    ]

    """
    Son los nombres de las columnas de la tabla
    """
    row_format = "\n{:>10}{:>25}{:>25}{:>25}{:>25}"
    header = row_format.format(
        "Politica",
        "Costo de orden",
        "Coste de mantenimiento",
        "Costo de faltante",
        "Costo total",
    )
    print(header)

    """
    Run the simulation.  As per Law and Kelton (2000), this only a
    single replication is run.  Given differences in random number
    generators (e.g., they use a LCG), results will not be identical.

    Se puede probar usando otro simulador como el LCG
    """
    numpy.random.seed(1234) ## Genero el num random
    for politica in politicas:
        env = simpy.Environment()
        db = dict(
            last_event=float(),
            costo_de_orden=float(),
            area_matenimiento=float(),
            area_faltante=float(),
        )

        inventario = Inventario(env, db, parametros)
        dmd_gen = env.process(
            demand_generator(env, inventario, parametros)
        )
        eval_gen = env.process(
            evaluation_generator(env, inventario, politica)
        )
        env.run(until=parametros["tamano_simulacion"])
        report(row_format, parametros, politica, db)
