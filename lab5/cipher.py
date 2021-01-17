from PIL import Image
from sys import argv
from os import path
from random import choice

if len(argv) != 2:
    exit(f'Usage: python3 {argv[0]} [file to be cyphered]')

inFile = argv[1]

if not path.isfile(inFile):
    exit(f'File {argv[1]} does not exist.')

img = Image.open(inFile).convert('1')

width, height = img.size[0]*2, img.size[1]*2

outImg1 = Image.new('1', (width, height))
outImg2 = Image.new('1', (width, height))

patterns = ((1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1),
            (0, 1, 1, 0), (0, 1, 0, 1), (0, 0, 1, 1))

for x in range(0, width, 2):
    for y in range(0, height, 2):
        pixel = img.getpixel((x/2, y/2))
        pattern = choice(patterns)
        outImg1.putpixel((x, y), pattern[0])
        outImg1.putpixel((x+1,y), pattern[1])
        outImg1.putpixel((x, y+1), pattern[2])
        outImg1.putpixel((x+1,y+1), pattern[3])
        if pixel == 0:
            outImg2.putpixel((x, y), 1-pattern[0])
            outImg2.putpixel((x+1,y), 1-pattern[1])
            outImg2.putpixel((x, y+1), 1-pattern[2])
            outImg2.putpixel((x+1,y+1), 1-pattern[3])
        else:
            outImg2.putpixel((x, y), pattern[0])
            outImg2.putpixel((x+1,y), pattern[1])
            outImg2.putpixel((x, y+1), pattern[2])
            outImg2.putpixel((x+1,y+1), pattern[3])
    
outImg1.save('share1.png', 'PNG')
outImg2.save('share2.png', 'PNG')