from .interfaces import IEncryption
from zope.interface import implementer
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from .key_rings import *
from .RSA import RSA_Wrapper
from .Msg import Msg

@implementer(IEncryption)
class AES_Wrapper():

    def __init__(self, key):
        self.key = key

    @classmethod
    def generate_session_key(cls):
        return get_random_bytes(16)

    def encrypt(self, data):
        data = bytes(data, 'utf-8')
        cipher = AES.new(self.key, AES.MODE_CFB)
        ciphertext = cipher.encrypt(data)
        return cipher.iv + ciphertext

    def decrypt(self, data, iv):
        cipher = AES.new(self.key, AES.MODE_CFB, iv=iv)
        pt = cipher.decrypt(data)
        return pt
    
def AES_send_pipeline(msg: Msg, key_id):
    session_key = AES_Wrapper.generate_session_key()
    cipher = AES_Wrapper(session_key)
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

def AES_receive_pipeline(data):
    key_id, encrypted_session_key, ciphertext = data[0:8], data[8:136], data[136:]
    # session_key = private_key_ring.get_decrypted_private_key(key_id, passphrase)
    