from zope.interface import implementer
from .interfaces import IAsymEncryption
from Crypto.Random.random import randint
from Crypto.Util.number import getPrime, long_to_bytes, bytes_to_long, inverse, getRandomRange
from Crypto.Util.py3compat import tobytes, tostr
from Crypto.Util.asn1 import DerSequence, DerNull
from Crypto.PublicKey import (_expand_subject_public_key_info,
                              _create_subject_public_key_info,) # Shouldn't be used, but it is what it is


# TODO: Mozda dodati protekciju za sam PEM format preko nekog passhprase-a, ima u Crypto.PublicKey.RSA ideja
class ElGamalKey:
    """
    ElGamal key object
        - p: large prime number
        - g: generator of Zp
        - y: part of the public, y = g^x mod p
        - x: private key, random number in between 0 and p-2
    """

    # OID for ElGamal
    oid = '1.3.14.7.2.1.1'

    def __init__(self):
        self.p = None
        self.g = None
        self.y = None
        self.x = None
        self.has_private_key = False

    @classmethod
    def construct(cls, p, g, y, x=None):
        elgamal_key = ElGamalKey()
        elgamal_key.p = p
        elgamal_key.g = g
        elgamal_key.y = y
        elgamal_key.x = x
        elgamal_key.has_private_key = x is not None
        return elgamal_key
        
    # def generate_key(self):
    #     self.p = getPrime(512)
    #     self.x = randint(0, self.p - 2)
    #     self.g = randint(0, self.p-1)
    #     self.y = pow(self.g, self.x, self.p)
    #     self.has_private_key = True


    def generate_key(self, key_length):
        self.p = getPrime(key_length)
        self.x = randint(0, self.p - 2)
        self.g = randint(0, self.p - 1)
        self.y = pow(self.g, self.x, self.p)
        self.has_private_key = True

    def has_private(self):
        return self.has_private_key
    
    def public_key(self):
        return ElGamalKey.construct(self.p, self.g, self.y)
        
    def public_key_components(self):
        return (self.p, self.g, self.y)
    
    def private_key_components(self):
        if self.has_private_key:
            return (self.p, self.g, self.y, self.x)
        raise ValueError('No private key')

    def export_key(self, format='PEM'):
        """
        Export ElGamal key into a PEM format.
        """
        # DER format is always used, even in case of PEM, which simply
        # encodes it into BASE64.
        if self.has_private():
            binary_key = DerSequence([0,
                                      self.p,
                                      self.g,
                                      self.y,
                                      self.x,
                                      ]).encode()
            
            key_type = 'ELGAMAL PRIVATE KEY'
        else:
            key_type = 'PUBLIC KEY'
            binary_key = _create_subject_public_key_info(ElGamalKey.oid,
                                                         DerSequence([self.p,
                                                                      self.g,
                                                                      self.y,]),
                                                         DerNull()
                                                         )
        if format == 'PEM':
            from Crypto.IO import PEM

            pem_str = PEM.encode(binary_key, key_type, None, None)
            return tobytes(pem_str)
        return binary_key
        
    def import_key(extern_key, passphrase=None):
        """
        Import an ElGamal key (public or private half), encoded in standard PEM format
        """
        from Crypto.IO import PEM

        extern_key = tobytes(extern_key)

        (der, marker, enc_flag) = PEM.decode(tostr(extern_key), None)
        return _import_keyDER(der, None)

    def __str__(self):
        return f'ElGamalKey(p={self.p}, g={self.g}, y={self.y}, x={self.x})'

@implementer(IAsymEncryption)
class ElGamal_Wrapper:
    
    def __init__(self, key: ElGamalKey):
        self.key: ElGamalKey = key

    @classmethod
    def generate_key(cls, key_length):
        elgamal_key = ElGamalKey()
        elgamal_key.generate_key(key_length)
        return elgamal_key

    @classmethod
    def construct_key(cls, p, g, y, x=None):
        return ElGamalKey.construct(p, g, y, x)

    def _encrypt(self, m, k):
        p, g, y = self.key.public_key_components()
        a = pow(g, k, p)
        b = (m * pow(y, k, p)) % p
        return (a, b)
    
    def _decrypt(self, m):
        p, g, y, x = self.key.private_key_components()
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
        # print(plaintext)
        k = randint(0, self.key.p - 2)
        ciphertext = self._encrypt(plaintext, k)
        return tuple(map(long_to_bytes, ciphertext))
    
    def decrypt(self, data: bytes):
        if not isinstance(data, tuple):
            data = (data,)
        data = tuple(map(bytes_to_long, data))
        # print(data)
        plaintext = self._decrypt(data)
        return long_to_bytes(plaintext)
    
def _import_private(encoded, *kwargs):
    # ElGamalPrivateKey ::= SEQUENCE {
    #           version Version,
    #           modulus INTEGER, -- p
    #           publicExponent INTEGER, -- g
    #           public result of  of g ^ x mod p INTEGER, -- y
    #           private random INTEGER, -- x
    # }
    #
    # Version ::= INTEGER
    der = DerSequence().decode(encoded, nr_elements=5, only_ints_expected=True)
    if der[0] != 0:
        raise ValueError("No valid encoding of an ElGamal private key")
    return ElGamalKey.construct(*der[1:])


def _import_public(encoded, *kwargs):
    # ElGamalPublicKey ::= SEQUENCE {
    #           modulus INTEGER, -- p
    #           publicExponent INTEGER, -- g
    #           public result of  of g ^ x mod p INTEGER, -- y
    # }
    der = DerSequence().decode(encoded, nr_elements=3, only_ints_expected=True)
    return ElGamalKey.construct(*der)

def _import_subjectPublicKeyInfo(encoded, *kwargs):

    algoid, encoded_key, params = _expand_subject_public_key_info(encoded)
    if algoid != ElGamalKey.oid or params is not None:
        raise ValueError("No ElGamal subjectPublicKeyInfo")
    return _import_public(encoded_key)

def _import_keyDER(extern_key, passphrase):
    """Import an ElGamal key (public or private half), encoded in DER form."""

    decodings = (_import_private,
                 _import_public,
                 _import_subjectPublicKeyInfo,
                 )

    for decoding in decodings:
        try:
            return decoding(extern_key, passphrase)
        except ValueError:
            pass

    raise ValueError("ElGamal key format is not supported")