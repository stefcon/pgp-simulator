from lib.ElGamal import ElGamalKey, ElGamalEncryption

def main():
    elgamal_key = ElGamalKey()
    elgamal_key.generate_key()
    print(elgamal_key)
    elgamal_enc = ElGamalEncryption(elgamal_key)
    m = 'cao'
    m  = m.encode()
    print('m_b', m)
    ciphertext = elgamal_enc.encrypt(m)
    print(ciphertext)

    print()

    plaintext = elgamal_enc.decrypt(ciphertext)
    print(plaintext)


if __name__ == '__main__':
    main()