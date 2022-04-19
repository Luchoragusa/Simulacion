import matplotlib.pyplot as plt

n = 1000
x = [0]; u = [0]
x[0] = 4798373
u[0] = x[0]/(2^31 - 1)

print(x)
print(u)

for i in range(n):
    if(i!=0):
        x.append(((2^16+3) * x[i-1]) % (2 ^ 31))
        u.append(x[i] / (2 ^ 31))
    plt.plot(x,u)
print(x)
print(u)
plt.show()