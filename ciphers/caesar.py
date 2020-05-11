from ciphers.cipher import Cipher
from ciphers.globals import char_shift
from dataclasses import dataclass
from ciphers.iomanager import IOManager


@dataclass
class Caesar(Cipher):
    key: int
    src: str
    dir: str

    def encode(self) -> None:
        iomanager = IOManager(self.src, self.dir)
        text = iomanager.read()
        encoded_text = [char_shift(char, int(self.key)) for char in text]
        iomanager.write(encoded_text)

    def decode(self) -> None:
        self.key = -1 * int(self.key)
        self.encode()
        self.key *= -1