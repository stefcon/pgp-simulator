from lib.key_rings import public_key_ring, private_key_ring
from lib.RSA import RSA_Wrapper
from lib.DSA import DSA_Wrapper
from lib.ElGamal import ElGamal_Wrapper
from lib.constants import *
from lib.key_rings import public_key_ring, private_key_ring

def main():

    # Initialize key ring
    rsa_key = RSA_Wrapper.generate_key(2048)
    key_id = rsa_key.p % (2**64)
    print(key_id)
    b_k = key_id.to_bytes(8, byteorder='big')
    print(len(b_k))

    print(int.from_bytes(b_k, byteorder='big'))
    


if __name__ == '__main__':
    main()