from zope.interface import Interface
from zope.interface import Attribute

# TODO: Maybe add attributes inside the interfaces to specify the type of encryption and signature algorithm used, as well as the data.
class IEncryption(Interface):
    """Interface for encryption"""

    def encrypt(data):
        """Encrypt data"""

    def decrypt(data):
        """Decrypt data"""
        

class ISignature(Interface):
    """Interface for signature"""

    def sign(data):
        """Sign data"""

    def verify(data):
        """Verify data"""




