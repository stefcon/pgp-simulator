from zope.interface import Interface
from zope.interface import Attribute


class IEncryption(Interface):
    """Interface for encryption"""

    def encrypt(data):
        """Encrypt data"""

    def decrypt(data, iv):
        """Decrypt data"""


class ISignature(Interface):
    """Interface for signature"""

    def sign(message, key):
        """Sign data"""

    def verify(message, signature, key):
        """Verify data"""




