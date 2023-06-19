from .index import *
from .constants import *
from .interfaces import IEncryption
from .exceptions import NoPassphrase
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
        encrypted_session_key = asym_cipher.encrypt(session_key)
    elif entry['type'] == ELGAMAL_ALGORITHM:
        p, g, y = entry['public_key']
        asym_cipher = ElGamal_Wrapper(ElGamal_Wrapper.construct_key(p, g, y))
        encrypted_session_key_tuple = asym_cipher.encrypt(session_key)
        encrypted_session_key = encrypted_session_key_tuple[0] + encrypted_session_key_tuple[1]
    elif entry['type'] == DSA_ALGORITHM:
        # TODO: Raise user-defined exception
        # Ne sme DSA za enkripciju, samo za potpis
        raise
    msg.data = key_id.to_bytes(KEY_ID_LEN, byteorder='big') + encrypted_session_key + ciphertext
    return msg


def decryption_receive_pipeline(msg: Msg, wrapper_and_passphrase):
    cipher_wrapper: IEncryption = wrapper_and_passphrase[0]
    key_id = int.from_bytes(msg.data[0:KEY_ID_LEN], byteorder='big')
    passphrase = wrapper_and_passphrase[1]
    if passphrase == "":
        raise NoPassphrase(key_id)
    key, cipher_length, type = private_key_ring.get_decrypted_private_key(key_id, passphrase)
    if type == RSA_ALGORITHM:
        encrypted_session_key, ciphertext = msg.data[KEY_ID_LEN:KEY_ID_LEN + cipher_length], msg.data[KEY_ID_LEN + cipher_length:]
        asym_cipher = RSA_Wrapper(key)
        session_key = asym_cipher.decrypt(encrypted_session_key)
    elif type == ELGAMAL_ALGORITHM:
        encrypted_session_key, ciphertext = msg.data[KEY_ID_LEN:KEY_ID_LEN + cipher_length * 2], msg.data[KEY_ID_LEN + cipher_length*2:]
        asym_cipher = ElGamal_Wrapper(key)
        encrypted_session_key_tuple =(encrypted_session_key[0:(cipher_length)], encrypted_session_key[(cipher_length):])
        session_key = asym_cipher.decrypt(encrypted_session_key_tuple)
    else:
        # TODO: Raise user-defined exception
        # Ne sme DSA za enkripciju, samo za potpis
        raise ValueError('Invalid key type')
    cipher = cipher_wrapper(session_key)
    msg.data = cipher.decrypt(ciphertext)
    return msg


#TODO mislim da nam ovde ne treba wrapper
def signature_send_pipeline(msg: Msg, wrapper_key_id_and_pass):
    wrapper, key_id, passphrase = wrapper_key_id_and_pass
    key, _, type = private_key_ring.get_decrypted_private_key(key_id, passphrase)
    if type == RSA_ALGORITHM:
        cipher = RSA_PSS_Wrapper(key)
    elif type == DSA_ALGORITHM:
        cipher = DSA_Wrapper(key)
    else:
        # Ne sme Elgamal za potpis, samo za enkripciju
        raise
    signature = cipher.sign(msg.data)
    ts = datetime.datetime.now().strftime(TIMESTAMP_FORMAT).encode()
    msg.data = ts + key_id.to_bytes(KEY_ID_LEN, byteorder='big') + signature + msg.data
    return msg


def signature_receive_pipeline(msg: Msg, _):
    ts, key_id = \
    msg.data[0:TIMESTAMP_LEN], \
    int.from_bytes(msg.data[TIMESTAMP_LEN:TIMESTAMP_LEN+KEY_ID_LEN], byteorder='big')

    entry = public_key_ring.get_entry_by_key_id(key_id)


    if entry['type'] == RSA_ALGORITHM:
        sig_length = RSA_PSS_Wrapper.signature_length(entry['key_length'])
        signature, msg.data = \
        msg.data[TIMESTAMP_LEN+KEY_ID_LEN:TIMESTAMP_LEN+KEY_ID_LEN+sig_length], \
        msg.data[TIMESTAMP_LEN+KEY_ID_LEN+sig_length:]
        n, e = entry['public_key']
        verifier = RSA_PSS_Wrapper(RSA_Wrapper.construct_key(n, e))
    elif entry['type'] == DSA_ALGORITHM:
        sig_length = DSA_Wrapper.signature_length(entry['key_length'])
        signature, msg.data = \
        msg.data[TIMESTAMP_LEN + KEY_ID_LEN:TIMESTAMP_LEN + KEY_ID_LEN + sig_length], \
        msg.data[TIMESTAMP_LEN + KEY_ID_LEN + sig_length:]
        y, g, p, q = entry['public_key']
        verifier = DSA_Wrapper(DSA_Wrapper.construct_key(y, g, p, q))
    else:
        # Ne sme Elgamal za potpis, samo za enkripciju
        raise ValueError('Invalid key type')

    if (not verifier.verify(msg.data, signature)):
        raise Exception('Signature verification failed')
    return msg

