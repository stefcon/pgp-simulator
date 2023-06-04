from .index import *
from .constants import *
from .interfaces import IEncryption

# --------------- Concatenation (First step) ---------------
def concatenate_with_timestamp(msg: Msg, filename: str):
    ts = datetime.datetime.now().strftime(TIMESTAMP_FORMAT).encode()
    msg.data = ts + bytes(filename, 'utf-8') + msg.data
    return msg

def extract_message(msg: Msg, filename: str):
    ts, msg.data = msg.data[0:TIMESTAMP_LEN], msg.data[TIMESTAMP_LEN:]
    f_b = bytes(filename, 'utf-8')
    _, msg.data = msg.data[:len(f_b)], msg.data[len(f_b):]
    return msg

# --------------- Zip ---------------
def zip_data(msg: Msg, _):
    msg.data = zlib.compress(msg.data)
    return msg

def unzip_data(msg: Msg, _):
    msg.data = zlib.decompress(msg.data)
    return msg

# --------------- Radix Conversion ---------------
def radix_convert(msg: Msg, _):
    msg.data = b64encode(msg.data).decode('ascii')
    return msg

def radix_deconvert(msg: Msg, _):
    msg.data = b64decode(msg.data)
    return msg

# --------------- Serialization of message ---------------
# Serializes the whole class using pickle library
def save_to_file(msg: Msg, filename: str):
    with open(filename, 'wb') as f:
        pickle.dump(msg, f)
    return msg

# Deserializes the whole class using pickle library
def load_from_file(msg: Msg, filename: str):    
    with open(filename, 'rb') as f:
        msg = pickle.load(f)
    return msg

# --------------- Encryption pipeline functions ---------------
def encryption_send_pipeline(msg: Msg, wrapper_and_key_id):
    cipher_wrapper: IEncryption = wrapper_and_key_id[0]
    key_id = wrapper_and_key_id[1]

    session_key = cipher_wrapper.generate_session_key()
    cipher = cipher_wrapper(session_key)
    ciphertext = cipher.encrypt(msg.data)

    entry = public_key_ring.get_entry_by_key_id(key_id)
    if entry['type'] == RSA_ALGORITHM:
        n, e = entry['public_key']
        asym_cipher = RSA_Wrapper(RSA_Wrapper.construct_key(n, e))
    else:
        # Elgamal
        pass
    msg.data = key_id + asym_cipher.encrypt(session_key) + ciphertext
    return msg


def decryption_receive_pipeline(msg: Msg, wrapper_and_passphrase):
    cipher_wrapper: IEncryption = wrapper_and_passphrase[0]
    passphrase = wrapper_and_passphrase[1]

    key_id, encrypted_session_key, ciphertext = msg.data[0:KEY_ID_LEN], msg.data[KEY_ID_LEN:KEY_ID_LEN+RSA_CIPHER_LEN], msg.data[KEY_ID_LEN+RSA_CIPHER_LEN:]
    key, type = private_key_ring.get_decrypted_private_key(key_id, passphrase)
    if type == RSA_ALGORITHM:
        asym_cipher = RSA_Wrapper(key)
    else:
        # Elgamal
        pass
    session_key = asym_cipher.decrypt(encrypted_session_key)
    cipher = cipher_wrapper(session_key)
    msg.data = cipher.decrypt(ciphertext)
    return msg

# --------------- Signature pipeline functions ---------------
def RSA_PSS_send_pipeline(msg: Msg, key_id_and_pass):
    key_id, passphrase = key_id_and_pass
    key, _ = private_key_ring.get_decrypted_private_key(key_id, passphrase)
    cipher = RSA_PSS_Wrapper(key)
    signature = cipher.sign(msg.data)
    ts = datetime.datetime.now().strftime(TIMESTAMP_FORMAT).encode()
    msg.data = ts + key_id + signature + msg.data
    return msg

def RSA_PSS_receive_pipeline(msg: Msg, _):
    ts, key_id, signature, msg.data = \
    msg.data[0:TIMESTAMP_LEN], \
    msg.data[TIMESTAMP_LEN:TIMESTAMP_LEN+KEY_ID_LEN], \
    msg.data[TIMESTAMP_LEN+KEY_ID_LEN:TIMESTAMP_LEN+KEY_ID_LEN+RSA_PSS_SIGNATURE_LEN], \
    msg.data[TIMESTAMP_LEN+KEY_ID_LEN+RSA_PSS_SIGNATURE_LEN:]

    entry = public_key_ring.get_entry_by_key_id(key_id)
    n, e = entry['public_key']
    verifier = RSA_PSS_Wrapper(RSA_Wrapper.construct_key(n, e))
    if (not verifier.verify(msg.data, signature)):
        raise Exception('Signature verification failed')
    return msg
    