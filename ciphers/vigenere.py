from typing import List
from ciphers.cipher import Cipher
from ciphers.iomanager import IOManager
from ciphers.globals import alphabet_pos, char_shift


class Vigenere(Cipher):
    def __init__(self, key: str, src: str, dir: str):
        self.key: List[int] = self.make_key_list(key)
        self.src = src
        self.dir = dir

    def encode(self) -> None:
        iomanager = IOManager(self.src, self.dir)
        text = iomanager.read()
        len_key_list = len(self.key)
        encoded_text = []
        key_index = 0
        for char in text:
            if alphabet_pos(char) is None:
                encoded_text.append(char)
                continue
            new_char = char_shift(char, self.key[key_index])
            encoded_text.append(new_char)
            key_index = (key_index + 1) % len_key_list
        iomanager.write(encoded_text)

    def decode(self) -> None:
        self.key = [-x for x in self.key]
        self.encode()
        self.key = [-x for x in self.key]

    @staticmethod
    def make_key_list(key: str) -> List[int]:
        key_list = list(map(alphabet_pos, list(key)))
        if None in key_list:
            raise ValueError("Wrong key")
        return key_list