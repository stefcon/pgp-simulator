import datetime
from .interfaces import ISignature
from zope.interface import implementer
from Crypto.Signature import pss
from Crypto.Hash import SHA1
from Crypto.PublicKey import RSA
from Crypto import Random
from .Msg import Msg
from .key_rings import *

@implementer(ISignature)
class RSA_PSS_Wrapper:
    """Wrapper for SHA hash function"""

    def __init__(self, key):
        self.key = key

    def sign(self, message):
        """Hash data"""
        h = SHA1.new(message).digest()
        return pss.new(self.key).sign(h)
    
    def verify(self, message, signature):
        h = SHA1.new(message)
        verifier = pss.new(self.key)
        try:
            verifier.verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False
        
def RSA_PSS_send_pipeline(msg: Msg, key_id_and_pass):
    key_id, passphrase = key_id_and_pass
    key = private_key_ring.get_decrypted_private_key(key_id, passphrase)
    cipher = RSA_PSS_Wrapper(key)
    signature = cipher.sign(msg.data)
    ts = datetime.datetime.strptime(datetime.datetime.now(), '%Y-%m-%d')
    msg.data = ts + key_id + signature + msg.data
    return msg

def RSA_PSS_receive_pipeline(msg: Msg):
    # ts(???) - key_id(8B) - signature(20B)
    pass
    