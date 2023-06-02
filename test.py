import lib.AES as aes
import lib.DES3 as des


def main():
    key = des.DES3_Wrapper.generate_session_key()
    print(key)
    cipher = des.DES3_Wrapper(key)
    ciphertext = cipher.encrypt('Hello World')
    print(ciphertext)
    
    cipher = aes.AES_Wrapper(key)
    ciphertext = cipher.encrypt('Hello World')
    print(ciphertext)

if  __name__ == '__main__':
    main()