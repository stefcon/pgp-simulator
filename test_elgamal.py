from lib.ElGamal import ElGamalKey, ElGamal_Wrapper

def main():
    elgamal_key = ElGamalKey()
    elgamal_key.generate_key(2048)
    str_key = elgamal_key.__str__()

    key = ElGamal_Wrapper.generate_key(2048)
    elgamal = ElGamal_Wrapper(key)
    str_key = elgamal.key.__str__()

    print(str_key)
    with open('elgamal_key.pem', 'wb') as f:
        f.write(elgamal.key.export_key(passphrase='123'))
    
    with open('elgamal_key.pem', 'rb') as f:
        elgamal.key = ElGamalKey.import_key(f.read(), passphrase='123')
    
    str_read_key = elgamal.key.__str__()
    if str_key == str_read_key:
        print('OK')

    drugi = ElGamalKey.construct(elgamal_key.p, elgamal_key.g, elgamal_key.y)
    print("PRoba:", drugi.p.bit_length())
    drugi_str = drugi.__str__()
    with open('drugi.pem', 'wb') as f:
        f.write(drugi.export_key())

    with open('drugi.pem', 'rb') as f:
        drugi = ElGamalKey.import_key(f.read())

    drugi_str_read = drugi.__str__()
    if drugi_str == drugi_str_read:
        print('OK2')


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