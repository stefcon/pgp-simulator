from lib.ElGamal import ElGamalKey, ElGamalEncryption

def main():
    elgamal_key = ElGamalKey()
    elgamal_key.generate_key()
    str_key = elgamal_key.__str__()
    print(str_key)
    with open('elgamal_key.pem', 'wb') as f:
        f.write(elgamal_key.export_key())
    
    with open('elgamal_key.pem', 'rb') as f:
        elgamal_key = ElGamalKey.import_key(f.read())
    
    str_read_key = elgamal_key.__str__()
    if str_key == str_read_key:
        print('OK')

    drugi = ElGamalKey.construct(elgamal_key.p, elgamal_key.g, elgamal_key.y)
    drugi_str = drugi.__str__()
    with open('drugi.pem', 'wb') as f:
        f.write(drugi.export_key())

    with open('drugi.pem', 'rb') as f:
        drugi = ElGamalKey.import_key(f.read())

    drugi_str_read = drugi.__str__()
    if drugi_str == drugi_str_read:
        print('OK')


    # elgamal_enc = ElGamalEncryption(elgamal_key)
    # m = 'cao'
    # m  = m.encode()
    # print('m_b', m)
    # ciphertext = elgamal_enc.encrypt(m)
    # print(ciphertext)

    # print()

    # plaintext = elgamal_enc.decrypt(ciphertext)
    # print(plaintext)


if __name__ == '__main__':
    main()