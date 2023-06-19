class NoPassphrase(Exception):
    def __init__(self, keyID):
        self.keyID = keyID