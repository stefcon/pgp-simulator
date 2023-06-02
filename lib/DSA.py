from .interfaces import ISignature
from zope.interface import implementer
from Crypto.Signature import DSS
from Crypto.Hash import SHA1

@implementer(ISignature)
class DSA_Wrapper():

    def __init__(self, key):
        self.key = key

    def sign(self, message):
        h = SHA1.new(message).digest()
        dsa = DSS.new(self.key, 'fips-186-3')
        return dsa.sign(h)


    def verify(self, message, signature):
        h = SHA1.new(message)
        dsa = DSS.new(self.key, 'fips-186-3')
        try:
            dsa.verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False