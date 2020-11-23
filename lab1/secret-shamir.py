from sys import argv, exit
from random import randrange, sample
from sympy import nextprime
from numpy import prod

FIELD_SIZE = 10**5


def init(argv):

    msg = "Usage: python3 " + \
        argv[0] + " <secret> <number of shares> <minimum number of shares>"

    if len(argv) < 4:
        exit(msg)

    secret = int(argv[1])
    n = int(argv[2])
    t = int(argv[3])

    if t > n:
        print("===> ERROR: minimum number of shares should be lower than the actual number of shares\n")
        exit(msg)

    print("Secret:\t\t\t\t", secret)
    print("Number of shares:\t\t", n)
    print("Minimum number of shares:\t", t)

    return secret, n, t


def polynomial(x, coeffs):
    return sum([coeffs[i] * x**(len(coeffs) - i - 1) for i in range(len(coeffs))])


def split(secret, n, t):

    p = nextprime(randrange(max(n, secret), FIELD_SIZE))

    a = [randrange(1, FIELD_SIZE) for _ in range(t - 1)]
    a.append(secret)

    shares = [(i, polynomial(i, a)) for i in range(1, n+1)]

    print("p:\t\t\t\t", p)
    print("Shares:\t\t\t\t", shares)
    return p, shares


def combine(p, shares):
    print("Shares used:\t\t\t", shares)

    secret = 0
    for i in range(len(shares)):
        x, y = shares[i][0], shares[i][1]
        for j in range(len(shares)):
            if j != i:
                xj = shares[j][0]
                y *= (xj / (x - xj))
        secret += y

    # secret = sum([shares[i][1] * prod([shares[j][0]/(shares[i][0] - shares[j][0])
    #                                    if j != i else 1 for j in range(len(shares))]) for i in range(len(shares))])

    return int(round(secret, 0)) % p


if __name__ == "__main__":

    secret, n, t = init(argv)
    p, shares = split(secret, n, t)

    # print("Combined secret:\t\t", combine(p, sample(shares, t)))
    shares.pop(2)
    print("Combined secret:\t\t", combine(p, shares))
