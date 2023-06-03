from .index import *

# --------------- Concatenation (First step) ---------------
def concatenate_with_timestamp(msg: Msg, filename: str):
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S').encode()
    msg.data = ts + bytes(filename, 'utf-8') + msg.data
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

def radix_deconvert(msg: Msg):
    msg.data = b64decode(msg.data).decode('ascii')
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
def AES_send_pipeline(msg: Msg, key_id):
    session_key = AES_Wrapper.generate_session_key()
    cipher = AES_Wrapper(session_key)
    ciphertext = cipher.encrypt(msg.data)


    entry = public_key_ring.get_entry_by_key_id(key_id)
    if entry['type'] == 'RSA':
        n, e = entry['public_key']
        asym_cipher = RSA_Wrapper(RSA_Wrapper.construct_key(n, e))
    else:
        # Elgamal
        pass
    msg.data = key_id + asym_cipher.encrypt(session_key) + ciphertext
    return msg


def AES_receive_pipeline(data):
    key_id, encrypted_session_key, ciphertext = data[0:8], data[8:136], data[136:]
    # session_key = private_key_ring.get_decrypted_private_key(key_id, passphrase)


def DES3_send_pipeline(msg: Msg, key_id):
    session_key = DES3_Wrapper.generate_session_key()
    cipher = DES3_Wrapper(session_key)
    ciphertext = cipher.encrypt(msg.data)

    entry = public_key_ring.get_entry_by_key_id(key_id)
    if entry['type'] == 'RSA':
        n, e = entry['public_key']
        asym_cipher = RSA_Wrapper(RSA_Wrapper.construct_key(n, e))
    else:
        # Elgamal
        pass
    msg.data = key_id + asym_cipher.encrypt(session_key) + ciphertext
    return msg

def DES3_receive_pipeline(data):
    pass

# --------------- Signature pipeline functions ---------------
def RSA_PSS_send_pipeline(msg: Msg, key_id_and_pass):
    key_id, passphrase = key_id_and_pass
    key = private_key_ring.get_decrypted_private_key(key_id, passphrase)
    cipher = RSA_PSS_Wrapper(key)
    signature = cipher.sign(msg.data)
    ts = bytes(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 'utf-8')
    msg.data = ts + key_id + signature + msg.data
    return msg

def RSA_PSS_receive_pipeline(msg: Msg):
    # ts(???) - key_id(8B) - signature(20B)
    pass