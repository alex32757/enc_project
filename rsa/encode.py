# https://ru.wikipedia.org/wiki/RSA

import argparse
import os
import sys

# fast power with module
def fast_pow(a, b, m):
    res = 1
    while b != 0:
        if b & 1:
            res = (res * a) % m
        a = (a * a) % m
        b >>= 1
    return res

def read_public_key(file):
    key_line = file.readline()
    key_str = key_line.split(',')
    size, e, n = list(map(int, key_str))
    return size, e, n

def encode(file_r, file_w, pub_key):
    file_w.write('{}'.format(os.fstat(file_r.fileno()).st_size))
    size, e, n = pub_key;
    size = size // 8;

    while True:
        arr = file_r.read(size)
        if arr == b'':
            break

        byte = int.from_bytes(arr, sys.byteorder)
        byte <<= (size - len(arr)) * 8
        result = fast_pow(byte, e, n)

        file_w.write(', {}'.format(result))

# parser
parser = argparse.ArgumentParser(description='Generate public and private key for backpack algorithm')
parser.add_argument('--pub',  dest='pub_file',  default='pub.key',
                    help='name of file with public key')
parser.add_argument('--txt',  dest='txt_file',  default='txt.txt',
                    help='name of file with text to encode')
parser.add_argument('--enc',  dest='enc_file',  default='enc.txt',
                    help='name of file with encoded text')
args = parser.parse_args()

# parse
print('-> parse')
print('\tuse name of file with public key     {}'.format(args.pub_file))
print('\tuse name of file with text to encode {}'.format(args.txt_file))
print('\tuse name of file with encoded text   {}'.format(args.enc_file))

# read
print('-> read')
size, e, n = read_public_key(open(args.pub_file, 'r'))

# encode
print('-> encode')
encode(open(args.txt_file, 'rb'), open(args.enc_file, 'w'), (size, e, n))
