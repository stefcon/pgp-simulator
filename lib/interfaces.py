from zope.interface import Interface
from zope.interface import Attribute


class IAsymEncryption(Interface):
    """Interface for encryption"""

    def generate_key(key_length):
        """Generate public and private key"""

    def construct_key(**kwargs):
        """Construct key out of elements"""
    def encrypt(data):
        """Encrypt data"""

    def decrypt(data):
        """Decrypt data"""

class IEncryption(Interface):
    """Interface for encryption"""

    def generate_session_key():
        """Generate session key"""

    def encrypt(data):
        """Encrypt data"""

    def decrypt(data):
        """Decrypt data"""


class ISignature(Interface):
    """Interface for signature"""

    def signature_length(key_length):
        """Return the signature length based on key length"""
    def sign(message, key):
        """Sign data"""

    def verify(message, signature, key):
        """Verify data"""




