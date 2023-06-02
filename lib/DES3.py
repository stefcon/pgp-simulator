from zope.interface import implementer
from .interfaces import IEncryption
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from .RSA import RSA_Wrapper
from .key_rings import *
from .Msg import Msg

@implementer(IEncryption)
class DES3_Wrapper():
    
    def __init__(self, key):
        self.key = key

    @classmethod
    def generate_session_key(cls):
        while True:
            try:
                key = DES3.adjust_key_parity(get_random_bytes(24))
                break
            except ValueError:
                pass
        return key
    
    def encrypt(self, data):
        data = bytes(data, 'utf-8')
        cipher = DES3.new(self.key, DES3.MODE_CFB)
        ciphertext = cipher.encrypt(data)
        return cipher.iv + ciphertext

    def decrypt(self, data, iv):
        cipher = DES3.new(self.key, DES3.MODE_CFB, iv=iv)
        plaintext = cipher.decrypt(data)
        return plaintext
    
def DES3_send_pipeline(msg: Msg, key_id):
    session_key = DES3_Wrapper.generate_session_key()
    cipher = DES3_Wrapper(session_key)
    ciphertext = cipher.encrypt(msg.data)

    entry = public_key_ring.get_entry_by_key_id(key_id)
    if entry.type == 'RSA':
        n, e = entry['public_key']
        asym_cipher = RSA_Wrapper(RSA_Wrapper.construct_key((n, e)))
    else:
        # Elgamal
        pass
    msg.data = key_id + asym_cipher.encrypt(session_key) + ciphertext
    return msg

def DES3_receive_pipeline(data):
    pass
