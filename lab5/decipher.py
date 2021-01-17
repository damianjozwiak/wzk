from PIL import Image
from sys import argv
from os import path

if len(argv) != 3:
    exit(f'Usage: python3 {argv[0]} [share 1] [share 2]')

inFile1 = argv[1]
if not path.isfile(inFile1):
    exit(f'File {argv[1]} does not exist.')

inFile2 = argv[2]
if not path.isfile(inFile2):
    exit(f'File {argv[2]} does not exist.')

share1 = Image.open(inFile1)
share2 = Image.open(inFile2)

result = Image.blend(share1.convert('L'), share2.convert('L'), 0.5)

# result.save('result.png', 'PNG')
result.show()