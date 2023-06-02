from dataclasses import dataclass

@dataclass
class Msg():
    enc: str = ''
    auth: str = ''
    uze_zip: bool = False
    uze_rad64: bool = False
    data: bytes = ''
    