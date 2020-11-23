from random import choice
from string import ascii_letters
from Crypto.Random import get_random_bytes


SMALL = 1048576
MEDIUM = SMALL * 200
BIG = SMALL * 400

text = ''


def writeToFile(size, filename):
    global text
    for _ in range(size):
        text += choice(ascii_letters)

    with open(filename + '.txt', 'w+') as file:
        file.write(text)


writeToFile(SMALL, 'small')
writeToFile(MEDIUM, 'medium')
writeToFile(BIG, 'big')
text = ''
