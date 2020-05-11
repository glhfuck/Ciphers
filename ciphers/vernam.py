from ciphers.cipher import Cipher
from dataclasses import dataclass
from ciphers.iomanager import IOManager


@dataclass
class Vernam(Cipher):
    key: str
    src: str
    dir: str

    def encode(self) -> None:
        iomanager = IOManager(self.src, self.dir)
        text = iomanager.read()
        len_key_list = len(self.key)
        encoded_text = []
        key_index = 0
        for char in text:
            new_char = ord(char) ^ ord(self.key[key_index])
            encoded_text.append(chr(new_char))
            key_index = (key_index + 1) % len_key_list
        iomanager.write(encoded_text)

    def decode(self) -> None:
        self.encode()