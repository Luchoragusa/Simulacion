import random as ran
import matplotlib.pyplot as plt


def fibonacci(n):
    if n == 1 or n == 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def fibonacci_strategy(bankroll):
    fibonacci_number = 1
    pockets = ["Red"] * 18 + ["Black"] * 18 + ["Green"] * 2
    bankroll_history = []
    while bankroll > 0:
        bet = fibonacci(fibonacci_number) * .01
        if bet > bankroll:
            bet = bankroll
        roll = ran.choice(pockets)
        if roll == "Red":
            bankroll += bet
            fibonacci_number = max(fibonacci_number - 2, 1)
        else:
            bankroll -= bet
            fibonacci_number += 1
        bankroll_history.append(bankroll)
    return bankroll_history



def main():
    histF = []
    bankroll = 100
    for i in range(4):
        histF = fibonacci_strategy(bankroll)
        plt.plot(histF, linewidth=2)
        plt.xlabel("Numero de rondas", fontsize=20, fontweight="bold")
        plt.ylabel("Saldo", fontsize=20, fontweight="bold")
        plt.xticks(fontsize=15, fontweight="bold")
        plt.yticks(fontsize=15, fontweight="bold")
        plt.title("Estrategia Fibonacci", fontsize=22, fontweight="bold")

main()