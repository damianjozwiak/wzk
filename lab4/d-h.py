from random import getrandbits
from math import gcd
from sympy import nextprime, isprime, is_primitive_root


BITS = 32


class Person:
    def __init__(self, n, g):
        self.n = n
        self.g = g
        self.privKey = getrandbits(BITS)

    def calculateX(self):
        return pow(self.g, self.privKey, self.n)

    def getSecret(self, Y):
        return pow(Y, self.privKey, self.n)


def findPrimitiveRoot(modulo):
    for i in range(modulo//2, modulo):
        if is_primitive_root(i, modulo):
            return i
    return None


def getN():
    n = nextprime(getrandbits(BITS))
    while True:
        if isprime(n*2+1):
            break
        n = nextprime(getrandbits(BITS))
    return n*2+1


if __name__ == "__main__":
    n = getN()
    g = findPrimitiveRoot(n)
    Alice = Person(n, g)
    Bob = Person(n, g)

    print('n:', n, 'g:', g, '\n')
    print('Private key (person A):', Alice.privKey)
    print('Private key (person B):', Bob.privKey, '\n')

    X = Alice.calculateX()
    Y = Bob.calculateX()

    print('PERSON A:\nPrivate key:', Alice.privKey, '\nX:', X, '\n')
    print('PERSON B:\nPrivate key:', Bob.privKey, '\nY:', Y, '\n')

    print('Secret k (person A)', Alice.getSecret(Y))
    print('Secret k (person B)', Bob.getSecret(X))
