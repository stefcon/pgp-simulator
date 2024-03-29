import datetime

from zope.interface import implementer
from .interfaces import *

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
            self.steps.append(signature_send_pipeline)
            if msg.auth == RSA_PSS_ALGORITHM:
                self.params.append((RSA_PSS_Wrapper, key_id_sender, passphrase))
            if msg.auth == DSA_ALGORITHM:
                self.params.append((DSA_Wrapper, key_id_sender, passphrase))

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

@implementer(ISubject)
class ReceivePipeline:
    def __init__(self, filename: str):
        self.steps = []
        self.params = []
        self.filename = filename
        self.msg = load_from_file(Msg(), filename)
        self.passphrase = []
        self.subscribers = set()

        # Step 1: Radix Conversion
        if self.msg.uze_rad64:
            self.steps.append(radix_deconvert)
            self.params.append(None)

        # Step 2: Decryption
        if self.msg.enc is not None:
            self.steps.append(decryption_receive_pipeline)
            if self.msg.enc == AES_ALGORITHM:
                self.params.append((AES_Wrapper, self.passphrase))
            elif self.msg.enc == DES3_ALGORITHM:
                self.params.append((DES3_Wrapper, self.passphrase))

        # Step 3: Unzip
        if self.msg.uze_zip:
            self.params.append(None)
            self.steps.append(unzip_data)

        # Step 4: Signature
        if self.msg.auth is not None:
            self.steps.append(signature_receive_pipeline)
            self.params.append(None)

        
        # Step 5: Message deconcatenation (filename + timestamp)
        self.params.append(filename)
        self.steps.append(extract_message)

    def run(self):
        try:
            for step, param in zip(self.steps, self.params):
                self.msg = step(self.msg, param)
            return self.msg
        except NoPassphrase as np:
            self.notify(np.keyID)

    def run_with_passphrase(self, passphrase):
        self.msg = load_from_file(Msg(), self.filename)
        self.passphrase.append(passphrase)
        self.run()

    def attach(self, observer):
        self.subscribers.add(observer)

    def detach(self, observer):
        """Detach observer"""
        self.subscribers.remove(observer)

    def notify(self, keyID):
        """Notify observers"""
        for subscriber in self.subscribers:
            subscriber.update(self, keyID)
