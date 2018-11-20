import math


def nCr(n, r):
    f = math.factorial
    return f(n) / (f(n - r) * f(r))

def binom(n, p, k):

    return nCr(n, k) * (p ** n) * ((1 - p) ** (n - k))


def binom_list(length):
    list = []
    for i in range(length):
        list.append(binom(length, 0.5, i))
    return list

print(nCr(3,0))
print(binom(3,0.5,0))