from sympy import nextprime, mod_inverse
from random import randrange
from string import ascii_letters
from sys import argv
from math import gcd

TEST = True


def chunkString(string, n):
    res = []
    temp = ''
    for char in string:
        if temp == '' and char == '0':
            res.append(char)
        elif int(temp + char) > n:
            res.append(temp)
            temp = char
        else:
            temp += char

    res.append(temp)

    return res


def getPrime(a=1000, b=9972):
    return nextprime(randrange(a, b))


def isCoprime(x, y):
    return gcd(x, y) == 1


def getCoprime(x):
    while True:
        y = getPrime(0, 100)
        if isCoprime(x, y):
            break
    return y


def parseChunk(message, key):
    # print(message, key)
    return (message**key[0]) % key[1]


def encrypt(message, key):
    chunks = chunkString(str(message), key[1])
    # chunks = list(str(message))
    return [parseChunk(int(chunk), key) for chunk in chunks]


def decrypt(chunks, key):
    return ''.join([str(parseChunk(chunk, key)) for chunk in chunks])


def getKeys():
    p, q = (47, 71) if TEST else (getPrime(), getPrime())

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 79 if TEST else getCoprime(phi)
    d = mod_inverse(e, phi)

    print('p:', p, '\tq:', q)
    print('n:', n, 'phi:', phi)
    print('e:', e, '\td:', d)

    return (e, n), (d, n)


def generateMessage(length=50):
    return randrange(10**(length - 1), 10**length)


if __name__ == "__main__":
    publicKey, privateKey = getKeys()
    print('\nPublic Key:', publicKey, '\nPrivate Key:', privateKey)
    message = 6882326879666683 if TEST else generateMessage()
    print('\nMessage:', message)

    encryptedChunks = encrypt(message, publicKey)
    # print('Encrypted message:', encryptedChunks)

    decryptedMsg = decrypt(encryptedChunks, privateKey)
    print('Decrypted message:', decryptedMsg)

    print('Message decrypted correctly' if str(message) ==
          decryptedMsg else "ERROR: Result incorrect")
