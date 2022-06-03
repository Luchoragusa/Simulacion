## https://github.com/wamuir/simpy-stockout

import itertools
import simpy
import numpy
import matplotlib.pyplot as plt

evolucionInventario = []
evolucionDemanda= []
evolucionInventarioT=[]

l_costo_de_orden=[]
l_area_faltante=[]
l_area_matenimiento=[]

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

        evolucionInventario.append(self.level) ## aca se guarda el estado del inventario

        self.actualiza_reloj()

    def recibirPedido(self, size):
        """
        Sumar pedidos recibidos al inventario
        """
        self.level += size

        evolucionInventario.append(self.level) ## aca se guarda el estado del inventario

        self.actualiza_reloj()

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

            l_costo_de_orden.append(self._db["costo_de_orden"])

            yield self._env.timeout(order.lag)
            self.recibirPedido(order.size)
            self._openOrder = False

    def actualiza_reloj(self):
        """
        Corresponds to `actualiza_reloj(void)`, p. 78
        """
        time_since_last_event = self._env.now - self._lastEvent
        if self.level < 0:
            self._db["area_faltante"] -= (
                self.level * time_since_last_event
            )

            l_area_faltante.append(self._db["area_faltante"])

        elif self.level > 0:
            self._db["area_matenimiento"] += (
                self.level * time_since_last_event
            )

            l_area_matenimiento.append(self._db["area_matenimiento"])

        self._lastEvent = self._env.now
        evolucionInventarioT.append(self._lastEvent) ## aca se guardan los tiempos de los pedidos


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
    Generador de numeros para la demanda con una distribucion exponencial, eso es lo que nosotros agarrabamos un numero
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

        evolucionDemanda.append(demand.size) ## aca se guarda la demanda que van saliendo

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
        yield env.timeout(1) ## aca se hace la evaluacion de inventario cada vez que se llega al segundo, es decir, cada 1 segundo


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
        cantidad_max_demanda=4, ## Esto es el numero de demandas que se pueden hacer, osea la cantidad de rangos entre los que tiene que caer el numero aleatorio
        niveles_demanda=( ## Esto es la funcion de distribucion de demandas, osea los rangos de los numeros aleatorios
            0.167,
            0.500,
            0.833,
            1.000,
        ),
        tiempo_demanda=0.10, ## Esto es el tiempo entre demandas
        rango_retraso_entrega=(0.50, 1.00), ## Tiempo de demora de la entrega, tiene distrubicion uniforme
        tamano_simulacion=20, ## Cantidad de x de la simulacion
        K=32.0, ## Es el precio del pedido en si, seria como una especie de envio
        i=3.0, ## Es el precio por unidad pedida
        h=1.0, # Costo de Holding, es decir, de mantener el articulo guardado, por el alquiler, mantenimiento y esas cosas
        pi=5.0, # Costo de Backlog (items pedidos no recibidos)
        numero_politicas=9, ## Seria el numero de politicas
    )

    politicas = [ ## Son las politicas que menciona el ejericicio, osea evalua "s" contra "S", se deja fija "s" en 20 y se evaluan los valores de 20 en 20 de "S" hasta 100
        dict(minimum=s, target=S)
        ##for s, S in itertools.product([20, 40, 60], [40, 60, 80, 100])
        for s, S in itertools.product([20], [40]) ## dependiente la cantidad de politicas son las corridas del ejercicio
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

        evolucionInventario = []
        evolucionDemanda= []
        evolucionInventarioT=[]

        evolucionInventario.append(parametros["cantidad_inicial_inventario"]) ## Aca se guarda el inventario inicial
        evolucionInventarioT.append(0) ## Aca se guarda el tiempo inicial

        inventario = Inventario(env, db, parametros)
        dmd_gen = env.process(
            demand_generator(env, inventario, parametros)
        )
        eval_gen = env.process(
            evaluation_generator(env, inventario, politica)
        )
        env.run(until=parametros["tamano_simulacion"])

        report(row_format, parametros, politica, db)

        plt.bar(evolucionInventarioT, evolucionInventario)
        plt.title("Evolucion del stock del inventario")
        plt.xlabel("Tiempo de pedidos")
        plt.ylabel("Estado del inventario")  
        plt.axhline(y=0, color = "black")  
        plt.axhline(y=parametros["cantidad_inicial_inventario"], color = "green", linestyle = "dotted")
        plt.axhline(y=(numpy.mean(evolucionInventario)), color = "yellow", linestyle = "dotted")

        plt.show()
        x = []
        for i in range(len(evolucionDemanda)):
            x.append(i)
        plt.bar(x, evolucionDemanda)
        plt.title("Evolucion de la demanada")
        plt.ylabel("Cantidad de productos demandados")  
        plt.axhline(y=(numpy.mean(evolucionDemanda)), color = "yellow", linestyle = "dotted")
        plt.show()

        x = []
        y = []
        for i in range(len(l_costo_de_orden)):
            x.append(i)
            y.append(l_costo_de_orden[i]/parametros["tamano_simulacion"])
        plt.title("Evolucion del costo de orden")
        plt.ylabel("Costo de orden") 
        plt.plot(x, y)
        plt.show()

        x = []
        y = []
        for i in range(len(l_area_faltante)):
            x.append(i)
            y.append((l_area_faltante[i] * parametros["pi"])/parametros["tamano_simulacion"])
        plt.title("Evolucion del costo de faltantes")
        plt.ylabel("Costo de faltante") 
        plt.ylabel("Cantidad de costos de faltante")
        plt.plot(x, y)
        plt.show()

        x = []
        y = []
        for i in range(len(l_area_matenimiento)):
            x.append(i)
            y.append((l_area_matenimiento[i] * parametros["h"]) /parametros["tamano_simulacion"])
        plt.title("Evolucion del costo de mantenimiento")
        plt.ylabel("Costo del mantenimiento") 
        plt.xlabel("Cantidad de costos de mantenimiento")
        plt.plot(x, y)
        plt.show()
