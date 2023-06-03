from zope.interface import implementer
from .interfaces import IEncryption
from Crypto.Cipher import DES3
from Crypto.Util.number import getPrime, long_to_bytes, bytes_to_long, inverse, getRandomRange
from Crypto.Random.random import randint

class ElGamalKey:
    """
    ElGamal key object
        - p: large prime number
        - g: generator of Zp
        - y: part of the public, y = g^x mod p
        - x: private key, random number in between 0 and p-2
    """
    def __init__(self):
        self.p = None
        self.g = None
        self.y = None
        self.x = None
        self.has_private_key = False

    def construct(self, p, g, y, x=None):
        self.p = p
        self.g = g
        self.y = y
        self.x = x
        self.has_private_key = x is not None
        
    def generate_key(self):
        self.p = getPrime(512)
        self.x = randint(0, self.p - 2)
        self.g = randint(0, self.p-1)
        self.y = pow(self.g, self.x, self.p)
        self.has_private_key = True
        
    def public_key(self):
        return (self.p, self.g, self.y)
    
    def private_key(self):
        if self.has_private_key:
            return (self.p, self.g, self.y, self.x)
        raise ValueError('No private key')

    def __str__(self):
        return f'ElGamalKey(p={self.p}, g={self.g}, y={self.y}, x={self.x})'

@implementer(IEncryption)
class ElGamalEncryption:
    
    def __init__(self, key: ElGamalKey):
        self.key: ElGamalKey = key

    def _encrypt(self, m, k):
        p, g, y = self.key.public_key()
        a = pow(g, k, p)
        b = (m * pow(y, k, p)) % p
        return (a, b)
    
    def _decrypt(self, m):
        p, g, y, x = self.key.private_key()
        a, b = m
        
        r = getRandomRange(2, p-1)
        a_blind = (a * pow(g, r, p)) % p
        ax = pow(a_blind, x, p)
        plaintext_blind = (b * inverse(ax, p) ) % p
        plaintext = (plaintext_blind * pow(y, r, p)) % p
        return plaintext
    
    def encrypt(self, data):
        if isinstance(data, str):
            data = bytes(data, 'utf-8')
        plaintext = bytes_to_long(data)
        print(plaintext)
        k = randint(0, self.key.p - 2)
        ciphertext = self._encrypt(plaintext, k)
        return tuple(map(long_to_bytes, ciphertext))
    
    def decrypt(self, data: bytes):
        if not isinstance(data, tuple):
            data = (data,)
        data = tuple(map(bytes_to_long, data))
        print(data)
        plaintext = self._decrypt(data)
        return long_to_bytes(plaintext)