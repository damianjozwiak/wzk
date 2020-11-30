from random import choice
from string import ascii_letters
from Crypto.Random import get_random_bytes


SMALL = 1048576
MEDIUM = SMALL * 200
BIG = SMALL * 400

text = ''
print('small')
for _ in range(SMALL):
        text += choice(ascii_letters)
    
with open('small.txt', 'w+') as file:
    file.write(text)

print('medium')
for _ in range(MEDIUM - SMALL):
        text += choice(ascii_letters)

with open('medium.txt', 'w+') as file:
    file.write(text)

print('big')
for _ in range(BIG - MEDIUM):
        text += choice(ascii_letters)

with open('big.txt', 'w+') as file:
    file.write(text)