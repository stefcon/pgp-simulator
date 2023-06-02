from index import *
import datetime

def concatenate_with_timestamp(msg: Msg, filename: str):
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S').encode()
    msg.data = ts + filename + msg.data
    return msg

def zip_data(msg: Msg, _):
    msg.data = zlib.compress(msg.data)
    return msg

def unzip_data(msg: Msg, _):
    msg.data = zlib.decompress(msg.data)
    return msg

def radix_convert(msg: Msg, _):
    msg.data = b64encode(msg.data).decode('ascii')
    return msg

def radix_deconvert(msg: Msg):
    msg.data = b64decode(msg.data).decode('ascii')
    return msg

# Serializes the whole class using pickle library
def save_to_file(msg: Msg, filename: str):
    with open(filename, 'wb') as f:
        pickle.dump(msg, f)

# Deserializes the whole class using pickle library
def load_from_file(msg: Msg, filename: str):    
    with open(filename, 'rb') as f:
        msg = pickle.load(f)
    return msg

class SendPipeline:

    def __init__(self, msg: Msg, filename = None, key_id_sender = None, 
                 key_id_recipient = None, passphrase = None):
        self.steps = []
        self.params = []
        self.msg = msg

        # Step 1: Message/Daga part
        self.steps.append(concatenate_with_timestamp)
        self.params.append(filename)
        
        # Step 2: Signature
        if msg.auth is not None:
            self.params.append((key_id_sender, passphrase))
            if msg.auth == 'RSA':
                self.steps.append(RSA_PSS_send_pipeline)
            if msg.auth == 'ELGAMAL/DSA':
                pass

        # Step 3: Zip
        if msg.uze_zip:
            self.params.append(None)
            self.steps.append(zip_data)

        # Step 4: Encryption
        if msg.enc is not None:
            self.params.append(key_id_recipient)
            if msg.enc == 'AES':
                self.steps.append(AES_send_pipeline)
            elif msg.enc == 'DES3':
                self.steps.append(DES3_send_pipeline)

        # Step 5: Radix Conversion
        if msg.uze_rad64:
            self.params.append(None)
            self.steps.append(radix_convert)

        # Step 6: Save in file
        self.params.append(filename)
        self.steps.append(save_to_file)

    def run(self):
        for step, param in zip(self.steps, self.params):
            self.msg = step(self.msg, param)
        return self.msg
    
class ReceivePipeline:
    def __init__(self, filename: str):
        self.steps = []
        self.msg = load_from_file(Msg(), filename)

        # Step 1: Radix Conversion
        if self.msg.uze_rad64:
            self.steps.append(radix_deconvert)

        # Step 2: Decryption
        if self.msg.enc is not None:
            if self.msg.enc == 'AES':
                self.steps.append(AES_receive_pipeline)
            elif self.msg.enc == 'DES3':
                self.steps.append(DES3_receive_pipeline)

        # Step 3: Unzip
        if self.msg.uze_zip:
            self.steps.append(unzip_data)

        # Step 4: Signature
        if self.msg.auth is not None:
            if self.msg.auth == 'RSA':
                self.steps.append(RSA_PSS_receive_pipeline)
            if self.msg.auth == 'ELGAMAL/DSA':
                pass

    def run(self, msg: Msg):
        for step in self.steps:
            msg = step(msg)
        return msg.data