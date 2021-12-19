# https://intuit.ru/studies/professional_skill_improvements/20679/courses/1234/lecture/31200?page=6

import argparse
import os
import sys

def read_public_key(file):
    key_line = file.readline()
    key_str = key_line.split(',')
    return list(map(int, key_str))

def encode(file_r, file_w, pub_key):
    size = len(pub_key) // 8;
    file_w.write('{}'.format(os.fstat(file_r.fileno()).st_size))

    while True:
        arr = file_r.read(size)
        if arr == b'':
            break

        result = 0
        byte = int.from_bytes(arr, sys.byteorder)
        byte <<= (size - len(arr)) * 8
        for i in range(len(pub_key)):
            if (byte >> i) & 1 == 1:
                result += pub_key[i]

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
pub_key = read_public_key(open(args.pub_file, 'r'))

# encode
print('-> encode')
encode(open(args.txt_file, 'rb'), open(args.enc_file, 'w'), pub_key)
