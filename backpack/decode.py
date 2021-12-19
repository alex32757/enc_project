# https://intuit.ru/studies/professional_skill_improvements/20679/courses/1234/lecture/31200?page=6

import argparse
import sys

def read_arr(file):
    key_line = file.readline()
    key_str = key_line.split(',')
    return list(map(int, key_str))

def decode(arr, file_w, prv_key, m, r):
    filesize = arr[0]
    size = len(prv_key)

    j = 0
    for byte in arr[1:]:
        j += size // 8
        result = 0
        byte = (byte * r) % m
        for i in range(size):
            if byte >= prv_key[size - 1 - i]:
                byte -= prv_key[size - 1 - i]
                result = (result << 1) | 1
            else:
                result = (result << 1)

        if j > filesize:
            result >>= (j - filesize) * 8
            file_w.write(result.to_bytes(size // 8 - (j - filesize), sys.byteorder));
        else:
            file_w.write(result.to_bytes(size // 8, sys.byteorder));


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
decode(enc_arr, open(args.dec_file, 'wb'), prv_key[2:], prv_key[0], prv_key[1])
