# https://ru.wikipedia.org/wiki/RSA

import argparse
import random

# fast power with module
def fast_pow(a, b, m):
    res = 1
    while b != 0:
        if b & 1:
            res = (res * a) % m
        a = (a * a) % m
        b >>= 1
    return res

def gcd_extended(a, b):
    x, xx, y, yy, c = 1, 0, 0, 1, b
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx * q
        y, yy = yy, y - yy * q
    return (a, x % c, y % c)

# test phermi
def is_prime(n, count):
    if not (n & 1):
        return False
    for i in range(count):
        r = random.randint(2, n - 1)
        if fast_pow(r, n - 1, n) != 1:
            return False
    return True

def generate_prime(mine, maxe, phermi):
    while True:
        r = random.randint(mine, maxe)
        for i in range(r, maxe):
            if is_prime(i, phermi):
                return i

def generate_key(n, phermi):
    p, q = 0, 0 
    while True:
        while p == q or p * q < 2 ** n:
            p = generate_prime(2 ** (n - 1), 2 ** n, phermi)
            q = generate_prime(2 ** (n - 1), 2 ** n, phermi)
        # e is prime phermi number
        n, phi, e = p * q, (p - 1) * (q - 1), 65537
        a, d, _ = gcd_extended(e, phi)
        if a == 1:
            return p, q, n, phi, e, d

def write(file, arr):
    for i in range(len(arr) - 1):
        file.write('{}, '.format(arr[i]))
    file.write('{}'.format(arr[-1]))

# parser
parser = argparse.ArgumentParser(description='Generate public and private key for RSA algorithm')
parser.add_argument('--pub',  dest='pub_file',  default='pub.key',
                    help='name of file with public key')
parser.add_argument('--prv',  dest='prv_file',  default='prv.key',
                    help='name of file with private key')
parser.add_argument('--bit',  dest='bit_size',  default=6, type=int,
                    help='lenth of key 2^bit >= 64')
parser.add_argument('--test', dest='test_size', default=100, type=int,
                    help='count of test phermi >= 1')
args = parser.parse_args()

# parse
print('-> parse')
print('\tuse name of file with public key  {}'.format(args.pub_file))
print('\tuse name of file with private key {}'.format(args.prv_file))
print('\tuse key length                    {}'.format(2 ** args.bit_size))
print('\tuse count of test phermi          {}'.format(args.test_size))

# generate
print('-> generate')
p, q, n, phi, e, d = generate_key(2 ** args.bit_size, args.test_size)
prv_key, pub_key = [d, n], [e, n]

# save
print('-> save')
write(open(args.prv_file, 'w'), [2 ** args.bit_size] + prv_key)
write(open(args.pub_file, 'w'), [2 ** args.bit_size] + pub_key)
