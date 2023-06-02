
from collections import defaultdict
import datetime
import DES3 as des


class PGPPrivateKeyRing:
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
        self.entries = {}
        self.index_by_user_id = defaultdict(list)
        self.index_by_key_id = {}

    def add_entry(self, key_id, public_key, encrypted_private_key, user_id):
        entry = {
            'key_id': key_id,
            'timestamp': datetime.datetime.strptime(datetime.datetime.now(), '%Y-%m-%d'),
            'public_key': public_key,
            'encrypted_private_key': encrypted_private_key,
            'user_id': user_id
        }
        self.entries[key_id] = entry
        self.index_by_user_id.setdefault(user_id, []).append(entry)
        self.index_by_key_id[key_id] = entry

    def _get_entry_by_key_id(self, key_id):
        return self.index_by_key_id.get(key_id)

    def _get_entries_by_user_id(self, user_id):
        return self.index_by_user_id.get(user_id)

    def _remove_entry(self, key_id):
        entry = self.entries.pop(key_id, None)
        if entry:
            entry = self.index_by_key_id.pop(key_id, None)
            self.index_by_user_id[entry['user_id']].remove(entry)

    def fetch_all_entries(self):
        return list(self.entries.values())
    
    def print_all_entries(self):
        for entry in self.entries.values():
            print('Key ID:', entry['key_id'])
            print('Timestamp:', entry['teimstamp'])
            print('Public Key:', entry['public_key'])
            print('Encrypted Private Key:', entry['encrypted_private_key'])
            print('User ID:', entry['user_id'])
            print()


class PGPPublicKeyRing:

    def __init__(self):
        self.index_by_user_id = defaultdict(list)
        self.index_by_key_id = {}

    def _encrypt_private_key(self, private_key, passphrase):
        pass

    def add_entry(self, key_id, public_key, encrypted_private_key, user_id):
        entry = {
            'key_id': key_id,
            'timestamp': datetime.datetime.strptime(datetime.datetime.now(), '%Y-%m-%d'),
            'public_key': public_key,
            'encrypted_private_key': encrypted_private_key,
            'user_id': user_id
        }
        self.index_by_user_id.setdefault(user_id, []).append(entry)
        self.index_by_key_id[key_id] = entry

    def get_entry_by_key_id(self, key_id):
        return self.index_by_key_id.get(key_id)

    def get_entries_by_user_id(self, user_id):
        return self.index_by_user_id.get(user_id)

    def remove_entry(self, key_id):
        entry = self.index_by_key_id.pop(key_id, None)
        if entry:
            self.index_by_user_id[entry['user_id']].remove(entry)

    def fetch_all_entries(self):
        return list(self.index_by_key_id.values())
    
    def print_all_entries(self):
        for entry in self.index_by_key_id.values():
            print('Key ID:', entry['key_id'])
            print('Timestamp:', entry['teimstamp'])
            print('Public Key:', entry['public_key'])
            print('Encrypted Private Key:', entry['encrypted_private_key'])
            print('User ID:', entry['user_id'])
            print()


# Example usage:
key_ring = PGPPrivateKeyRing()

# Add entries
key_ring.add_entry("ABC123", "public_key1", "encrypted_private_key1", "user1")
key_ring.add_entry("DEF456", "public_key2", "encrypted_private_key2", "user2")
key_ring.add_entry("GHI789", "public_key3", "encrypted_private_key3", "user1")

# Get entry by Key ID
entry = key_ring.get_entry_by_key_id("ABC123")
if entry:
    print("Entry found:")
    print(entry)
else:
    print("Entry not found.")

# Get entries by User ID
entries = key_ring.get_entries_by_user_id("user1")
if entries:
    print("Entries found for user1:")
    for entry in entries:
        print(entry)
else:
    print("No entries found for user1.")

# Remove an entry
key_ring.remove_entry("DEF456")

# Print all entries
key_ring.print_all_entries()
