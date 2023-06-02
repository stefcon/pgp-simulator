from collections import defaultdict
import datetime
import pickle
from .AES import AES_Wrapper
from Crypto.Hash import SHA1


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

    def add_entry(self, key_id, key, email, name, type):
        user_id = name + ' <' + email + '>'
        if type == 'RSA':
            entry = {
                'key_id': key_id,
                'timestamp': datetime.datetime.strptime(datetime.datetime.now(), '%Y-%m-%d'),
                'public_key': (key.n, key.e),
                'user_id': user_id,
                'type': 'RSA'
            }
        elif type == 'ELGAMAL/DSA':
            pass
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

    def _encrypt_private_key(self, private_key, passphrase):
        serialized_private_key = pickle.dumps(private_key)
        h_passphrase = SHA1.new(passphrase).digest()
        cipher = AES_Wrapper(h_passphrase)
        ciphertext = cipher.encrypt(serialized_private_key)
        return ciphertext, h_passphrase
    
    def _decrypt_private_key(self, encrypted_private_key, passphrase):
        iv, ciphertext = encrypted_private_key[0:16], encrypted_private_key[16:]
        cipher = AES_Wrapper(passphrase)
        serialized_private_key= cipher.decrypt(ciphertext, iv)
        private_key = pickle.loads(serialized_private_key)
        return private_key
    
    def get_decrypted_private_key(self, key_id, passphrase):
        encrypted_private_key = self.index_by_key_id[key_id]['encrypted_private_key']
        return self._decrypt_private_key(encrypted_private_key, passphrase)
        

    def check_password(self, passphrase, key_id):
        h_pp_to_be_checked = SHA1.new(passphrase).digest()
        if h_pp_to_be_checked != self.index_by_key_id[key_id]['h_passphrase']:
            return False
        return True

    def add_entry(self, key_id, key, email, name, passphrase, type):
        user_id = name + ' <' + email + '>'
        encrypted_private_key, h_passphrase = self._encrypt_private_key(key, passphrase)
        if type == 'RSA':
            entry = {
                'key_id': key_id,
                'timestamp': datetime.datetime.strptime(datetime.datetime.now(), '%Y-%m-%d'),
                'public_key': (key.n, key.e),
                'encrypted_private_key': encrypted_private_key,
                'user_id': user_id,
                'h_passphrase': h_passphrase,
                'type': 'RSA'
            }
        elif type == 'ELGAMAL/DSA':
            pass
        self.index_by_user_id[user_id].append(entry)
        self.index_by_key_id[key_id] = entry

    def print_all_entries(self):
        for entry in self.index_by_key_id.values():
            print('Key ID:', entry['key_id'])
            print('Timestamp:', entry['timestamp'])
            print('Public Key:', entry['public_key'])
            print('Encrypted Private Key:', entry['encrypted_private_key'])
            print('User ID:', entry['user_id'])
            print('H(passphrase)', entry['h_passphrase'])
            print()


public_key_ring = PGPPublicKeyRing()
private_key_ring = PGPPrivateKeyRing()