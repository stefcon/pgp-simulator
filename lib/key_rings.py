from collections import defaultdict
import datetime
from Crypto.Hash import SHA1
from Crypto.PublicKey import RSA, DSA
from .ElGamal import ElGamalKey
from .AES import AES_Wrapper
from .constants import *

class PGPPublicKeyRing:
    """
    PGP public key ring class that contains a list of private keys and public keys with following attributes:
        - Key ID
        - Timestamp
        - Public Key
        - User ID
    Structure can be indexed by both Key ID and User ID.
    """

    def __init__(self):
        self.index_by_user_id = defaultdict(list)
        self.index_by_key_id = {}

    def add_entry(self, key_id, key, email, name, key_length, type):
        user_id = name + ' <' + email + '>'
        if type == RSA_ALGORITHM:
            entry = {
                'key_id': key_id,
                'timestamp': datetime.datetime.now().strftime(TIMESTAMP_FORMAT),
                'public_key': (key.n, key.e),
                'user_id': user_id,
                'key_length': key_length,
                'type': RSA_ALGORITHM
            }
        elif type == ELGAMAL_ALGORITHM:
            entry = {
                'key_id': key_id,
                'timestamp': datetime.datetime.now().strftime(TIMESTAMP_FORMAT),
                'public_key': (key.p, key.g, key.y),
                'user_id': user_id,
                'key_length': key_length,
                'type': ELGAMAL_ALGORITHM
            }
        elif type == DSA_ALGORITHM:
            entry = {
                'key_id': key_id,
                'timestamp': datetime.datetime.now().strftime(TIMESTAMP_FORMAT),
                'public_key': (key.y, key.g, key.p, key.q),
                'user_id': user_id,
                'key_length': key_length,
                'type': DSA_ALGORITHM
            }
        self.index_by_user_id[user_id].append(entry)
        self.index_by_key_id[key_id] = entry

    def get_entry_by_key_id(self, key_id):
        return self.index_by_key_id.get(key_id)

    def get_entries_by_user_id(self, user_id):
        return self.index_by_user_id.get(user_id)

    def remove_entry_key_id(self, key_id):
        entry = self.index_by_key_id.pop(key_id, None)
        if entry is not None:
            self.index_by_user_id[entry['user_id']].remove(entry)

    def remove_entry_user_id(self, user_id):
        entries = self.index_by_user_id.pop(user_id, None)
        if entries is not None:
            for entry in entries:
                self.index_by_key_id.pop(entry['key_id'], None)

    def get_all_entries(self):
        return list(self.index_by_key_id.values())
    
    def print_all_entries(self):
        for entry in self.index_by_key_id.values():
            print('Key ID:', entry['key_id'])
            print('Timestamp:', entry['timestamp'])
            print('Public Key:', entry['public_key'])
            print('User ID:', entry['user_id'])
            print('Key length:', entry['key_length'])
            print('Encryption type:', entry['type'])
            print()

