import datetime
from .interfaces import ISignature
from zope.interface import implementer
from Crypto.Signature import pss
from Crypto.Hash import SHA1
from .key_rings import *

@implementer(ISignature)
class RSA_PSS_Wrapper:
    """Wrapper for SHA hash function"""

    def __init__(self, key):
        self.key = key

    @classmethod
    def signature_length(cls, key_length):
        if key_length == 256:
            return 256
        elif key_length == 128:
            return 128
        else:
            return -1

    def sign(self, message):
        """Hash data"""
        h = SHA1.new(message)
        return pss.new(self.key).sign(h)
    
    def verify(self, message, signature):
        h = SHA1.new(message)
        verifier = pss.new(self.key)
        try:
            verifier.verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False