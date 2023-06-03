import datetime
from .pipeline_steps import *

class SendPipeline:

    def __init__(self, msg: Msg, filename = None, key_id_sender = None, 
                 key_id_recipient = None, passphrase = None):
        self.steps = []
        self.params = []
        self.msg = msg

        # Step 1: Message concatenation (filename + timestamp)
        self.steps.append(concatenate_with_timestamp)
        self.params.append(filename)
        
        # Step 2: Signature
        if msg.auth is not None:
            self.params.append((key_id_sender, passphrase))
            if msg.auth == RSA_PSS_ALGORITHM:
                self.steps.append(RSA_PSS_send_pipeline)
            if msg.auth == DSA_ELGAMAL_ALGORITHM:
                pass

        # Step 3: Zip
        if msg.uze_zip:
            self.params.append(None)
            self.steps.append(zip_data)

        # Step 4: Encryption
        if msg.enc is not None:
            self.steps.append(encryption_send_pipeline)
            if msg.enc == AES_ALGORITHM:
                self.params.append((AES_Wrapper, key_id_recipient))
            elif msg.enc == DES3_ALGORITHM:
                self.params.append((DES3_Wrapper, key_id_recipient))
                

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
        self.params = []
        self.msg = load_from_file(Msg(), filename)

        # Step 1: Radix Conversion
        if self.msg.uze_rad64:
            self.steps.append(radix_deconvert)
            self.params.append(None)

        # Step 2: Decryption
        if self.msg.enc is not None:
            self.steps.append(decryption_receive_pipeline)
            if self.msg.enc == AES_ALGORITHM:
                self.params.append((AES_Wrapper, 'aaa'))
            elif self.msg.enc == DES3_ALGORITHM:
                self.params.append((DES3_Wrapper, 'aaa'))

        # Step 3: Unzip
        if self.msg.uze_zip:
            self.params.append(None)
            self.steps.append(unzip_data)

        # Step 4: Signature
        if self.msg.auth is not None:
            self.params.append(None)
            if self.msg.auth == RSA_PSS_ALGORITHM:
                self.steps.append(RSA_PSS_receive_pipeline)
            if self.msg.auth == DSA_ELGAMAL_ALGORITHM:
                pass
        
        # Step 5: Message deconcatenation (filename + timestamp)
        self.params.append(filename)
        self.steps.append(extract_message)

    def run(self):
        for step, param in zip(self.steps, self.params):
            self.msg = step(self.msg, param)
        return self.msg