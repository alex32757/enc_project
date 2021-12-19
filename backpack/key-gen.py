# https://intuit.ru/studies/professional_skill_improvements/20679/courses/1234/lecture/31200?page=6

import argparse
import random

# return gcd, ax + by = gcd
def gcd_extended(a, b):
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx * q
        y, yy = yy, y - yy * q
    return (a, x, y)

# return private key
def generate_private_key(n, diff):
    a = []
    s = 0

    for i in range(n):
        r = random.randint(1, diff)
        a.append(s + r)
        s += s + r

    return a

# return public key, secret m, secret n, secret n ^ -1
def generate_public_key(prv_key):
    s = prv_key[-1] + 1
    m = random.randint(s, 10 * s)
    n = random.randint(m // 2, m)

    while True:
        nod, x, y = gcd_extended(n, m)
        if nod == 1:
            break
        n = random.randint(m // 2, m)
    
    a = list(map(lambda x: (x * n) % m, prv_key))

    return a, m, n, x % m

def write(file, arr):
    for i in range(len(arr) - 1):
        file.write('{}, '.format(arr[i]))
    file.write('{}'.format(arr[-1]))

# parser
parser = argparse.ArgumentParser(description='Generate public and private key for backpack algorithm')
parser.add_argument('--pub',  dest='pub_file',  default='pub.key',
                    help='name of file with public key')
parser.add_argument('--prv',  dest='prv_file',  default='prv.key',
                    help='name of file with private key')
parser.add_argument('--bit',  dest='bit_size',  default=6, type=int,
                    help='lenth of key 2^bit >= 64')
parser.add_argument('--diff', dest='diff_size', default=100, type=int,
                    help='max difference between sum and next element >= 2')
args = parser.parse_args()

# parse
print('-> parse')
print('\tuse name of file with public key  {}'.format(args.pub_file))
print('\tuse name of file with private key {}'.format(args.prv_file))
print('\tuse key length                    {}'.format(2 ** args.bit_size))
print('\tuse diff                          {}'.format(args.diff_size))

# generate
print('-> generate')
prv_key          = generate_private_key(2 ** args.bit_size, args.diff_size)
pub_key, m, n, x = generate_public_key(prv_key)

# save
print('-> save')
write(open(args.prv_file, 'w'), [m, x] + prv_key)
write(open(args.pub_file, 'w'), pub_key)
