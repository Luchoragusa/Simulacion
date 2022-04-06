import random as ran
import matplotlib.pyplot as plt


def fibonacci(n):
    if n == 1 or n == 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def estrategiaFibonacci(saldo):
    enesimo = 1
    mesa = ["Red"] * 18 + ["Black"] * 18 + ["Green"] * 2
    saldo_history = []
    while saldo > 0:
        apuesta = fibonacci(enesimo) * .01
        if apuesta > saldo:
            apuesta = saldo
        roll = ran.choice(mesa)
        if roll == "Red":
            saldo += apuesta
            enesimo = max(enesimo - 2, 1)
        else:
            saldo -= apuesta
            enesimo += 1
        saldo_history.append(saldo)
    return saldo_history

def main():
    saldo = 100
    for i in range(4):
        plt.plot(estrategiaFibonacci(saldo))

    plt.xlabel("Numero de rondas", fontsize=10, fontweight="bold")
    plt.ylabel("Saldo", fontsize=10, fontweight="bold")
    plt.title("Estrategia Fibonacci", fontsize=10, fontweight="bold")

    plt.show()

main()