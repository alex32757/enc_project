# https://ru.wikipedia.org/wiki/RSA

import argparse
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

def read_arr(file):
    key_line = file.readline()
    key_str = key_line.split(',')
    return list(map(int, key_str))

def decode(arr, file_w, prv_key):
    size, d, n = prv_key
    size = size // 8
    filesize = arr[0]

    j = 0
    for byte in arr[1:]:
        j += size
        result = fast_pow(byte, d, n)

        if j > filesize:
            result >>= (j - filesize) * 8
            file_w.write(result.to_bytes(size - (j - filesize), sys.byteorder));
        else:
            file_w.write(result.to_bytes(size, sys.byteorder));


# parser
parser = argparse.ArgumentParser(description='Generate public and private key for backpack algorithm')
parser.add_argument('--prv',  dest='prv_file',  default='prv.key',
                    help='name of file with private key')
parser.add_argument('--dec',  dest='dec_file',  default='dec.txt',
                    help='name of file with decoded text')
parser.add_argument('--enc',  dest='enc_file',  default='enc.txt',
                    help='name of file with encoded text')
args = parser.parse_args()

# parse
print('-> parse')
print('\tuse name of file with private key    {}'.format(args.prv_file))
print('\tuse name of file with decoded text   {}'.format(args.dec_file))
print('\tuse name of file with encoded text   {}'.format(args.enc_file))

# read
print('-> read')
prv_key = read_arr(open(args.prv_file, 'r'))
enc_arr = read_arr(open(args.enc_file, 'r'))

# decode 
print('-> decode')
decode(enc_arr, open(args.dec_file, 'wb'), prv_key)
