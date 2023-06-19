class NoPassphrase(Exception):
    def __init__(self, key_id):
        self.keyID = key_id

class WrongPassphrase(Exception):
    def __init__(self, key_id):
        self.keyID = key_id

    def __str__(self):
        return f'Wrong passphrase for key {self.keyID}'
    
class BadSignature(Exception):
    def __str__(self):
        return f'Bad signature!'