class PGPPrivateKeyRing(PGPPublicKeyRing):
    """
    PGP private key ring class that contains a list of private keys and public keys with following attributes:
        - Key ID
        - Timestamp
        - Public Key
        - Encrypted Private Key
        - User ID
        - H(Passphrase)
    Structure can be indexed by both Key ID and User ID.
    """
    def __init__(self):
        super().__init__()

    def _encrypt_RSA_private_key(self, private_key, passphrase):
        serialized_private_key = private_key.export_key('DER')
        cipher = AES_Wrapper(SHA1.new(bytes(passphrase, 'utf-8')).digest()[:16])
        ciphertext = cipher.encrypt(serialized_private_key)
        return ciphertext

    def _encrypt_ElGamal_private_key(self, private_key, passphrase):
        serialized_private_key = private_key.export_key()
        cipher = AES_Wrapper(SHA1.new(bytes(passphrase, 'utf-8')).digest()[:16])
        ciphertext = cipher.encrypt(serialized_private_key)
        return ciphertext

    def _encrypt_DSA_private_key(self, private_key, passphrase):
        serialized_private_key = private_key.export_key('DER')
        cipher = AES_Wrapper(SHA1.new(bytes(passphrase, 'utf-8')).digest()[:16])
        ciphertext = cipher.encrypt(serialized_private_key)
        return ciphertext
    
    def _decrypt_RSA_private_key(self, encrypted_private_key, passphrase):
        cipher = AES_Wrapper(SHA1.new(bytes(passphrase, 'utf-8')).digest()[:16])
        serialized_private_key= cipher.decrypt(encrypted_private_key)
        private_key = RSA.import_key(serialized_private_key)
        return private_key

    def _decrypt_ElGamal_private_key(self, encrypted_private_key, passphrase):
        cipher = AES_Wrapper(SHA1.new(bytes(passphrase, 'utf-8')).digest()[:16])
        serialized_private_key= cipher.decrypt(encrypted_private_key)
        private_key = ElGamalKey.import_key(serialized_private_key)
        return private_key

    def _decrypt_DSA_private_key(self, encrypted_private_key, passphrase):
        cipher = AES_Wrapper(SHA1.new(bytes(passphrase, 'utf-8')).digest()[:16])
        serialized_private_key= cipher.decrypt(encrypted_private_key)
        private_key = DSA.import_key(serialized_private_key)
        return private_key
    
    def get_decrypted_private_key(self, key_id, passphrase):
        try:
            entry = self.index_by_key_id[key_id]
            encrypted_private_key = entry['encrypted_private_key']
            if entry['type'] == RSA_ALGORITHM:
                return self._decrypt_RSA_private_key(encrypted_private_key, passphrase), entry['key_length'], entry['type']
            elif entry['type'] == ELGAMAL_ALGORITHM:
                return self._decrypt_ElGamal_private_key(encrypted_private_key, passphrase), entry['key_length'], entry['type']
            elif entry['type'] == DSA_ALGORITHM:
                return self._decrypt_DSA_private_key(encrypted_private_key, passphrase), entry['key_length'], entry['type']
        except (ValueError, KeyError):
            # TODO: Raise user-defined exception
            raise

    # def check_password(self, passphrase, key_id):
    #     h_pp_to_be_checked = SHA1.new(bytes(passphrase, 'utf-8')).digest()
    #     if h_pp_to_be_checked != self.index_by_key_id[key_id]['h_passphrase']:
    #         return False
    #     return True

    def add_entry(self, key_id, key, email, name, passphrase, key_length, type):
        user_id = name + ' <' + email + '>'
        if type == RSA_ALGORITHM:
            encrypted_private_key = self._encrypt_RSA_private_key(key, passphrase)
            entry = {
                'key_id': key_id,
                'timestamp': datetime.datetime.now().strftime(TIMESTAMP_FORMAT),
                'public_key': (key.n, key.e),
                'encrypted_private_key': encrypted_private_key,
                'user_id': user_id,
                'key_length': key_length,
                'type': RSA_ALGORITHM
            }
        elif type == ELGAMAL_ALGORITHM:
            encrypted_private_key = self._encrypt_ElGamal_private_key(key, passphrase)
            entry = {
                'key_id': key_id,
                'timestamp': datetime.datetime.now().strftime(TIMESTAMP_FORMAT),
                'public_key': (key.p, key.g, key.y),
                'encrypted_private_key': encrypted_private_key,
                'user_id': user_id,
                'key_length': key_length,
                'type': ELGAMAL_ALGORITHM
            }
        elif type == DSA_ALGORITHM:
            encrypted_private_key = self._encrypt_DSA_private_key(key, passphrase)
            entry = {
                'key_id': key_id,
                'timestamp': datetime.datetime.now().strftime(TIMESTAMP_FORMAT),
                'public_key': (key.y, key.g, key.p, key.q),
                'encrypted_private_key': encrypted_private_key,
                'user_id': user_id,
                'key_length': key_length,
                'type': DSA_ALGORITHM
            }
        self.index_by_user_id[user_id].append(entry)
        self.index_by_key_id[key_id] = entry

    def print_all_entries(self):
        for entry in self.index_by_key_id.values():
            print('Key ID:', entry['key_id'])
            print('Timestamp:', entry['timestamp'])
            print('Public Key:', entry['public_key'])
            print('Encrypted Private Key:', entry['encrypted_private_key'])
            print('User ID:', entry['user_id'])
            print('Key length:', entry['key_length'])
            print('Encryption type:', entry['type'])
            print()


public_key_ring = PGPPublicKeyRing()
private_key_ring = PGPPrivateKeyRing()