import os
from zope.interface import implementer
from .interfaces import *
from collections import defaultdict
import datetime
from Crypto.Hash import SHA1
from Crypto.PublicKey import RSA, DSA
from .ElGamal import ElGamalKey
from .AES import AES_Wrapper
from .constants import *

def generate_key(key_length, key_type):
    if key_type == RSA_ALGORITHM:
        key = RSA.generate(key_length)
        key_id = key.n % (2 ** 64)
    elif key_type == ELGAMAL_ALGORITHM:
        key = ElGamalKey().generate_key(key_length)
        key_id = key.p % (2 ** 64)
    elif key_type == DSA_ALGORITHM:
        key = DSA.generate(key_length)
        key_id = key.p % (2 ** 64)
    else:
        raise ValueError('Invalid key type')
    return key, key_id


def import_key(filepath: str, passphrase: str = None):
        filename = os.path.basename(filepath)
        key_type = filename.split('.')[0].split(DATA_SEPARATOR)[-1]
        with open(filename, 'rb') as f:
            if key_type == RSA_ALGORITHM:
                key = RSA.import_key(f.read(), passphrase=passphrase)
                length = key.n.bit_length() // 8
            elif key_type == ELGAMAL_ALGORITHM:
                key = ElGamalKey.import_key(f.read(), passphrase=passphrase)
                length = key.p.bit_length() // 8
            elif key_type == DSA_ALGORITHM:
                key = DSA.import_key(f.read(), passphrase=passphrase)
                length = key.p.bit_length() // 8
            else:
                raise ValueError('Invalid key type')
            
            return key, key_type, length

def export_key(key, key_type, filepath: str, private=False, passphrase: str = None):
    if not private:
        if key_type == RSA_ALGORITHM:
            key = RSA.construct(key)
        elif key_type == ELGAMAL_ALGORITHM:
            key = ElGamalKey().construct(*key)
        elif key_type == DSA_ALGORITHM:
            key = DSA.construct(key)
        else:
            raise ValueError('Invalid key type')
    with open(filepath + DATA_SEPARATOR + key_type + '.pem', 'wb') as f:
        f.write(key.export_key(format='PEM', passphrase=passphrase))


@implementer(ISubject)
class BaseKeyRing:
    def __init__(self):
        self.index_by_user_id = defaultdict(list)
        self.index_by_key_id = {}
        self.subscribers = set()

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

    def get_user_ids(self, type=None):
        if type is None:
            return list(self.index_by_user_id.keys())
        else:
            return [entry['user_id'] for entry in self.index_by_key_id.values() if entry['type'] != type]
    
    def get_key_ids_for_user_id(self, user_id, type=None):
        if type is None:
            return [entry['key_id'] for entry in self.index_by_user_id[user_id]]
        else:
            return [entry['key_id'] for entry in self.index_by_user_id[user_id] if entry['type'] != type]

    def get_all_entries(self):
        return list(self.index_by_key_id.values())
    
    def attach(self, observer):
        self.subscribers.add(observer)

    def detach(self, observer):
        """Detach observer"""
        self.subscribers.remove(observer)

    def notify(self, new_entry):
        """Notify observers"""
        for subscriber in self.subscribers:
            subscriber.update(self, new_entry)


class PGPPublicKeyRing(BaseKeyRing):
    """
    PGP public key ring class that contains a list of private keys and public keys with following attributes:
        - Key ID
        - Timestamp
        - Public Key
        - User ID
    Structure can be indexed by both Key ID and User ID.
    """

    def __init__(self):
        super().__init__()

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
        else:
            raise ValueError('Invalid key type')
        self.index_by_user_id[user_id].append(entry)
        self.index_by_key_id[key_id] = entry
        self.notify(entry)
    
    def print_all_entries(self):
        for entry in self.index_by_key_id.values():
            print('Key ID:', entry['key_id'])
            print('Timestamp:', entry['timestamp'])
            print('Public Key:', entry['public_key'])
            print('User ID:', entry['user_id'])
            print('Key length:', entry['key_length'])
            print('Encryption type:', entry['type'])
            print()

class PGPPrivateKeyRing(BaseKeyRing):
    """
    PGP private key ring class that contains a list of private keys and public keys with following attributes:
        - Key ID
        - Timestamp
        - Public Key
        - Encrypted Private Key
        - User ID
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
        serialized_private_key = private_key.export_key('DER')
        cipher = AES_Wrapper(SHA1.new(bytes(passphrase, 'utf-8')).digest()[:16])
        ciphertext = cipher.encrypt(serialized_private_key)
        return ciphertext

    def _encrypt_DSA_private_key(self, private_key, passphrase):
        serialized_private_key = private_key.export_key('DER')
        cipher = AES_Wrapper(SHA1.new(bytes(passphrase, 'utf-8')).digest()[:16])
        ciphertext = cipher.encrypt(serialized_private_key)
        return ciphertext
    
    def _decrypt_RSA_private_key(self, encrypted_private_key, passphrase):
        print("udje u rsa")
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
                print('RSA')
                return self._decrypt_RSA_private_key(encrypted_private_key, passphrase), entry['key_length'], entry['type']
            elif entry['type'] == ELGAMAL_ALGORITHM:
                return self._decrypt_ElGamal_private_key(encrypted_private_key, passphrase), entry['key_length'], entry['type']
            elif entry['type'] == DSA_ALGORITHM:
                return self._decrypt_DSA_private_key(encrypted_private_key, passphrase), entry['key_length'], entry['type']
        except (ValueError, KeyError) as e:
            raise ValueError('Invalid passphrase')


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
        else:
            raise ValueError('Invalid key type')
        self.index_by_user_id[user_id].append(entry)
        self.index_by_key_id[key_id] = entry
        self.notify(entry)

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