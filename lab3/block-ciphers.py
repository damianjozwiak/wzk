import json
import Levenshtein

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
from random import choice, randrange
from string import ascii_letters
from time import time
from sys import argv

key = ''

modes = {
    'ECB': AES.MODE_ECB,
    'CBC': AES.MODE_CBC,
    'OFB': AES.MODE_OFB,
    'CFB': AES.MODE_CFB,
    'CTR': AES.MODE_CTR
}


def getTime(func, *args):
    start = time()

    if len(args) == 2:
        result = func(args[0], args[1])
    else:
        result = None
        print('getTime(): Wrong number of arguments')

    end = time()

    return (end - start), result


def cipherFile(file, mode):
    global key
    key = get_random_bytes(16)
    cipher = AES.new(key, mode)
    ctBytes = cipher.encrypt(file)

    ct = b64encode(ctBytes).decode('utf-8')
    if mode == AES.MODE_ECB:
        result = json.dumps({'ciphertext': ct})
    elif mode == AES.MODE_CTR:
        nonce = b64encode(cipher.nonce).decode('utf-8')
        result = json.dumps({'nonce': nonce, 'ciphertext': ct})
    else:
        iv = b64encode(cipher.iv).decode('utf-8')
        result = json.dumps({'iv': iv, 'ciphertext': ct})

    return result


def decipherFile(mode, jsonInput):

    b64 = json.loads(jsonInput)
    if 'iv' in b64:
        iv = b64decode(b64['iv'])
        cipher = AES.new(key, mode, iv=iv)
    elif 'nonce' in b64:
        nonce = b64decode(b64['nonce'])
        cipher = AES.new(key, mode, nonce=nonce)
    else:
        cipher = AES.new(key, mode)

    ct = b64decode(b64['ciphertext'])

    return cipher.decrypt(ct)


def measureTimes():
    files = ['small', 'medium', 'big']

    for filename in files:
        with open(filename + '.txt', 'r+') as file:

            print('=====')
            print('PROCESSING', filename.upper(), 'FILE')
            print('=====')

            text = bytes(file.read(), 'utf-8')
            for key, mode in modes.items():

                encryptionTime, message = getTime(cipherFile, text, mode)
                decryptionTime, result = getTime(decipherFile, mode, message)

                if result != text:
                    print('not OK')

                print('\n{}:\tencrypting:'.format(
                    key), encryptionTime, 'seconds')
                print('\tdecrypting:', decryptionTime, 'seconds')
                print('\ttotal time:', (encryptionTime + decryptionTime), 'seconds')


def checkErrors(DEBUG=False):
    print('\n=====')
    print('ERROR PROPAGATION')
    print('=====')
    # text = bytes(
        # 'Mam tu 80 znakow liczac spacje to jest dokladnie 5 razy rozmiar bloku szyfru AES', 'utf-8')
    text = get_random_bytes(16*3)
    if DEBUG:
        print('Initial message:\n', text, '\n')
    for key, mode in modes.items():
        print(key)
        encryptedMsg = json.loads(cipherFile(text, mode))
        ctList = list(encryptedMsg['ciphertext'])
        ctList[randrange(len(ctList))] = choice(ascii_letters)
        encryptedMsg['ciphertext'] = "".join(ctList)

        result = decipherFile(mode, json.dumps(encryptedMsg))
        if DEBUG:
            print('Decryption result:\n', result)
        print('Similarity ratio:', Levenshtein.ratio(result, text), '\n')


if __name__ == "__main__":
    if int(argv[1]):
        measureTimes()

    if int(argv[2]):
        checkErrors(True if len(argv) == 4 and int(argv[3]) else False)
