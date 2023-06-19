from lib.pipeline import SendPipeline, ReceivePipeline
from lib.Msg import Msg
from Crypto.PublicKey import RSA
from lib.RSA import RSA_Wrapper
from lib.DSA import DSA_Wrapper
from lib.ElGamal import ElGamal_Wrapper
from lib.key_rings import public_key_ring, private_key_ring
import lib.pipeline_steps
from lib.constants import *

"""
    Singature length:
    DSA(2048) - 56
    DSA(1024) - 40
    RSA_PSS(2048) - 256
    RSA_PSS(1024) - 128
"""

def main():
    message = 'Hello World!'

    # Intialize message
    msg = Msg()
    msg.data = message.encode()
    msg.enc = AES_ALGORITHM
    msg.auth = DSA_ALGORITHM
    msg.uze_zip = True
    msg.uze_rad64 = True

    # Initialize key ring
    # rsa_key = RSA_Wrapper.generate_key(2048)
    # public_key_ring.add_entry(int.from_bytes(b'0'*8, byteorder='big'), rsa_key, 'adf@adfs.com', 'brr', RSA_ALGORITHM)
    # private_key_ring.add_entry(int.from_bytes(b'0'*8, byteorder='big'), rsa_key, 'adf@adfs.com', 'brr', 'aaa', RSA_ALGORITHM)

    #dsa_key = DSA
    elgamal_length = 2048
    elgamal_key = ElGamal_Wrapper.generate_key(elgamal_length)
    public_key_ring.add_entry(int.from_bytes(b'0'*8, byteorder='big'), elgamal_key, 'adf@adfs.com', 'brr', elgamal_length//8, ELGAMAL_ALGORITHM)
    private_key_ring.add_entry(int.from_bytes(b'0'*8, byteorder='big'), elgamal_key, 'adf@adfs.com', 'brr', 'aaa', elgamal_length//8, ELGAMAL_ALGORITHM)

    dsa_length = 1024
    dsa_key = DSA_Wrapper.generate_key(dsa_length)
    print(dsa_key)
    public_key_ring.add_entry(int.from_bytes(b'2'*8, byteorder='big'), dsa_key, 'adf@adfs.com', 'brr', dsa_length//8, DSA_ALGORITHM)
    private_key_ring.add_entry(int.from_bytes(b'2'*8, byteorder='big'), dsa_key, 'adf@adfs.com', 'brr', 'aaa', dsa_length//8, DSA_ALGORITHM)

    rsa_length = 1024
    rsa_key = RSA_Wrapper.generate_key(rsa_length)
    print(rsa_key.public_key())
    public_key_ring.add_entry(int.from_bytes(b'1'*8, byteorder='big'), rsa_key, 'adf@adfs.com', 'brr', rsa_length//8, RSA_ALGORITHM)
    private_key_ring.add_entry(int.from_bytes(b'1'*8, byteorder='big'), rsa_key, 'adf@adfs.com', 'brr', 'aaa', rsa_length//8, RSA_ALGORITHM)

    rsa_key = RSA.import_key(open('rsa~RSA.pem', 'rb').read(), passphrase='123')

    private_key_ring.add_entry(rsa_key.n % (2 ** 64), rsa_key, 'aaa@a.com', 'brr', '123', 2048//8, RSA_ALGORITHM)
    public_key_ring.add_entry(rsa_key.n % (2 ** 64), rsa_key, 'aaa@a.com', 'brr', 2048//8, RSA_ALGORITHM)
    print(rsa_key.n % (2 ** 64))

    # pipeline = SendPipeline(msg, 'test.txt', rsa_key.n % (2 ** 64), rsa_key.n % (2 ** 64), 'aaa')
    # msg = pipeline.run()

    print(msg.data)

    pipeline = ReceivePipeline('C:/Users/stefc/Fakultet_lokal/ZP/pgp-sim/test2.txt')
    msg = pipeline.run()
    print()
    print(msg.data)


if  __name__ == '__main__':
    main()